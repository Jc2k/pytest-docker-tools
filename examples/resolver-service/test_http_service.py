import json
from http.client import HTTPConnection


def test_api_server(apiserver):
    port = apiserver.ports['8080/tcp'][0]
    hcl = HTTPConnection(f'localhost:{port}')
    hcl.request('GET', '/')
    response = hcl.getresponse()
    assert response.status == 200
    assert json.loads(response.read()) == {'result': '127.0.0.1'}
