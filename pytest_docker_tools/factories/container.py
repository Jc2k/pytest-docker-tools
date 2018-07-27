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


class FixtureCollector(object):

    def visit_value(self, val):
        if isinstance(val, str):
            for literal_text, format_spec, conversion, _ in Formatter().parse(val):
                if format_spec:
                    yield format_spec.split('.')[0].split('[')[0]
        elif callable(val):
            yield from inspect.getargspec(val)[0]

    def visit_list(self, val):
        for v in val:
            yield from self.visit(v)

    def visit_dict(self, mapping):
        for k, v in mapping.items():
            yield from self.visit(k)
            yield from self.visit(v)

    def visit(self, value):
        if isinstance(value, dict):
            yield from self.visit_dict(value)
        elif isinstance(value, list):
            yield from self.visit_list(value)
        elif value:
            yield from self.visit_value(value)

    def get_fixtures_from_params(self, kwargs):
        return tuple(set(self.visit(kwargs)))


class ConstructorRenderer(object):

    def __init__(self, request):
        self.request = request

    def visit_value(self, val):
        if isinstance(val, str):
            return FixtureFormatter(self.request).format(val)
        elif callable(val):
            return val(*[self.request.getfixturevalue(f) for f in inspect.getargspec(val)[0]])
        return val

    def visit_list(self, val):
        return [self.visit(v) for v in val]

    def visit_dict(self, mapping):
        return {self.visit(k): self.visit(v) for (k, v) in mapping.items()}

    def visit(self, value):
        if isinstance(value, dict):
            return self.visit_dict(value)
        elif isinstance(value, list):
            return self.visit_list(value)
        elif value:
            return self.visit_value(value)


class FixtureFormatter(Formatter):

    def __init__(self, request):
        self.request = request

    def get_value(self, key, args, kwargs):
        return self.request.getfixturevalue(key)


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
            **ConstructorRenderer(request).visit(local_kwargs)
        )

        wait_for_callable(
            f'Waiting for container to be ready',
            lambda: container.reload() or container.ready(),
        )

        return container

    pytest.fixture(scope=scope)(container)

    # pytest.mark.usefixtures(*FixtureCollector().get_fixtures_from_params(kwargs))(container)

    return container
