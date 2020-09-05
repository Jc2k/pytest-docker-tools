from pytest_docker_tools.builder import fixture_factory


@fixture_factory(scope="session")
def image(request, docker_client, wrapper_class, **kwargs):
    """ Docker image: named "{name}" (already available) """

    image = docker_client.images.get(kwargs["name"])
    wrapper_class = wrapper_class or (lambda image: image)
    return wrapper_class(image)
