import logging
import os
import socket

from _pytest.pytester import Pytester
from docker.client import DockerClient
from docker.errors import NotFound
import pytest

from pytest_docker_tools import build, container, fetch, image
from pytest_docker_tools.utils import LABEL_REUSABLE, wait_for_callable

logger = logging.getLogger(__name__)

test_container_1_image = fetch(repository="redis:latest")
test_container_1_same_image = image(name="redis:latest")

test_container_1 = container(
    image="{test_container_1_image.id}",
    ports={
        "6379/tcp": None,
    },
    name="test_container",
)

original_container_1 = container(
    image="{test_container_1_same_image.id}",
    ports={
        "6379/tcp": None,
    },
    name="test_container_org",
)

ipv6_folder = os.path.join(os.path.dirname(__file__), "fixtures/ipv6")
ipv6_image = build(path=ipv6_folder)
ipv6 = container(
    image="{ipv6_image.id}",
    ports={
        "1234/udp": None,
    },
)


def test_container_created(docker_client: DockerClient, test_container_1):
    for c in docker_client.containers.list(ignore_removed=True):
        if c.id == test_container_1.id:
            assert "creator" in c.attrs["Config"]["Labels"].keys()
            assert LABEL_REUSABLE in c.attrs["Config"]["Labels"].keys()
            assert c.attrs["Config"]["Labels"]["creator"] == "pytest-docker-tools"
            # Looks like we managed to start one!
            break
    else:
        assert False, "Looks like we failed to start a container"


def test_container_ipv6(ipv6):
    addr = ipv6.get_addr("1234/udp")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"msg", addr)

    wait_for_callable("Waiting for delivery confirmation", lambda: "msg" in ipv6.logs())


def test_reusable_conflict(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            container = docker_client.containers.get("test_reusable_conflict")
        except NotFound:
            return
        container.remove(force=True)

    request.addfinalizer(_cleanup)

    with pytest.raises(NotFound):
        docker_client.containers.get("test_reusable_conflict")

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch",
                "memcache_image = fetch(repository='memcached:latest')",
                "memcache = container(",
                "    name='test_reusable_conflict',",
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
                "def test_session_1(memcache):",
                "    assert memcache.name == 'test_reusable_conflict'",
            )
        )
    )

    docker_client.images.pull(repository="memcached:latest")
    docker_client.containers.create(
        name="test_reusable_conflict", image="memcached:latest"
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=0, errors=1)
    result.stdout.re_match_lines([".*does not appear to be a reusable container"])


def test_reusable_must_be_named(
    request, pytester: Pytester, docker_client: DockerClient
):
    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch",
                "memcache_image = fetch(repository='memcached:latest')",
                "memcache = container(",
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
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=0, errors=1)


def test_set_own_labels(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            container = docker_client.containers.get("test_set_own_labels")
        except NotFound:
            return
        container.remove(force=True)

    with pytest.raises(NotFound):
        docker_client.containers.get("test_set_own_labels")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch",
                "memcache_image = fetch(repository='memcached:latest')",
                "memcache = container(",
                "    name='test_set_own_labels',",
                "    image='{memcache_image.id}',",
                "    scope='session',",
                "    labels={'my-label': 'testtesttest'},",
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
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    container = docker_client.containers.get("test_set_own_labels")
    labels = container.attrs["Config"]["Labels"]
    assert labels["creator"] == "pytest-docker-tools"
    assert labels["pytest-docker-tools.reusable"] == "True"
    assert labels["my-label"] == "testtesttest"


def test_reusable_reused(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            container = docker_client.containers.get("test_reusable_reused")
        except NotFound:
            return
        container.remove(force=True)

    with pytest.raises(NotFound):
        docker_client.containers.get("test_reusable_reused")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch",
                "memcache_image = fetch(repository='memcached:latest')",
                "memcache = container(",
                "    name='test_reusable_reused',",
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
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run1 = docker_client.containers.get("test_reusable_reused")

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    run2 = docker_client.containers.get("test_reusable_reused")

    assert run1.id == run2.id


def test_reusable_stale(request, pytester: Pytester, docker_client: DockerClient):
    def _cleanup():
        try:
            container = docker_client.containers.get("test_reusable_stale")
        except NotFound:
            return
        container.remove(force=True)

    with pytest.raises(NotFound):
        docker_client.containers.get("test_reusable_stale")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch",
                "cache_image = fetch(repository='memcached:latest')",
                "cache = container(",
                "    name='test_reusable_stale',",
                "    image='{cache_image.id}',",
                "    scope='session',",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_container="\n".join(
            (
                "import socket",
                "def test_session_1(cache):",
                "    assert cache.name == 'test_reusable_stale'",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    # Make sure container persisted beyond the end of the test
    run1 = docker_client.containers.get("test_reusable_stale")

    # If we re-run straight away the container shouldn't be deleted
    # This is just to make sure that the test case isn't broken
    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)
    run1.reload()

    # Switching memcache to redis should force a replacement
    # of a stale container
    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import container, fetch",
                "cache_image = fetch(repository='redis:latest')",
                "cache = container(",
                "    name='test_reusable_stale',",
                "    image='{cache_image.id}',",
                "    scope='session',",
                ")",
            )
        )
    )

    result = pytester.runpytest("--reuse-containers")
    result.assert_outcomes(passed=1)

    # There should be a new container
    run2 = docker_client.containers.get("test_reusable_stale")
    assert run1.id != run2.id

    # Old container should be gone
    with pytest.raises(NotFound):
        run1.reload()


