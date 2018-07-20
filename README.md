# pytest-docker-tools

This package contains some opinionated helpers for Dockerized integration
testing drive by `py.test`.

You define your fixtures in your `conftest.py`

```
from pytest_docker_tools import create_container, image_fixture


smtp_image = image_fixture('smtp_image')


@pytest.fixture(scope='function')
def smtp(request, docker_client, smtp_image):
    print('Creating smtp container')
    container = create_container(
        request,
        docker_client,
        smtp_image.id,
    )
    wait_for_port(container['container'], 25)
    return container
```
