import inspect
import sys

import pytest


def repository_image(name, tag=None, scope='session'):
    '''
    Fixture factory for fetching container images from a repository. For example
    in your conftest.py you can:

        from pytest_docker_tools import factories

        factories.repository_image('test_image', 'redis:latest')

    By default the fixture has a session scope.
    '''

    tag = tag or name
    if ':' not in tag:
        tag += ':latest'

    def repository_image(request, docker_client):
        sys.stdout.write(f'Fetching {name}\n')

        image = docker_client.images.pull(tag)
        # request.addfinalizer(lambda: docker_client.images.remove(image.id))

        return image

    repository_image.__name__ = name
    pytest.fixture(scope=scope, name=name)(repository_image)

    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    setattr(module, name, repository_image)

    return repository_image
