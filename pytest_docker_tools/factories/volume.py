import uuid

from pytest_docker_tools.builder import fixture_factory


@fixture_factory()
def volume(request, docker_client, **kwargs):
    ''' Docker volume '''

    vol_id = 'pytest-' + str(uuid.uuid4())
    print(f'Creating volume {vol_id}')
    volume = docker_client.volumes.create(vol_id)
    request.addfinalizer(lambda: volume.remove(True))
    return volume
