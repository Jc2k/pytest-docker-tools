from _pytest.pytester import Pytester
from docker.errors import NotFound
import pytest

from pytest_docker_tools import volume

test_volume_1 = volume()


def test_volume1_created(docker_client, test_volume_1):
    for v in docker_client.volumes.list():
        if v.id == test_volume_1.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, "Looks like we failed to create a volume"


def test_reusable_must_be_named(request, pytester: Pytester, docker_client):
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


def test_reusable_reused(request, pytester: Pytester, docker_client):
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
