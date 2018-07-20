import inspect
import sys

import pytest


def image(name, path=None, scope='session'):
    '''
    Fixture factory for creating container images from a Dockerfile. For example
    in your conftest.py you can:

        from pytest_docker_tools import image_fixture

        test_image = image_fixture('test_image', path='path/to/buildcontext')

    Where the path is a folder containing a Dockerfile.

    By default the fixture has a session scope.
    '''

    def image(request, docker_client):
        sys.stdout.write(f'Building {name}')

        try:
            image, logs = docker_client.images.build(
                path=path or name,
                tag=f'{name}:latest'
            )

            for line in logs:
                sys.stdout.write('.')
                sys.stdout.flush()

        finally:
            sys.stdout.write('\n')

        # request.addfinalizer(lambda: docker_client.images.remove(image.id))

        return image

    image.__name__ = name
    pytest.fixture(scope=scope, name=name)(image)

    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    setattr(module, name, image)

    return image