def test_container_env_by_fixtureref(
    request, pytester: Pytester, docker_client: DockerClient
):
    def _cleanup():
        try:
            container = docker_client.containers.get("test_env_by_fixture")
        except NotFound:
            return
        container.remove(force=True)

    with pytest.raises(NotFound):
        docker_client.containers.get("test_env_by_fixture")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "import pytest",
                "from pytest_docker_tools import container, fetch, fxtr",
                "@pytest.fixture(scope='session')",
                "def memcached_env():",
                "    yield {'Foo': 'Bar'}",
                "cache_image = fetch(repository='memcached:latest')",
                "cache = container(",
                "    name='test_env_by_fixture',",
                "    image='{cache_image.id}',",
                "    environment=fxtr('memcached_env'),",
                "    scope='session'",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_container="\n".join(
            (
                "def test_session_1(cache):",
                "    assert cache.name == 'test_env_by_fixture'",
                "    custom_env = [env for env in cache.attrs['Config']['Env'] if 'Foo' in env]",
                "    assert custom_env",
                "    assert custom_env[0] == 'Foo=Bar'",
            )
        )
    )

    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


def test_container_env_by_lambda(
    request, pytester: Pytester, docker_client: DockerClient
):
    def _cleanup():
        try:
            container = docker_client.containers.get("test_env_by_fixture")
        except NotFound:
            return
        container.remove(force=True)

    with pytest.raises(NotFound):
        docker_client.containers.get("test_env_by_fixture")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "import pytest",
                "from pytest_docker_tools import container, fetch",
                "@pytest.fixture(scope='session')",
                "def memcached_env():",
                "    yield {'Foo': 'Bar'}",
                "cache_image = fetch(repository='memcached:latest')",
                "cache = container(",
                "    name='test_env_by_fixture',",
                "    image='{cache_image.id}',",
                "    environment=lambda memcached_env: memcached_env,",
                "    scope='session'",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_container="\n".join(
            (
                "def test_session_1(cache):",
                "    assert cache.name == 'test_env_by_fixture'",
                "    custom_env = [env for env in cache.attrs['Config']['Env'] if 'Foo' in env]",
                "    assert custom_env",
                "    assert custom_env[0] == 'Foo=Bar'",
            )
        )
    )

    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


def test_container_env_by_fixture(
    request, pytester: Pytester, docker_client: DockerClient
):
    def _cleanup():
        try:
            container = docker_client.containers.get("test_env_by_fixture")
        except NotFound:
            return
        container.remove(force=True)

    with pytest.raises(NotFound):
        docker_client.containers.get("test_env_by_fixture")

    request.addfinalizer(_cleanup)

    pytester.makeconftest(
        "\n".join(
            (
                "import pytest",
                "from pytest_docker_tools import container, fetch",
                "@pytest.fixture(scope='session')",
                "def memcached_env():",
                "    yield {'Foo': 'Bar'}",
                "cache_image = fetch(repository='memcached:latest')",
                "cache = container(",
                "    name='test_env_by_fixture',",
                "    image='{cache_image.id}',",
                "    environment=memcached_env,",
                "    scope='session'",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_container="\n".join(
            (
                "def test_session_1(cache):",
                "    assert cache.name == 'test_env_by_fixture'",
                "    custom_env = [env for env in cache.attrs['Config']['Env'] if 'Foo' in env]",
                "    assert custom_env",
                "    assert custom_env[0] == 'Foo=Bar'",
            )
        )
    )

    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
