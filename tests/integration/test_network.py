from pytest_docker_tools import network

test_network_1 = network()
test_network_2 = network()


def test_network_1_created(docker_client, test_network_1):
    for n in docker_client.networks.list():
        if n.id == test_network_1.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, "Looks like we failed to create a network"


def test_reusable_network_2_created(
    enable_container_reuse, docker_client, test_network_2
):
    for n in docker_client.networks.list():
        if n.id == test_network_2.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, "Looks like we failed to create a network"
