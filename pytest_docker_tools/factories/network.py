import uuid

from pytest_docker_tools.builder import fixture_factory


@fixture_factory()
def network(request, docker_client, **kwargs):
    ''' Docker network '''

    name = kwargs.pop('name', 'pytest-{uuid}').format(uuid=str(uuid.uuid4()))
    print(f'Creating network {name}')
    network = docker_client.networks.create(name, **kwargs)
    request.addfinalizer(lambda: network.remove())
    return network
