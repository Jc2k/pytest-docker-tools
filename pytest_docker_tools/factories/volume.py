import io
import os
import tarfile
import uuid

from pytest_docker_tools.builder import fixture_factory


def _populate_volume(docker_client, volume, seeds):
    fp = io.BytesIO()
    tf = tarfile.open(mode="w:gz", fileobj=fp)

    for path, contents in seeds.items():
        ti = tarfile.TarInfo(path)
        if contents is None:
            ti.type = tarfile.DIRTYPE
            tf.addfile(ti)
        else:
            ti.size = len(contents)
            tf.addfile(ti, io.BytesIO(contents))

    tf.close()
    fp.seek(0)

    image, logs = docker_client.images.build(
        path=os.path.join(os.path.dirname(__file__), '..', 'contexts/scratch'),
        rm=True,
    )
    list(logs)

    container = docker_client.containers.create(
        image=image.id,
        volumes={
            f'{volume.name}': {'bind': '/data'},
        },
    )

    try:
        container.put_archive('/data', fp)
    finally:
        container.remove(force=True)


@fixture_factory()
def volume(request, docker_client, **kwargs):
    ''' Docker volume '''

    name = kwargs.pop('name', 'pytest-{uuid}').format(uuid=str(uuid.uuid4()))
    seeds = kwargs.pop('initial_content', {})

    print(f'Creating volume {name}')
    volume = docker_client.volumes.create(name, **kwargs)
    request.addfinalizer(lambda: volume.remove(True))

    if seeds:
        _populate_volume(docker_client, volume, seeds)

    return volume
