import uuid

from docker.client import DockerClient
import pytest
from pytest import UsageError

from pytest_docker_tools.builder import fixture_factory
from pytest_docker_tools.utils import (
    hash_params,
    is_reusable_container,
    is_reusable_network,
    set_reusable_labels,
    set_signature,
)


def is_using_network(container, network):
    settings = container.attrs.get("NetworkSettings", {})
    return network.name in settings.get("Networks", {})


def _remove_stale_network(network):
    for container in network.client.containers.list(ignore_removed=True):
        if not is_using_network(container, network):
            continue

        if not is_reusable_container(container):
            raise UsageError(
                f"The network {network.name} is connected to a non-reusable container: {container.id}"
            )

        print(
            f"Removing container {container.name} connected to stale network {network.name}"
        )
        container.remove(force=True)

    print(f"Removing stale reusable network: {network.name}")
    network.remove()


@fixture_factory()
def network(request, docker_client: DockerClient, wrapper_class, **kwargs):
    """ Docker network """

    set_reusable_labels(kwargs, request)

    signature = hash_params(kwargs)
    set_signature(kwargs, signature)

    wrapper_class = wrapper_class or (lambda network: network)

    if request.config.option.reuse_containers:
        if "name" in kwargs.keys():
            name = kwargs["name"]
            networks = docker_client.networks.list()
            for network in networks:
                if network.name != name:
                    continue

                if not is_reusable_network(network):
                    pytest.fail(
                        f"Tried to reuse {network.name} but it does not appear to be a reusable network"
                    )

                if (
                    network.attrs["Labels"].get("pytest-docker-tools.signature", "")
                    != signature
                ):
                    _remove_stale_network(network)
                    break

                return wrapper_class(network)
        else:
            raise UsageError(
                "Error: Tried to use '--reuse-containers' command line argument without "
                "setting 'name' attribute on network"
            )

    name = kwargs.pop("name", "pytest-{uuid}").format(uuid=str(uuid.uuid4()))

    print(f"Creating network {name}")
    network = docker_client.networks.create(name, **kwargs)

    if not request.config.option.reuse_containers:
        request.addfinalizer(lambda: network.remove())

    return wrapper_class(network)
