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


def _process_image(request, image):
    if hasattr(image, '_pytestfixturefunction'):
        return request.getfixturevalue(image._pytestfixturefunction.name).id
    return image


def _process_network(request, network):
    if hasattr(network, '_pytestfixturefunction'):
        return request.getfixturevalue(network._pytestfixturefunction.name).id
    return network


def _process_volumes(request, volumes):
    vols = {}
    for key, val in volumes.items():
        if hasattr(key, '_pytestfixturefunction'):
            key = request.getfixturevalue(key._pytestfixturefunction.name).id
        vols[key] = val
    return vols


def _process_environment(request, environment):
    env = {}
    for key, val in environment.items():
        if callable(val):
            val = val(*[request.getfixturevalue(f) for f in inspect.getargspec(val)[0]])
        env[key] = val
    return env


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
    return {k: _process(request, v) for (k, v) in mapping.items()}


def _process(request, val):
    if isinstance(val, dict):
        return _process_dict(request, val)
    elif isinstance(val, list):
        return _process_list(request, val)
    else:
        return _process_val(request, val)


def container(name, image, *, scope='function', **kwargs):
    '''
    Fixture factory for creating containers. For example in your conftest.py
    you can:

        from pytest_docker_tools import container_fixture

        test_container = container_fixture('test_container', 'redis')

    This will create a container called 'test_container' from the 'redis' image.
    '''

    def container(request, docker_client):
        local_kwargs = dict(kwargs)

        if 'network' in local_kwargs:
            local_kwargs['network'] = _process_network(request, local_kwargs.pop('network'))

        environment = _process_environment(request, local_kwargs.pop('environment', {}))
        volumes = _process_volumes(request, local_kwargs.pop('volumes', {}))

        container = create_container(
            request,
            docker_client,
            _process_image(request, image),
            environment=environment,
            volumes=volumes,
            **_process_dict(request, local_kwargs)
        )

        wait_for_callable(
            f'Waiting for container {name} to be ready',
            lambda: container.reload() or container.ready(),
        )

        return container

    container.__name__ = name
    pytest.fixture(scope=scope, name=name)(container)

    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    setattr(module, name, container)

    return container
