import os
import socket

from pytest_docker_tools import build, container, fetch
from pytest_docker_tools.utils import wait_for_callable

test_container_1_image = fetch(repository='redis:latest')

test_container_1 = container(
    image='{test_container_1_image.id}',
    ports={
        '6379/tcp': None,
    },
)

ipv6_folder = os.path.join(os.path.dirname(__file__), 'fixtures/ipv6')
ipv6_image = build(path=ipv6_folder)
ipv6 = container(
    image='{ipv6_image.id}',
    ports={
        '1234/udp': None,
    }
)


def test_container_created(docker_client, test_container_1):
    for c in docker_client.containers.list(ignore_removed=True):
        if c.id == test_container_1.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, 'Looks like we failed to start a container'


def test_container_ipv6(ipv6):
    addr = ipv6.get_addr('1234/udp')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b'msg', addr)

    wait_for_callable('Waiting for delivery confirmation', lambda: 'msg' in ipv6.logs())
