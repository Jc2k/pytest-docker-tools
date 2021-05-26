import os
import socket

import pytest

from pytest_docker_tools import build, container, fetch, image
from pytest_docker_tools.utils import DOCKER_LABEL_REUSABLE_CONTAINER, wait_for_callable

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

reused_container = container(name="test_container_org")

ipv6_folder = os.path.join(os.path.dirname(__file__), "fixtures/ipv6")
ipv6_image = build(path=ipv6_folder)
ipv6 = container(
    image="{ipv6_image.id}",
    ports={
        "1234/udp": None,
    },
)


@pytest.fixture()
def enable_container_reuse(request):
    request.config.option.reuse_containers = True
    yield
    request.config.option.reuse_containers = False


def test_container_created(docker_client, test_container_1):
    for c in docker_client.containers.list(ignore_removed=True):
        if c.id == test_container_1.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, "Looks like we failed to start a container"


def test_container_ipv6(ipv6):
    addr = ipv6.get_addr("1234/udp")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"msg", addr)

    wait_for_callable("Waiting for delivery confirmation", lambda: "msg" in ipv6.logs())


def test_container_label(docker_client, test_container_1):
    for c in docker_client.containers.list(ignore_removed=True):
        assert "container-creator" in c.attrs["Config"]["Labels"].keys()
        assert (
            DOCKER_LABEL_REUSABLE_CONTAINER
            in c.attrs["Config"]["Labels"].keys()
        )
        assert c.attrs["Config"]["Labels"]["container-creator"] == "pytest-docker-tools"

        break
    else:
        assert False, "Looks like we failed to start a container"


def test_container_reuse_create(
    enable_container_reuse, docker_client, original_container_1, reused_container
):
    assert original_container_1.id == reused_container.id
    for c in docker_client.containers.list(ignore_removed=True):
        if c.id == original_container_1.id:
            c.remove(force=True)
