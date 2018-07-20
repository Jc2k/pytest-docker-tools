from pytest_docker_tools import factories

factories.container('test_container_1', 'redis')


def test_container_created(docker_client, test_container_1):
    for container in docker_client.containers.list():
        if container.id == test_container_1['container'].id:
            # Looks like we managed to start one!
            break
    else:
        assert False, 'Looks like we failed to start a container'
