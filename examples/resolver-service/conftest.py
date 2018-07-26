import os
from http.client import HTTPConnection

import pytest
from pytest_docker_tools import build, container

fakedns_image = build(
    path=os.path.join(os.path.dirname(__file__), 'dns'),
)

fakedns = container(
    image='{fakedns_image.id}',
    environment={
        'DNS_EXAMPLE_COM__A': '127.0.0.1',
    }
)

apiserver_image = build(
    path=os.path.join(os.path.dirname(__file__), 'api'),
)


apiserver = container(
    image='{apiserver_image.id}',
    ports={
        '8080/tcp': None,
    },
    dns=['{fakedns.ips.primary}']
)


@pytest.fixture
def apiclient(apiserver):
    port = apiserver.ports['8080/tcp'][0]
    return HTTPConnection(f'localhost:{port}')
