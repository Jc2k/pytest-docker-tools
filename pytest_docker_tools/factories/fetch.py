import sys

from pytest_docker_tools.builder import fixture_factory


@fixture_factory(scope="session")
def fetch(request, docker_client, wrapper_class, **kwargs):
    """ Docker image: Fetched from {repository} """

    sys.stdout.write(f'Fetching {kwargs["repository"]}\n')

    image = docker_client.images.pull(**kwargs)
    # request.addfinalizer(lambda: docker_client.images.remove(image.id))

    wrapper_class = wrapper_class or (lambda image: image)
    return wrapper_class(image)
