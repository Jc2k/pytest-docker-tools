# pytest-docker-tools

This package contains some opinionated helpers for Dockerized integration
testing drive by `py.test`.

You can define your fixtures in your `conftest.py` or in the test module
where you are using them.

A simple example of a container built from an image with a volume attached:

```
from pytest_docker_tools import container_fixture, image_fixture, volume_fixture

container_fixture(
    'my_microservice',
    image('my_microservice_image', path='.'),
    volumes={
      volume_fixture('my_microservice_data'): {'bind': '/var/tmp'},
    }
)
```

Wherever possible the arguments to container_fixture mirror the arguments to the python docker libraries `run()` API.
