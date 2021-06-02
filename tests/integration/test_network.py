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


def test_reusable_conflict(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            network = docker_client.networks.get("test_reusable_conflict")
        except NotFound:
            return
        network.remove()

    request.addfinalizer(_cleanup)

    with pytest.raises(NotFound):
        docker_client.networks.get("test_reusable_conflict")

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import network",
                "memcache_network = network(",
                "    name='test_reusable_conflict'",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_network="\n".join(
            (
                "def test_session_1(memcache_network):",
                "    assert memcache_network.name == 'test_reusable_conflict'",
            )
        )
    )

    docker_client.networks.create(name="test_reusable_conflict")

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=0, errors=1)
    result.stdout.re_match_lines([".*does not appear to be a reusable network"])


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
                "    labels={'my-label': 'testtesttest'},",
                ")",
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
    labels = network.attrs["Labels"]
    assert labels["creator"] == "pytest-docker-tools"
    assert labels["pytest-docker-tools.reusable"] == "True"
    assert labels["my-label"] == "testtesttest"


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


def test_reusable_stale(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            network = docker_client.networks.get("test_reusable_stale")
        except NotFound:
            return
        network.remove()

    with pytest.raises(NotFound):
        docker_client.networks.get("test_reusable_stale")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import network",
                "memcache_network = network(",
                "    name='test_reusable_stale',",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_network="\n".join(
            (
                "def test_session_1(memcache_network):",
                "    assert memcache_network.name == 'test_reusable_stale'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run1 = docker_client.networks.get("test_reusable_stale")

    # Running again immediately shouldn't recreate the network
    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)
    # This would explode if the network had been removed
    run1.reload()

    # Add a label to the network to make it stale
    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import network",
                "memcache_network = network(",
                "    name='test_reusable_stale',",
                "    labels={'my-label': 'testtesttest'}",
                ")",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    # It should be replaced
    run2 = docker_client.networks.get("test_reusable_stale")
    assert run1.id != run2.id

    with pytest.raises(NotFound):
        run1.reload()


def test_reusable_stale_dependent_container(
    request, pytester: Pytester, docker_client: DockerClient
):
    def _cleanup():
        try:
            container = docker_client.containers.get(
                "test_reusable_stale_dependent_container_net"
            )
            container.remove(force=True)
        except NotFound:
            pass

        try:
            network = docker_client.networks.get(
                "test_reusable_stale_dependent_container"
            )
            network.remove()
        except NotFound:
            pass

    request.addfinalizer(_cleanup)

    with pytest.raises(NotFound):
        docker_client.networks.get("test_reusable_stale_dependent_container")
        docker_client.containers.get("test_reusable_stale_dependent_container_net")

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch, network",
                "redis_image = fetch(repository='redis:latest')",
                "redis_network = network(",
                "    name='test_reusable_stale_dependent_container',",
                ")",
                "redis = container(",
                "    name='test_reusable_stale_dependent_container_net',",
                "    image='{redis_image.id}',",
                "    network='{redis_network.name}',",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_network="\n".join(
            (
                "def test_session_1(redis):",
                "    assert redis.name == 'test_reusable_stale_dependent_container_net'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run1 = docker_client.containers.get("test_reusable_stale_dependent_container_net")

    # Running again immediately shouldn't recreate the container
    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    # This would explode if the container had been removed
    run1.reload()

    # Add a label to the network to make it stale
    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch, network",
                "redis_image = fetch(repository='redis:latest')",
                "redis_network = network(",
                "    name='test_reusable_stale_dependent_container',",
                "    labels={'my-label': 'testtesttest'},",
                ")",
                "redis = container(",
                "    name='test_reusable_stale_dependent_container_net',",
                "    image='{redis_image.id}',",
                "    network='{redis_network.name}',",
                ")",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run2 = docker_client.containers.get("test_reusable_stale_dependent_container_net")
    assert run1.id != run2.id

    with pytest.raises(NotFound):
        run1.reload()


def test_reusable_conflicting_container(
    request, pytester: Pytester, docker_client: DockerClient
):
    def _cleanup():
        try:
            container = docker_client.containers.get(
                "test_reusable_conflicting_container_net"
            )
            container.remove(force=True)
        except NotFound:
            pass

        try:
            network = docker_client.networks.get("test_reusable_conflicting_container")
            network.remove()
        except NotFound:
            pass

    request.addfinalizer(_cleanup)

    with pytest.raises(NotFound):
        docker_client.networks.get("test_reusable_conflicting_container")
        docker_client.containers.get("test_reusable_conflicting_container_net")

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch, network",
                "redis_network = network(",
                "    name='test_reusable_conflicting_container',",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_network="\n".join(
            (
                "def test_session_1(redis_network):",
                "    assert redis_network.name == 'test_reusable_conflicting_container'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    # At this stage our network exists and we are going to create a container that
    # *isn't managed by pytest-docker-tools*
    # We should refuse to delete that container even when the network is stale
    docker_client.images.pull(repository="memcached:latest")
    docker_client.containers.create(
        name="test_reusable_conflicting_container_net",
        image="memcached:latest",
        network="test_reusable_conflicting_container",
    )

    # Add a label to the network to make the network stale
    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch, network",
                "redis_network = network(",
                "    name='test_reusable_conflicting_container',",
                "    labels={'my-label': 'testtesttest'},",
                ")",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=0, errors=1)
    result.stdout.re_match_lines([".*is connected to a non-reusable container.*"])
