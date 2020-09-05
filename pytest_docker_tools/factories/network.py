import uuid

from pytest_docker_tools.builder import fixture_factory


@fixture_factory()
def network(request, docker_client, wrapper_class, **kwargs):
    """ Docker network """

    name = kwargs.pop("name", "pytest-{uuid}").format(uuid=str(uuid.uuid4()))

    print(f"Creating network {name}")
    network = docker_client.networks.create(name, **kwargs)
    request.addfinalizer(lambda: network.remove())

    wrapper_class = wrapper_class or (lambda network: network)
    return wrapper_class(network)
