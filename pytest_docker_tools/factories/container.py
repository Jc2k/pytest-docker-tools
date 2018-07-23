import inspect
from string import Formatter

import pytest
from pytest_docker_tools.utils import wait_for_callable
from pytest_docker_tools.wrappers import Container


def create_container(request, docker_client, *args, **kwargs):
    kwargs.update({'detach': True})

    container = docker_client.containers.run(*args, **kwargs)
    request.addfinalizer(lambda: container.remove(force=True) and container.wait(timeout=10))

    return Container(container)


class FixtureFormatter(Formatter):

    def __init__(self, request):
        self.request = request

    def get_value(self, key, args, kwargs):
        return self.request.getfixturevalue(key)


def _process_val(request, val):
    if isinstance(val, str):
        return FixtureFormatter(request).format(val)
    elif callable(val):
        return val(*[request.getfixturevalue(f) for f in inspect.getargspec(val)[0]])
    return val


def _process_list(request, val):
    return [_process(request, v) for v in val]


def _process_dict(request, mapping):
    return {_process(request, k): _process(request, v) for (k, v) in mapping.items()}


def _process(request, val):
    if isinstance(val, dict):
        return _process_dict(request, val)
    elif isinstance(val, list):
        return _process_list(request, val)
    else:
        return _process_val(request, val)


def container(*, scope='function', **kwargs):
    '''
    Fixture factory for creating containers. For example in your conftest.py
    you can:

        from pytest_docker_tools import container_fixture

        test_container = container_fixture('test_container', 'redis')

    This will create a container called 'test_container' from the 'redis' image.
    '''

    def container(request, docker_client):
        local_kwargs = dict(kwargs)

        container = create_container(
            request,
            docker_client,
            **_process_dict(request, local_kwargs)
        )

        wait_for_callable(
            f'Waiting for container to be ready',
            lambda: container.reload() or container.ready(),
        )

        return container

    pytest.fixture(scope=scope)(container)

    return container
