import sys

from pytest_docker_tools.builder import fixture_factory


@fixture_factory(scope='session')
def build(request, docker_client, **kwargs):
    ''' Docker image: built from "{path}" '''

    # The docker build command now defaults to --rm=true, but docker-py doesnt
    # Let's do what docker build does by default
    kwargs.setdefault('rm', True)

    sys.stdout.write(f'Building {kwargs["path"]}')

    try:
        image, logs = docker_client.images.build(**kwargs)

        for line in logs:
            sys.stdout.write('.')
            sys.stdout.flush()

    finally:
        sys.stdout.write('\n')

    # request.addfinalizer(lambda: docker_client.images.remove(image.id))

    return image
