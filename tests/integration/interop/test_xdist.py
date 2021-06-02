from _pytest.pytester import Pytester
from docker.client import DockerClient
from docker.errors import NotFound
import pytest


def test_xdist_named_container(
    request, pytester: Pytester, docker_client: DockerClient
):
    def _cleanup():
        try:
            for i in range(2):
                container = docker_client.containers.get(f"my-named-container-gw{i}")
        except NotFound:
            return
        container.remove(force=True)

    with pytest.raises(NotFound):
        for i in range(2):
            docker_client.containers.get(f"my-named-container-gw{i}")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch",
                "memcache_image = fetch(repository='memcached:latest')",
                "memcache = container(",
                "    name='my-named-container-{worker_id}',",
                "    image='{memcache_image.id}',",
                "    scope='session',",
                "    ports={",
                "        '11211/tcp': None,",
                "    },",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_named_container="\n".join(
            (
                "import socket",
                "def test_session_1(memcache):",
                "    sock = socket.socket()",
                "    sock.connect(('127.0.0.1', memcache.ports['11211/tcp'][0]))",
                "    sock.close()",
                "def test_session_2(memcache):",
                "    sock = socket.socket()",
                "    sock.connect(('127.0.0.1', memcache.ports['11211/tcp'][0]))",
                "    sock.close()",
            )
        )
    )

    result = pytester.runpytest("-n", "2")
    result.assert_outcomes(passed=2)

    with pytest.raises(NotFound):
        for i in range(2):
            docker_client.containers.get(f"my-named-container-gw{i}")


def test_xdist_reusable(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            for i in range(2):
                container = docker_client.containers.get(f"my-reusable-container-gw{i}")
                container.remove(force=True)
        except NotFound:
            return

    with pytest.raises(NotFound):
        for i in range(2):
            docker_client.containers.get(f"my-reusable-container-gw{i}")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch",
                "memcache_image = fetch(repository='memcached:latest')",
                "memcache = container(",
                "    name='my-reusable-container-{worker_id}',",
                "    image='{memcache_image.id}',",
                "    scope='session',",
                "    ports={",
                "        '11211/tcp': None,",
                "    },",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_container="\n".join(
            (
                "import socket",
                "def test_session_1(memcache):",
                "    sock = socket.socket()",
                "    sock.connect(('127.0.0.1', memcache.ports['11211/tcp'][0]))",
                "    sock.close()",
                "def test_session_2(memcache):",
                "    sock = socket.socket()",
                "    sock.connect(('127.0.0.1', memcache.ports['11211/tcp'][0]))",
                "    sock.close()",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers", "-n", "2")
    result.assert_outcomes(passed=2)

    run1a = docker_client.containers.get("my-reusable-container-gw0")
    run1b = docker_client.containers.get("my-reusable-container-gw1")
    assert run1a.id != run1b.id

    result = pytester.runpytest("--reuse-containers", "-n", "2")
    result.assert_outcomes(passed=2)

    run2a = docker_client.containers.get("my-reusable-container-gw0")
    run2b = docker_client.containers.get("my-reusable-container-gw1")

    assert run1a.id == run2a.id
    assert run1b.id == run2b.id
