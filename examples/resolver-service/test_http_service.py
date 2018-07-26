import json


def test_api_server(apiclient):
    apiclient.request('GET', '/')
    response = apiclient.getresponse()
    assert response.status == 200
    assert json.loads(response.read()) == {'result': '127.0.0.1'}
