import sys

from pytest_docker_tools.builder import fixture_factory


@fixture_factory(scope="session")
def build(request, docker_client, wrapper_class, **kwargs):
    """ Docker image: built from "{path}" """

    # The docker build command now defaults to --rm=true, but docker-py doesnt
    # Let's do what docker build does by default
    kwargs.setdefault("rm", True)

    if "path" in kwargs:
        sys.stdout.write(f'Building {kwargs["path"]}')
    else:
        sys.stdout.write("Building")

    try:
        image, logs = docker_client.images.build(**kwargs)

        for line in logs:
            sys.stdout.write(".")
            sys.stdout.flush()

    finally:
        sys.stdout.write("\n")

    # request.addfinalizer(lambda: docker_client.images.remove(image.id))

    wrapper_class = wrapper_class or (lambda image: image)
    return wrapper_class(image)
