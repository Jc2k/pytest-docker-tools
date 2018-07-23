import sys

import pytest


def build(*, path, scope='session'):
    '''
    Fixture factory for creating container images from a Dockerfile. For example
    in your conftest.py you can:

        from pytest_docker_tools import build

        test_image = build(path='path/to/buildcontext')

    Where the path is a folder containing a Dockerfile.

    By default the fixture has a session scope.
    '''

    def build(request, docker_client):
        sys.stdout.write(f'Building {path}')

        try:
            image, logs = docker_client.images.build(
                path=path
            )

            for line in logs:
                sys.stdout.write('.')
                sys.stdout.flush()

        finally:
            sys.stdout.write('\n')

        # request.addfinalizer(lambda: docker_client.images.remove(image.id))

        return image

    pytest.fixture(scope=scope)(build)

    return build
