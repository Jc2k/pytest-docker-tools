from pytest_docker_tools import volume

test_volume_1 = volume()


def test_volume_created(docker_client, test_volume_1):
    for v in docker_client.volumes.list():
        if v.id == test_volume_1.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, 'Looks like we failed to create a volume'
