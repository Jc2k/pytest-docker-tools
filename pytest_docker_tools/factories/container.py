from pytest_docker_tools.builder import fixture_factory
from pytest_docker_tools.exceptions import ContainerNotReady, TimeoutError
from pytest_docker_tools.utils import wait_for_callable
from pytest_docker_tools.wrappers import Container


@fixture_factory()
def container(request, docker_client, wrapper_class, **kwargs):
    """ Docker container: image={image} """

    wrapper_class = wrapper_class or Container

    if request.config.option.reuse_containers:
        name = kwargs['name']
        if name:
            current_containers = docker_client.containers.list()
            for cont in current_containers:
                if cont.name == name:
                    raw_container = cont
                    return wrapper_class(raw_container)
        else:
            raise RuntimeError("Error: Tried to use '--reuse_containers' command line argument without "
                               "setting 'name' attribute on container")

    timeout = kwargs.pop("timeout", 30)

    kwargs.update({"detach": True})

    raw_container = docker_client.containers.run(**kwargs)
    if not request.config.option.reuse_containers:
        request.addfinalizer(
            lambda: raw_container.remove(force=True) and raw_container.wait(timeout=10)
        )

    container = wrapper_class(raw_container)

    try:
        wait_for_callable("Waiting for container to be ready", container.ready, timeout)
    except TimeoutError:
        raise ContainerNotReady(
            container, "Timeout while waiting for container to be ready"
        )

    return container
