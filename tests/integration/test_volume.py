from _pytest.pytester import Pytester
from docker.client import DockerClient
from docker.errors import NotFound
import pytest

from pytest_docker_tools import volume

test_volume_1 = volume()


def test_volume1_created(docker_client: DockerClient, test_volume_1):
    for v in docker_client.volumes.list():
        if v.id == test_volume_1.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, "Looks like we failed to create a volume"


def test_reusable_must_be_named(
    request, pytester: Pytester, docker_client: DockerClient
):
    with pytest.raises(NotFound):
        docker_client.volumes.get("my-reusable-volume")

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import volume",
                "memcache_volume = volume(",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_volume="\n".join(
            (
                "def test_session_1(memcache_volume):",
                "    assert memcache_volume.name == 'my-reusable-volume'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=0, errors=1)

    with pytest.raises(NotFound):
        docker_client.volumes.get("my-reusable-volume")


def test_set_own_label(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            volume = docker_client.volumes.get("my-reusable-volume")
        except NotFound:
            return
        volume.remove()

    with pytest.raises(NotFound):
        docker_client.volumes.get("my-reusable-volume")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import volume",
                "memcache_volume = volume(",
                "    name='my-reusable-volume',",
                "    labels={'my-label': 'testtesttest'},",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_volume="\n".join(
            (
                "def test_session_1(memcache_volume):",
                "    assert memcache_volume.name == 'my-reusable-volume'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    volume = docker_client.volumes.get("my-reusable-volume")

    labels = volume.attrs["Labels"]
    assert labels["creator"] == "pytest-docker-tools"
    assert labels["pytest-docker-tools.reusable"] == "True"
    assert labels["my-label"] == "testtesttest"


def test_reusable_reused(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            volume = docker_client.volumes.get("my-reusable-volume")
        except NotFound:
            return
        volume.remove()

    with pytest.raises(NotFound):
        docker_client.volumes.get("my-reusable-volume")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import volume",
                "memcache_volume = volume(",
                "    name='my-reusable-volume',",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_volume="\n".join(
            (
                "def test_session_1(memcache_volume):",
                "    assert memcache_volume.name == 'my-reusable-volume'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run1 = docker_client.volumes.get("my-reusable-volume")

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run2 = docker_client.volumes.get("my-reusable-volume")

    assert run1.id == run2.id


def test_reusable_stale(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            volume = docker_client.volumes.get("test_reusable_stale")
        except NotFound:
            return
        volume.remove()

    with pytest.raises(NotFound):
        docker_client.volumes.get("test_reusable_stale")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import volume",
                "memcache_volume = volume(",
                "    name='test_reusable_stale',",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_volume="\n".join(
            (
                "def test_session_1(memcache_volume):",
                "    assert memcache_volume.name == 'test_reusable_stale'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run1 = docker_client.volumes.get("test_reusable_stale")

    # Running again immediately shouldn't recreate the volume
    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    # This would explode if the volume had been removed
    run1.reload()

    # Add a label to the volume to make it stale
    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import volume",
                "memcache_volume = volume(",
                "    name='test_reusable_stale',",
                "    labels={'my-label': 'testtesttest'},",
                ")",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    # It should be replaced by a volume with labels on it
    run2 = docker_client.volumes.get("test_reusable_stale")
    run2.attrs["Labels"]["my-label"] == "testtesttest"


def test_reusable_stale_dependent_container(
    request, pytester: Pytester, docker_client: DockerClient
):
    def _cleanup():
        try:
            container = docker_client.containers.get(
                "test_reusable_stale_dependent_container_vol"
            )
            container.remove(force=True)
        except NotFound:
            pass

        try:
            volume = docker_client.volumes.get(
                "test_reusable_stale_dependent_container"
            )
            volume.remove()
        except NotFound:
            pass

    request.addfinalizer(_cleanup)

    with pytest.raises(NotFound):
        docker_client.volumes.get("test_reusable_stale_dependent_container")
        docker_client.containers.get("test_reusable_stale_dependent_container_vol")

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch, volume",
                "redis_image = fetch(repository='redis:latest')",
                "redis_volume = volume(",
                "    name='test_reusable_stale_dependent_container',",
                ")",
                "redis = container(",
                "    name='test_reusable_stale_dependent_container_vol',",
                "    image='{redis_image.id}',",
                "    volumes={'{redis_volume.name}': {'bind': '/data'}},",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_volume="\n".join(
            (
                "def test_session_1(redis):",
                "    assert redis.name == 'test_reusable_stale_dependent_container_vol'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run1 = docker_client.containers.get("test_reusable_stale_dependent_container_vol")

    # Running again immediately shouldn't recreate the container
    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    # This would explode if the container had been removed
    run1.reload()

    # Add a label to the volume to make it stale
    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch, volume",
                "redis_image = fetch(repository='redis:latest')",
                "redis_volume = volume(",
                "    name='test_reusable_stale_dependent_container',",
                "    labels={'my-label': 'testtesttest'},",
                ")",
                "redis = container(",
                "    name='test_reusable_stale_dependent_container_vol',",
                "    image='{redis_image.id}',",
                "    volumes={'{redis_volume.name}': {'bind': '/data'}},",
                ")",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run2 = docker_client.containers.get("test_reusable_stale_dependent_container_vol")
    assert run1.id != run2.id

    with pytest.raises(NotFound):
        run1.reload()
