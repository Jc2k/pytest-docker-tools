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


def test_set_own_labels(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            network = docker_client.networks.get("test_set_own_labels")
        except NotFound:
            return
        network.remove()

    with pytest.raises(NotFound):
        docker_client.networks.get("test_set_own_labels")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import network",
                "memcache_network = network(",
                "    name='test_set_own_labels',",
                "    labels={'my-label': 'testtesttest'}," ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_network="\n".join(
            (
                "def test_session_1(memcache_network):",
                "    assert memcache_network.name == 'test_set_own_labels'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    network = docker_client.networks.get("test_set_own_labels")
    assert network.attrs["Labels"] == {
        "creator": "pytest-docker-tools",
        "pytest-docker-tools.reusable": "True",
        "my-label": "testtesttest",
    }


def test_reusable_reused(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            network = docker_client.networks.get("test_reusable_reused")
        except NotFound:
            return
        network.remove()

    with pytest.raises(NotFound):
        docker_client.networks.get("test_reusable_reused")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import network",
                "memcache_network = network(",
                "    name='test_reusable_reused',",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_network="\n".join(
            (
                "def test_session_1(memcache_network):",
                "    assert memcache_network.name == 'test_reusable_reused'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run1 = docker_client.networks.get("test_reusable_reused")

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run2 = docker_client.networks.get("test_reusable_reused")

    assert run1.id == run2.id
