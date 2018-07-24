# pytest-docker-tools

You have written a software application (in any language) and have packaged in as a Docker image. Now you want to smoke test the built image or do some integration testing with other containers before releasing it. You:

 * want to reason about your environment in a similar way to a `docker-compose.yml`
 * want the environment to be automatically created and destroyed as tests run
 * don't want to have to write loads of boilerplate code for creating the test environment
 * want to be able to run the tests in parallel
 * want the tests to be reliable

`pytest-docker-tools` is a set of opinionated helpers for creating `py.test` fixtures for your smoke testing and integration testing needs. It strives to keep your environment definition declarative, like a docker-compose.yml. It embraces py.test fixture overloading. It tries not to be too magical.

The man interface provided by this library is a set of 'fixture factories'. It provides a 'best in class' implementation of a fixture, and then allows you to treat it as a template - injecting your own configuration declaratively. You can define your fixtures in your `conftest.py` and access them from all your tests, and you can override them as needed in individual test modules.

The API is straightforward and implicitly captures the interdependencies in the specification. For example, here is how it might look if you were building out a microservice with a redis backend:

```
from pytest_docker_tools import *

my_image = fetch('redis:latest')

my_image_2 = build(
  path='db'
)

my_data = volume()

my_microservice_backend = container(
    image='{my_image.id}',
    volumes={
      '{my_data.id}': {'bind': '/var/tmp'},
    }
)

my_microservice = container(
    image='{my_image_2.id}',
    environment={
      'DATABASE_IP': '{mydatabase.ips.primary}',
    },
    ports={
      '3679/tcp': None,
    }
)
```

You can now create a test that exercises your microservice:

```
def test_my_frobulator(my_microservice):
    socket = socket.socket()
    socket.connect('127.0.0.1', my_microservice.ports['3679/tcp'][0])
    ....
```

In this example all the dependencies will be resolved in order and once per session:

 * The latest redis:latest will be fetched
 * A container image will be build from the `Dockerfile` in the `db` folder.

Then once per test:

 * A new volume will be created
 * A new 'backend' container will be created from `redis:latest`. It will be attached to the new volume.
 * A new 'frontend' container will be created from the freshly built container. It will be given the IP if the backend via an environment variable. Port 3679 in the container will be exposed as an ephemeral port on the host.

The test can then run and access the container via its ephemeral high port. At the end of the test the environment will be thrown away.

If the test fails the `docker logs` output from each container will be captured and added to the test output.


## Parallelism

Integration and smoke tests are often slow, but a lot of time is spent waiting. So running tests in parallel is a great way to speed them up. `pytest-docker-tools` avoids creating resource names that could collide. This means its a great fit for use with `pytest-xdist`.

Here is a bare minimum example that just tests creating and destroying 100 instances of a redis fixture that runs under xdist. Create a `test_xdist.py` plugin:

```
import pytest
from pytest_docker_tools import container, fetch

my_redis_image = fetch('redis:latest')

my_redis = container(
    image='{my_redis_image.id}',
)


@pytest.mark.parametrize("i", list(range(100)))
def test_xdist(i, my_redis):
    assert my_redis.status == "running"
```

And invoke it with:

```
pytest test_xdist.py -n auto
```

It will create a worker per core and run the tests in parallel:

```
===================================== test session starts ======================================
platform darwin -- Python 3.6.5, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: ~/pytest-docker-tools, inifile:
plugins: xdist-1.22.2, forked-0.2, docker-tools-0.0.2
gw0 [100] / gw1 [100] / gw2 [100] / gw3 [100] / gw4 [100] / gw5 [100] / gw6 [100] / gw7 [100]
scheduling tests via LoadScheduling
......................................................................................... [ 82%]
...........                                                                              [100%]
================================= 100 passed in 70.08 seconds ==================================
```


## Factories Reference

### Containers

To create a container in your tests use the `container` fixture factory.

```
from pytest_docker_tools import container

my_microservice_backend = container(image='redis:latest')
```

The default scope for this factory is `function`. This means a new container will be created for each test.

The `container` fixture factory supports all parameters that can be passed to the docker-py `run` method. See [here](https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.run) for them all.

Any variables are interpolated against other defined fixtures. This means that a fixture can depend on other fixtures, and they will be built and run in order.

For example:

```
from pytest_docker_tools import container, fetch

my_microservice_backend_image = fetch('redis:latest')
my_microservice_backend = container(image='{my_microservice_backend_image.id}')
```

This will fetch the latest `redis:latest` first, and then run a container from the exact image that was pulled. Note that if you don't use `build` or `fetch` to prepare a Docker image then the tag or hash that you specify must already exist on the host where you are running the tests. There is no implicit fetching of Docker images.

The container will be automatically deleted after the test has finished.


#### Ip Addresses

If your container is only attached to a single network you can get its Ip address through a helper property on the container object:

```
my_service = container(
  image='{my_image.id}',
)

def test_get_service_ip(my_service):
    print(my_service.ips.primary)
```

If you want to look up its ip address by network you can also access it more specifically:

```
def test_get_service_ip(my_network, my_service):
    print(my_service.ips[my_network])
```

#### Ports

The factory takes the same port arguments as the official Python Docker API. We recommend using the ephemeral high ports syntax:

```
my_service = container(
  image='{my_image.id}',
  ports={'3275/tcp': None}
)
```

Docker will map port 3275 in the container to a random port on your host. In order to access it from your tests you can get the bound port from the container instance:

```
def test_connect_my_service(my_service):
    print(my_service.ports['3275/tcp'][0])
```


#### Logs

You can inspect the logs of your container with the logs method:

```
def test_logs(my_redis_service):
    assert 'oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo' in my_redis_service.logs()
```


### Images

To pull an image from your default repository use the `fetch` fixture factory. To build an image from local source use the `build` fixture factory.

```
from pytest_docker_tools import build, fetch

my_image = fetch('redis:latest')

my_image_2 = build(
  path='db'
)
```

The default scope for this factory is `session`. This means the fixture will only build or fetch once per py.test invocation. The fixture will not be triggered until a test (or other fixture) tries to use it. This means you won't waste time building an image if you aren't running the test that uses it.


### Networks

By default any containers you create with the `container()` fixture factory will run on your default docker network. You can create a dedicated network for your test with the `network()` fixture factory.

```
from pytest_docker_tools import network

frontend_network = network()
```

The default scope for this factory is `function`. This means a new network will be created for each test that is executed.

The network will be removed after the test using it has finished.


#### Volumes

In the ideal case a Docker container instance is read only. No data inside the container is written to, if it is its to a volume. If you are testing that your service can run read only you might want to mount a rw volume. You can use the `volume()` fixture factory to create a Docker volume with a lifecycle tied to your tests.

```
from pytest_docker_tools import volume

backend_storage = volume()
```

The default scope for this factory is `function`. This means a new volume will be created for each test that is executed. The volume will be removed after the test using it has finished.
