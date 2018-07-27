from pytest_docker_tools import container, fetch

test_container_1_image = fetch(repository='redis:latest')

test_container_1 = container(
    image='{test_container_1_image.id}',
    ports={
        '6379/tcp': None,
    },
)


def test_container_created(docker_client, test_container_1):
    for c in docker_client.containers.list(ignore_removed=True):
        if c.id == test_container_1.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, 'Looks like we failed to start a container'
