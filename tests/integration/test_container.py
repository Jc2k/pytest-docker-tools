from pytest_docker_tools import container_fixture

container_fixture('test', 'redis')


def test_container_created(docker_client, mycontainer):
    for container in docker_client.containers.list():
        if container.id == mycontainer['container'].id:
            # Looks like we managed to start one!
            break
    else:
        assert False, 'Looks like we failed to start a container'
