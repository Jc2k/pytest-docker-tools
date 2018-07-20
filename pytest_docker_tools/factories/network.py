import inspect
import uuid

import pytest


def network(name, scope='function'):
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
        vol_id = name + '-' + str(uuid.uuid4())
        print(f'Creating network {vol_id}')
        network = docker_client.networks.create(vol_id)
        request.addfinalizer(lambda: network.remove())
        return network

    network.__name__ = name

    pytest.fixture(scope=scope, name=name)(network)

    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    setattr(module, name, network)

    return network
