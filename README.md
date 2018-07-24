# pytest-docker-tools

You have written a software application (in any language) and have packaged in as a Docker image. Now you want to smoke test the built image or do some integration testing with other containers before releasing it. You:

 * want to reason about your environment in a similar way to a `docker-compose.yml`
 * want the environment to be automatically created and destroyed as tests run
 * don't want to have to write loads of boilerplate code for creating the test environment
 * want to be able to run the tests in parallel
 * want the tests to be reliable

`pytest-docker-tools` is a set of opinionated helpers for creating `py.test` fixtures for your smoke testing and integration testing needs. It strives to keep your environment definition declarative, like a docker-compose.yml. It embraces py.test fixture overloading. It tries not to be too magical.

The main interface provided by this library is a set of 'fixture factories'. It provides a 'best in class' implementation of a fixture, and then allows you to treat it as a template - injecting your own configuration declaratively. You can define your fixtures in your `conftest.py` and access them from all your tests, and you can override them as needed in individual test modules.

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

 * The latest `redis:latest` will be fetched
 * A container image will be build from the `Dockerfile` in the `db` folder.

Then once per test:

 * A new volume will be created
 * A new 'backend' container will be created from `redis:latest`. It will be attached to the new volume.
 * A new 'frontend' container will be created from the freshly built container. It will be given the IP if the backend via an environment variable. Port 3679 in the container will be exposed as an ephemeral port on the host.

The test can then run and access the container via its ephemeral high port. At the end of the test the environment will be thrown away.

If the test fails the `docker logs` output from each container will be captured and added to the test output.


## Parallelism

Integration and smoke tests are often slow, but a lot of time is spent waiting. So running tests in parallel is a great way to speed them up. `pytest-docker-tools` avoids creating resource names that could collide. It also makes it easy to not care what port your service is bound to. This means its a great fit for use with `pytest-xdist`.

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

Any string variables are interpolated against other defined fixtures. This means that a fixture can depend on other fixtures, and they will be built and run in order.

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


## Fixtures

### docker_client

The `docker_client` fixture returns an instance of the official docker client.

```
def test_container_created(docker_client, test_container_1):
    for c in docker_client.containers.list(ignore_removed=True):
        if c.id == test_container_1.id:
            # Looks like we managed to start one!
            break
    else:
        assert False, 'Looks like we failed to start a container'
```

Take care when using the `docker_client` directly:

 * Obviously resources created imperatively via the API won't be removed at the end of the test automatically
 * It's easy to break xdist compatibility
   * Always use `ignore_removed` with `docker_client.containers.list()` - it is racy without
   * It's easy to find other instances of the resources you are working with (created in other workers). Be mindful of this!
 * Don't take destructive action - someone could be running tests on a machine with other (non-test) containers running, collateral damage is easy and should be avoided.

This is the fixture used by our fixture factories. This means if you define a `docker_client` fixture of your own then the tests will use that instead.


## Tips and tricks

### Client fixtures

You will probably want to create an API client for the service you are testing.

```
import hpfeeds
import pytest
from pytest_docker_tools import container, fetch


hpfeeds_broker_image = fetch('jc2k/hpfeeds3-broker:later')

hpfeeds_broker = container(
    image='{hpfeeds_broker_image.id}',
    environment={
        'HPFEEDS_TEST_SECRET': 'test',
        'HPFEEDS_TEST_SUBCHANS': 'test',
        'HPFEEDS_TEST_PUBCHANS': 'test',
    },
    command=[
        '/app/bin/hpfeeds-broker',
        '--bind=0.0.0.0:20000',
        # Read user creds from environment variables
        '--auth=env',
    ],
    ports={
        '20000/tcp': None,
    },
)

def hpfeeds_client(hpfeeds_broker):
    client = hpfeeds.new(
        '127.0.0.1',
        hpfeeds_broker.ports['20000/tcp'][0],
        'test',
        'test',
    )

    request.addfinalizer(client.close)
    request.addfinalizer(client.stop)

    return client


def test_send_message(hpfeeds_client):
    hpfeeds_client.publish('test', b'DATA DATA DATA')
```

