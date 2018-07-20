# pytest-docker-tools

This package contains some opinionated helpers for Dockerized integration
testing drive by `py.test`.

You can define your fixtures in your `conftest.py` or in the test module
where you are using them.

A simple example of a container built from an image with a volume attached:

```
from pytest_docker_tools.factories import *

container(
    'my_microservice',
    image('my_microservice_image', path='.'),
    volumes={
      volume('my_microservice_data'): {'bind': '/var/tmp'},
    }
)
```

Wherever possible the arguments to container_fixture mirror the arguments to the python docker libraries `run()` API.

You can create containers that depend on other containers:

```
from pytest_docker_tools.factories import *

container(
    'my_database',
    image('my_database_image', path='db'),
    volumes={
      volume('my_microservice_data'): {'bind': '/var/tmp'},
    }
)

container(
    'my_microservice',
    image('my_microservice_image', path='microservice'),
    environment={
      'DATABASE_IP': lambda my_database: my_database['ip'],
    }
)
```

Whenever you create a test that uses the `my_microservice` container it will also start a database container.
