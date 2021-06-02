import hashlib
import json

from pytest import UsageError

from pytest_docker_tools.builder import fixture_factory
from pytest_docker_tools.exceptions import ContainerNotReady, TimeoutError
from pytest_docker_tools.utils import (
    is_reusable_container,
    set_reusable_labels,
    wait_for_callable,
)
from pytest_docker_tools.wrappers import Container


@fixture_factory()
def container(request, docker_client, wrapper_class, **kwargs):
    """ Docker container: image={image} """

    wrapper_class = wrapper_class or Container

    kwargs.update({"detach": True})
    set_reusable_labels(kwargs, request)

    signature = hashlib.sha256(
        json.dumps(kwargs, sort_keys=True).encode("utf-8")
    ).hexdigest()
    kwargs.setdefault("labels", {})["pytest-docker-tools.signature"] = signature

    if request.config.option.reuse_containers:
        if "name" in kwargs.keys():
            name = kwargs["name"]
            current_containers = docker_client.containers.list(ignore_removed=True)
            for cont in current_containers:
                if cont.name != name:
                    continue
                if not is_reusable_container(cont):
                    continue
                if cont.labels.get("pytest-docker-tools.signature", "") != signature:
                    print(f"Removing stale reusable container: {name}")
                    cont.remove(force=True)
                    break
                return wrapper_class(cont)
        else:
            raise UsageError(
                "Error: Tried to use '--reuse-containers' command line argument without "
                "setting 'name' attribute on container"
            )

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
