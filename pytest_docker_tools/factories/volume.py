import uuid

from pytest_docker_tools.builder import fixture_factory


@fixture_factory()
def volume(request, docker_client, **kwargs):
    ''' Docker volume '''

    name = kwargs.pop('name', 'pytest-{uuid}').format(uuid=str(uuid.uuid4()))
    print(f'Creating volume {name}')
    volume = docker_client.volumes.create(name, **kwargs)
    request.addfinalizer(lambda: volume.remove(True))
    return volume
