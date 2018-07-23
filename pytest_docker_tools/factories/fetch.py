import sys

import pytest


def fetch(tag, scope='session'):
    '''
    Fixture factory for fetching container images from a repository. For example
    in your conftest.py you can:

        from pytest_docker_tools import factories

        factories.repository_image('test_image', 'redis:latest')

    By default the fixture has a session scope.
    '''

    if ':' not in tag:
        tag += ':latest'

    def fetch(request, docker_client):
        sys.stdout.write(f'Fetching {tag}\n')

        image = docker_client.images.pull(tag)
        # request.addfinalizer(lambda: docker_client.images.remove(image.id))

        return image

    pytest.fixture(scope=scope)(fetch)

    return fetch
