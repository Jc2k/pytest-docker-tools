import sys

from pytest_docker_tools.builder import fixture_factory


@fixture_factory(scope='session')
def fetch(request, docker_client, **kwargs):
    ''' Docker image: Fetched from {repository} '''

    sys.stdout.write(f'Fetching {kwargs["repository"]}\n')

    image = docker_client.images.pull(**kwargs)
    # request.addfinalizer(lambda: docker_client.images.remove(image.id))

    return image
