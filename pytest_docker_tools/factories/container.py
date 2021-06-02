from docker.errors import NotFound
import pytest

from pytest_docker_tools.builder import fixture_factory
from pytest_docker_tools.exceptions import ContainerNotReady, TimeoutError
from pytest_docker_tools.utils import (
    check_signature,
    hash_params,
    is_reusable_container,
    set_reusable_labels,
    set_signature,
    wait_for_callable,
)
from pytest_docker_tools.wrappers import Container


@fixture_factory()
def container(request, docker_client, wrapper_class, **kwargs):
    """ Docker container: image={image} """

    wrapper_class = wrapper_class or Container

    kwargs.update({"detach": True})
    set_reusable_labels(kwargs, request)

    signature = hash_params(kwargs)
    set_signature(kwargs, signature)

    if request.config.option.reuse_containers:
        if "name" not in kwargs.keys():
            pytest.fail(
                "Tried to use '--reuse-containers' command line argument without "
                "setting 'name' attribute on container"
            )

        name = kwargs["name"]

        try:
            current = docker_client.containers.get(name)
        except NotFound:
            pass
        else:
            # Found a container with the right name, but it doesn't have pytest-docker-tools labels
            # We shouldn't just clobber it, its not ours. Bail out.
            if not is_reusable_container(current):
                pytest.fail(
                    f"Tried to reuse {name} but it does not appear to be a reusable container"
                )

            # It's ours, and its not stale. Reuse it!
            if check_signature(current.labels, signature):
                return wrapper_class(current)

            # It's ours and it is stale. Clobber it.
            print(f"Removing stale reusable container: {name}")
            current.remove(force=True)

    timeout = kwargs.pop("timeout", 30)

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
