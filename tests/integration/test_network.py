from _pytest.pytester import Pytester
from docker.client import DockerClient
from docker.errors import NotFound
import pytest

from pytest_docker_tools import network

test_network_1 = network()


def test_network_1_created(docker_client: DockerClient, test_network_1):
    for n in docker_client.networks.list():
        if n.id == test_network_1.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, "Looks like we failed to create a network"


def test_reusable_must_be_named(
    request, pytester: Pytester, docker_client: DockerClient
):
    with pytest.raises(NotFound):
        docker_client.networks.get("my-reusable-network")

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import network",
                "memcache_network = network(",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_network="\n".join(
            (
                "def test_session_1(memcache_network):",
                "    assert memcache_network.name == 'my-reusable-network'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=0, errors=1)

    with pytest.raises(NotFound):
        docker_client.networks.get("my-reusable-network")


def test_reusable_reused(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            network = docker_client.networks.get("my-reusable-network")
        except NotFound:
            return
        network.remove()

    with pytest.raises(NotFound):
        docker_client.networks.get("my-reusable-network")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import network",
                "memcache_network = network(",
                "    name='my-reusable-network',",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_network="\n".join(
            (
                "def test_session_1(memcache_network):",
                "    assert memcache_network.name == 'my-reusable-network'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run1 = docker_client.networks.get("my-reusable-network")

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run2 = docker_client.networks.get("my-reusable-network")

    assert run1.id == run2.id
