import uuid

from pytest_docker_tools.builder import fixture_factory


@fixture_factory()
def network(request, docker_client, **kwargs):
    ''' Docker network '''

    network_id = 'pytest-' + str(uuid.uuid4())
    print(f'Creating network {network_id}')
    network = docker_client.networks.create(network_id)
    request.addfinalizer(lambda: network.remove())
    return network
