from pytest_docker_tools.builder import fixture_factory
from pytest_docker_tools.exceptions import ContainerNotReady, TimeoutError
from pytest_docker_tools.utils import wait_for_callable
from pytest_docker_tools.wrappers import Container


@fixture_factory()
def container(request, docker_client, wrapper_class, **kwargs):
    """ Docker container: image={image} """

    timeout = kwargs.pop("timeout", 30)

    kwargs.update({"detach": True})

    raw_container = docker_client.containers.run(**kwargs)
    request.addfinalizer(
        lambda: raw_container.remove(force=True) and raw_container.wait(timeout=10)
    )

    wrapper_class = wrapper_class or Container
    container = wrapper_class(raw_container)

    try:
        wait_for_callable("Waiting for container to be ready", container.ready, timeout)
    except TimeoutError:
        raise ContainerNotReady(
            container, "Timeout while waiting for container to be ready"
        )

    return container
