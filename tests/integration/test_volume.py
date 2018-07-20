from pytest_docker_tools import factories

factories.volume('test_volume_1')


def test_volume_created(docker_client, test_volume_1):
    for volume in docker_client.volumes.list():
        if volume.id == test_volume_1.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, 'Looks like we failed to create a volume'