In this example, any test that uses the `hpfeeds_client` fixture will get a properly configure client connected to a broker running in a Docker container on an ephemeral high port. When the test finishes the client will cleanly disconnect, and the docker container will be thrown away.


### Fixture overloading

Complicated environments can be defined with fixture factories. They form a directed acyclic graph. By using fixture overloading it is possible to (in the context of a single test module) replace a node in that dependency graph without having to redefine the entire environment.

#### Replacing a container fixture without having to redefine its dependents

You can define a fixture in your `conftest.py`:

```
from pytest_docker_tools import *


redis_image = fetch('redis:latest')
api_server_image = build(path='db')

redis = container(
    image='{redis_image.id}',
)

api_server = container(
    image='{api_server_image.id}',
    environment={
      'DATABASE_IP': '{redis.ips.primary}',
    },
    ports={
      '8080/tcp': None,
    }
)
```

You can then overload these fixtures in your test modules. For example, if redis had a magic replication feature and you want to test for an edge case with your API you could in your `test_magic_rep.py`:

```
import socket

from pytest_docker_tools import *


redis = container(
  image='{redis_image.id}',
  environment={
    'REDIS_MAGIC_REP': '1',
  }
)


def test_magic_rep(api_server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', api_server.ports['8080/tcp'][0]))
    sock.close()
```

Here we have redefined the redis container locally in `test_magic_rep.py`. It is able to use the `redis_image` fixture we defined in `conftest.py`. More crucially though, in `test_magic_rep.py` when we use the core `api_server` fixture it actually pulls in the local definition of `redis` and not the one from `conftest.py`! You don't have to redefine anything else. It just works.


#### Injecting fixture configuration through fixtures

You can pull in normal py.test fixtures from your fixture factory too. This means we can use fixture overloading and pass in config. In your `conftest.py`:

```
import pytest
from pytest_docker_tools import *


redis_image = fetch('redis:latest')
api_server_image = build(path='db')

redis = container(
    image='{redis_image.id}',
)

api_server = container(
    image='{api_server_image.id}',
    environment={
      'DATABASE_IP': '{redis.ips.primary}',
      'AUTHENTICATION_BACKEND': '{authentication_backend}'
    },
    ports={
      '8080/tcp': None,
    }
)


@pytest.fixture
def authentication_backend():
    return 'memory'
```

Your test can now inject a different authentication backend by overloading the `authentication_backend` fixture in your 'test_auth_sqlite.py' module:

```
import socket

import pytest


@pytest.fixture
def authentication_backend():
    return 'sqlite'


def test_magic_rep(api_server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', api_server.ports['8080/tcp'][0]))
    sock.close()
```

Your `api_server` container (and its `redis` backend) will be built as normal, only in this one test module it will use its sqlite backend.


### Fixture parameterisation

You can create parameterisation fixtures. Perhaps you wan to run all your `api_server` tests against both of your authentication backends. In your `conftest.py`:

```
import pytest
from pytest_docker_tools import *


redis_image = fetch('redis:latest')
api_server_image = build(path='db')

redis = container(
    image='{redis_image.id}',
)

api_server_memory = container(
    image='{api_server_image.id}',
    environment={
      'DATABASE_IP': '{redis.ips.primary}',
      'AUTHENTICATION_BACKEND': 'memory'
    },
    ports={
      '8080/tcp': None,
    }
)

api_server_sqlite = container(
    image='{api_server_image.id}',
    environment={
      'DATABASE_IP': '{redis.ips.primary}',
      'AUTHENTICATION_BACKEND': 'sqlite'
    },
    ports={
      '8080/tcp': None,
    }
)


@pytest.fixture(scope='function', params=['api_server_memory', 'api_server_sqlite'])
def apiserver(request):
    return request.getfixturevalue(request.param)
```

Then in your test:

```
def test_list_users(apiserver):
    pass
```

This test will be invoked twice - once against the memory backend, and once against the sqlite backend.
