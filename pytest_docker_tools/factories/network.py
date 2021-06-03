import uuid

from docker.client import DockerClient
from docker.errors import NotFound
import pytest

from pytest_docker_tools.builder import fixture_factory
from pytest_docker_tools.utils import (
    check_signature,
    hash_params,
    is_reusable_container,
    is_reusable_network,
    is_using_network,
    set_reusable_labels,
    set_signature,
)


def _remove_stale_network(network):
    for container in network.client.containers.list(ignore_removed=True, all=True):
        if not is_using_network(container, network):
            continue

        if not is_reusable_container(container):
            pytest.fail(
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
        if "name" not in kwargs.keys():
            pytest.fail(
                "Error: Tried to use '--reuse-containers' command line argument without "
                "setting 'name' attribute on network"
            )

        name = kwargs["name"]
        try:
            network = docker_client.networks.get(name)
        except NotFound:
            pass
        else:
            # Found a network with the right name, but it doesn't have pytest-docker-tools labels
            # We shouldn't just clobber it, its not ours. Bail out.
            if not is_reusable_network(network):
                pytest.fail(
                    f"Tried to reuse {network.name} but it does not appear to be a reusable network"
                )

            # It's ours, and its not stale. Reuse it!
            if check_signature(network.attrs["Labels"], signature):
                return wrapper_class(network)

            # It's ours and it is stale. Clobber it.
            _remove_stale_network(network)

    name = kwargs.pop("name", "pytest-{uuid}").format(uuid=str(uuid.uuid4()))

    print(f"Creating network {name}")
    network = docker_client.networks.create(name, **kwargs)

    if not request.config.option.reuse_containers:
        request.addfinalizer(lambda: network.remove())

    return wrapper_class(network)
