import textwrap

import pytest
from pytest_docker_tools.templates import (
    find_fixtures_in_params,
    resolve_fixtures_in_params,
)
from pytest_docker_tools.utils import wait_for_callable
from pytest_docker_tools.wrappers import Container


def create_container(request, docker_client, *args, **kwargs):
    kwargs.update({'detach': True})

    container = docker_client.containers.run(*args, **kwargs)
    request.addfinalizer(lambda: container.remove(force=True) and container.wait(timeout=10))

    return Container(container)


def build_fixture_function(name, docstring, fixtures, callable):
    fixtures_str = ','.join(fixtures)
    template = textwrap.dedent(f'''
    def {name}({fixtures_str}):
        \'\'\'
        {docstring}
        \'\'\'
        return _{name}(request, docker_client)
    ''')
    globals = {
        f'_{name}': callable,
    }
    exec(template, globals)
    return globals[name]


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
            **resolve_fixtures_in_params(request, local_kwargs)
        )

        wait_for_callable(
            f'Waiting for container to be ready',
            lambda: container.reload() or container.ready(),
        )

        return container

    fixtures = find_fixtures_in_params(kwargs).union(set(('request', 'docker_client')))

    container = build_fixture_function(
        'container',
        f'Docker container; image={kwargs["image"]}',
        fixtures,
        container
    )
    pytest.fixture(scope=scope)(container)

    return container
