import uuid

import pytest


def volume(scope='function'):
    '''
    Fixture factory for creating volumes. For example in your conftest.py you can:

        from pytest_docker_tools import volume_fixture

        test_storage = volume_fixture('test_storage')

    Then you can reference that volume from your test:

        def test_a_docker_volume(test_storage):
            print(test_storage.id)

    The fixture has a function scope - it will be destroyed after your test exits.
    '''

    def volume(request, docker_client):
        vol_id = 'pytest-' + str(uuid.uuid4())
        print(f'Creating volume {vol_id}')
        volume = docker_client.volumes.create(vol_id)
        request.addfinalizer(lambda: volume.remove(True))
        return volume

    pytest.fixture(scope=scope)(volume)

    return volume
