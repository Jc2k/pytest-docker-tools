from pytest_docker_tools import factories

factories.network('test_network_1')


def test_network_created(docker_client, test_network_1):
    for network in docker_client.networks.list():
        if network.id == test_network_1.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, 'Looks like we failed to create a network'
