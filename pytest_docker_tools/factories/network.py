import uuid

import pytest


def network(scope='function'):
    '''
    Fixture factory for creating networks. For example in your conftest.py you can:

        from pytest_docker_tools import network_fixture

        test_storage = network_fixture('test_storage')

    Then you can reference that network from your test:

        def test_a_docker_network(test_storage):
            print(test_storage.id)

    The fixture has a function scope - it will be destroyed after your test exits.
    '''

    def network(request, docker_client):
        network_id = 'pytest-' + str(uuid.uuid4())
        print(f'Creating network {network_id}')
        network = docker_client.networks.create(network_id)
        request.addfinalizer(lambda: network.remove())
        return network

    pytest.fixture(scope=scope)(network)

    return network
