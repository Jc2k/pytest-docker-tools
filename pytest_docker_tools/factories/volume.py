import io
import os
import tarfile
import uuid

from docker.errors import NotFound
import pytest

from pytest_docker_tools.builder import fixture_factory
from pytest_docker_tools.utils import (
    check_signature,
    hash_params,
    is_reusable_container,
    is_reusable_volume,
    is_using_volume,
    set_reusable_labels,
    set_signature,
)


def _remove_stale_volume(docker_client, volume):
    for container in docker_client.containers.list(ignore_removed=True, all=True):
        if not is_using_volume(container, volume):
            continue

        if not is_reusable_container(container):
            pytest.fail(
                f"The volume {volume.name} is connected to a non-reusable container: {container.id}"
            )

        print(
            f"Removing container {container.name} connected to stale volume {volume.name}"
        )
        container.remove(force=True)

    print(f"Removing stale reusable volume: {volume.name}")
    volume.remove()


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

    set_reusable_labels(kwargs, request)

    signature = hash_params(kwargs)
    set_signature(kwargs, signature)

    if request.config.option.reuse_containers:
        if "name" not in kwargs.keys():
            pytest.fail(
                "Error: Tried to use '--reuse-containers' command line argument without "
                "setting 'name' attribute on volume"
            )

        name = kwargs["name"]
        try:
            volume = docker_client.volumes.get(name)
        except NotFound:
            pass
        else:
            # Found a volume with the right name, but it doesn't have pytest-docker-tools labels
            # We shouldn't just clobber it, its not ours. Bail out.
            if not is_reusable_volume(volume):
                pytest.fail(
                    f"Tried to reuse {name} but it does not appear to be a reusable volume"
                )

            # It's ours, and its not stale. Reuse it!
            if check_signature(volume.attrs["Labels"], signature):
                return wrapper_class(volume)

            # It's ours and it is stale. Clobber it.
            _remove_stale_volume(docker_client, volume)

    name = kwargs.pop("name", "pytest-{uuid}").format(uuid=str(uuid.uuid4()))
    seeds = kwargs.pop("initial_content", {})

    print(f"Creating volume {name}")
    volume = docker_client.volumes.create(name, **kwargs)

    if not request.config.option.reuse_containers:
        request.addfinalizer(lambda: volume.remove(True))

    if seeds:
        _populate_volume(docker_client, volume, seeds)

    return wrapper_class(volume)
