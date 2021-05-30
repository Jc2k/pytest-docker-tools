import io
import os
import tarfile
import uuid

from pytest import UsageError

from pytest_docker_tools.builder import fixture_factory
from pytest_docker_tools.utils import is_reusable_volume, set_reusable_labels


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
        path=os.path.join(os.path.dirname(__file__), "..", "contexts/scratch"),
        rm=True,
    )
    list(logs)

    container = docker_client.containers.create(
        image=image.id,
        volumes={
            f"{volume.name}": {"bind": "/data"},
        },
    )

    try:
        container.put_archive("/data", fp)
    finally:
        container.remove(force=True)


@fixture_factory()
def volume(request, docker_client, wrapper_class, **kwargs):
    """ Docker volume """
    wrapper_class = wrapper_class or (lambda volume: volume)

    if request.config.option.reuse_containers:
        if "name" in kwargs.keys():
            name = kwargs["name"]
            volumes = docker_client.volumes.list()
            for volume in volumes:
                if volume.name == name and is_reusable_volume(volume):
                    return wrapper_class(volume)
        else:
            raise UsageError(
                "Error: Tried to use '--reuse-containers' command line argument without "
                "setting 'name' attribute on volume"
            )

    name = kwargs.pop("name", "pytest-{uuid}").format(uuid=str(uuid.uuid4()))
    seeds = kwargs.pop("initial_content", {})

    set_reusable_labels(kwargs, request)

    print(f"Creating volume {name}")
    volume = docker_client.volumes.create(name, **kwargs)

    if not request.config.option.reuse_containers:
        request.addfinalizer(lambda: volume.remove(True))

    if seeds:
        _populate_volume(docker_client, volume, seeds)

    return wrapper_class(volume)
