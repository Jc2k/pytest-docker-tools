from pytest_docker_tools import container_fixture

mycontainer = container_fixture('test', 'redis')


def test_container_created(docker_client, mycontainer):
    print(mycontainer)
    assert False
