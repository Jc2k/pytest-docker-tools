import hashlib
import json
import uuid

from pytest import UsageError

from pytest_docker_tools.builder import fixture_factory
from pytest_docker_tools.utils import is_reusable_network, set_reusable_labels


@fixture_factory()
def network(request, docker_client, wrapper_class, **kwargs):
    """ Docker network """

    set_reusable_labels(kwargs, request)

    signature = hashlib.sha256(
        json.dumps(kwargs, sort_keys=True).encode("utf-8")
    ).hexdigest()
    kwargs.setdefault("labels", {})["pytest-docker-tools.signature"] = signature

    wrapper_class = wrapper_class or (lambda network: network)

    if request.config.option.reuse_containers:
        if "name" in kwargs.keys():
            name = kwargs["name"]
            networks = docker_client.networks.list()
            for network in networks:
                if network.name != name:
                    continue
                if not is_reusable_network(network):
                    continue
                if (
                    network.attrs["Labels"].get("pytest-docker-tools.signature", "")
                    != signature
                ):
                    print(f"Removing stale reusable network: {name}")
                    network.remove()
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
