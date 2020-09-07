# pytest-docker-tools

You have written a software application (in any language) and have packaged in as a Docker image. Now you want to smoke test the built image or do some integration testing with other containers before releasing it. You:

 * want to reason about your environment in a similar way to a `docker-compose.yml`
 * want the environment to be automatically created and destroyed as tests run
 * don't want to have to write loads of boilerplate code for creating the test environment
 * want to be able to run the tests in parallel
 * want the tests to be reliable

`pytest-docker-tools` is a set of opinionated helpers for creating `py.test` fixtures for your smoke testing and integration testing needs. It strives to keep your environment definition declarative, like a docker-compose.yml. It embraces py.test fixture overloading. It tries not to be too magical.

The main interface provided by this library is a set of 'fixture factories'. It provides a 'best in class' implementation of a fixture, and then allows you to treat it as a template - injecting your own configuration declaratively. You can define your fixtures in your `conftest.py` and access them from all your tests, and you can override them as needed in individual test modules.

The API is straightforward and implicitly captures the interdependencies in the specification. For example, here is how it might look if you were building out a microservice and wanted to point its DNS and a mock DNS server:

```python
# conftest.py

from http.client import HTTPConnection

import pytest
from pytest_docker_tools import build, container

fakedns_image = build(
    path='examples/resolver-service/dns',
)

fakedns = container(
    image='{fakedns_image.id}',
    environment={
        'DNS_EXAMPLE_COM__A': '127.0.0.1',
    }
)

apiserver_image = build(
    path='examples/resolver-service/api',
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
```

You can now create a test that exercises your microservice:

```python
# test_smoketest.py

import socket

def test_my_frobulator(apiserver):
    sock = socket.socket()
    sock.connect(('127.0.0.1', apiserver.ports['8080/tcp'][0]))


def test_my_frobulator_works_after_restart(apiserver):
    apiserver.restart()

    sock = socket.socket()
    sock.connect(('127.0.0.1', apiserver.ports['8080/tcp'][0]))
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

In the example you'll notice we defined an `apiclient` fixture. Of course if you use that it will implicitly pull in both of the server fixtures and 'just work':

```python
# test_smoketest.py

import json


def test_api_server(apiclient):
    apiclient.request('GET', '/')
    response = apiclient.getresponse()
    assert response.status == 200
    assert json.loads(response.read()) == {'result': '127.0.0.1'}
```


## Scope

All of the fixture factories take the `scope` keyword. Fixtures created with these factories will behave like any py.test fixture with that scope.

In this example we create a memcache that is `session` scoped and another that is `module` scoped.

```python
# conftest.py

from pytest_docker_tools import container, fetch

memcache_image = fetch(repository='memcached:latest')

memcache_session = container(
    image='{memcache_image.id}',
    scope='session',
    ports={
        '11211/tcp': None,
    },
)

memcache_module = container(
    image='{memcache_image.id}',
    scope='module',
    ports={
        '11211/tcp': None,
    },
)
```

When `test_scope_1.py` runs neither container is running so a new instance of each is started. Their scope is longer than a single `function` so they are kept alive for the next test that needs them.

```python
# test_scope_1.py

import socket

def test_session_1(memcache_session):
    sock = socket.socket()
    sock.connect(('127.0.0.1', memcache_session.ports['11211/tcp'][0]))
    sock.sendall(b'set mykey 0 600 4\r\ndata\r\n')
    sock.sendall(b'get mykey\r\n')
    assert sock.recv(1024) == b'STORED\r\nVALUE mykey 0 4\r\ndata\r\nEND\r\n'
    sock.close()

def test_session_2(memcache_session):
    sock = socket.socket()
    sock.connect(('127.0.0.1', memcache_session.ports['11211/tcp'][0]))
    sock.sendall(b'set mykey 0 600 4\r\ndata\r\n')
    sock.sendall(b'get mykey\r\n')
    assert sock.recv(1024) == b'STORED\r\nVALUE mykey 0 4\r\ndata\r\nEND\r\n'
    sock.close()

def test_module_1(memcache_module):
    sock = socket.socket()
    sock.connect(('127.0.0.1', memcache_module.ports['11211/tcp'][0]))
    sock.sendall(b'set mykey 0 600 4\r\ndata\r\n')
    sock.sendall(b'get mykey\r\n')
    assert sock.recv(1024) == b'STORED\r\nVALUE mykey 0 4\r\ndata\r\nEND\r\n'
    sock.close()

def test_module_2(memcache_module):
    sock = socket.socket()
    sock.connect(('127.0.0.1', memcache_module.ports['11211/tcp'][0]))
    sock.sendall(b'set mykey 0 600 4\r\ndata\r\n')
    sock.sendall(b'get mykey\r\n')
    assert sock.recv(1024) == b'STORED\r\nVALUE mykey 0 4\r\ndata\r\nEND\r\n'
    sock.close()
```

When `test_scope_2.py` runs the `session` scoped container is still running, so it will be reused. But we are now in a new module now so the `module` scoped container will have been destroyed. A new empty instance will be created.

```python
# test_scope_2.py

import socket

def test_session_3(memcache_session):
    sock = socket.socket()
    sock.connect(('127.0.0.1', memcache_session.ports['11211/tcp'][0]))
    sock.sendall(b'get mykey\r\n')
    assert sock.recv(1024) == b'VALUE mykey 0 4\r\ndata\r\nEND\r\n'
    sock.close()

def test_module_3(memcache_module):
    sock = socket.socket()
    sock.connect(('127.0.0.1', memcache_module.ports['11211/tcp'][0]))
    sock.sendall(b'get mykey\r\n')
    assert sock.recv(1024) == b'END\r\n'
    sock.close()
```


## Parallelism

Integration and smoke tests are often slow, but a lot of time is spent waiting. So running tests in parallel is a great way to speed them up. `pytest-docker-tools` avoids creating resource names that could collide. It also makes it easy to not care what port your service is bound to. This means its a great fit for use with `pytest-xdist`.

Here is a bare minimum example that just tests creating and destroying 100 instances of a redis fixture that runs under xdist. Create a `test_xdist.py` plugin:

```python

import pytest
from pytest_docker_tools import container, fetch

my_redis_image = fetch(repository='redis:latest')

my_redis = container(
    image='{my_redis_image.id}',
)


@pytest.mark.parametrize("i", list(range(100)))
def test_xdist(i, my_redis):
    assert my_redis.status == "running"
```

And invoke it with:

```bash
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

```python
from pytest_docker_tools import container

my_microservice_backend = container(image='redis:latest')
```

The default scope for this factory is `function`. This means a new container will be created for each test.

The `container` fixture factory supports all parameters that can be passed to the docker-py `run` method. See [here](https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.run) for them all.

Any string variables are interpolated against other defined fixtures. This means that a fixture can depend on other fixtures, and they will be built and run in order.

For example:

```python
from pytest_docker_tools import container, fetch

redis_image = fetch(repository='redis:latest')
redis = container(image='{redis_image.id}')


def test_container_starts(redis):
    assert redis.status == "running"
```

This will fetch the latest `redis:latest` first, and then run a container from the exact image that was pulled. Note that if you don't use `build` or `fetch` to prepare a Docker image then the tag or hash that you specify must already exist on the host where you are running the tests. There is no implicit fetching of Docker images.

The container will be ready when the test is started, and will be automatically deleted after the test has finished.

If for some reason it's not ready in the timeout period (30 seconds by default) the test will fail.

`timeout` can be passed to the `container` factory:

```python
from pytest_docker_tools import container, fetch

redis_image = fetch(repository='redis:latest')
redis = container(image='{redis_image.id}', timeout=30)

def test_container_starts(redis):
    assert redis.status == "running"
```

To create a container defining its `Dockerfile` in code:

```python
import io

from pytest_docker_tools import build, container

dockerfile = io.BytesIO(b"""
FROM alpine:3.12
RUN apk --no-cache add python3
CMD ["tail", "-f", "/dev/null"]
""")

image = build(fileobj=dockerfile)
container = container(image='{image.id}')

def test_container_starts(container):
    assert container.status == "running"
```

#### Ip Addresses

If your container is only attached to a single network you can get its Ip address through a helper property. Given this environment:

```python
# conftest.py

from pytest_docker_tools import container, fetch, network

redis_image = fetch(repository='redis:latest')
backend_network = network()

redis = container(
  image='{redis_image.id}',
  network='{backend_network.name}',
)
```

You can access the IP via the container helper:

```python
import ipaddress

def test_get_service_ip(redis):
    # This will raise a ValueError if not a valid ip
    ipaddress.ip_address(redis.ips.primary)
```

If you want to look up its ip address by network you can also access it more specifically:

```python
import ipaddress

def test_get_service_ip(backend_network, redis):
    ipaddress.ip_address(redis.ips[backend_network])
```

#### Ports

The factory takes the same port arguments as the official Python Docker API. We recommend using the ephemeral high ports syntax:

```python
# conftest.py

from pytest_docker_tools import container

apiserver = container(
  image='{apiserver_image.id}',
  ports={'8080/tcp': None}
)
```

Docker will map port 8080 in the container to a random port on your host. In order to access it from your tests you can get the bound port from the container instance:

```python
def test_connect_my_service(apiserver):
    assert apiserver.ports['8080/tcp'][0] != 8080
```


#### Logs

You can inspect the logs of your container with the logs method:

```python
from pytest_docker_tools import container, fetch


redis_image = fetch(repository='redis:latest')
redis = container(
    image='{redis_image.id}',
    ports={'6379/tcp': None},
)

def test_logs(redis):
    assert 'oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo' in redis.logs()
```


### Images

To pull an image from your default repository use the `fetch` fixture factory. To build an image from local source use the `build` fixture factory. If you are smoke testing an artifact already built locally you can use the `image` fixture factory to reference it.

```python
from pytest_docker_tools import build, image, fetch

my_image = fetch(repository='redis:latest')

my_image_2 = build(
  path='db'
)
```

The `build` fixture factory supports all parameters that can be passed to the docker-py `build` method. See [here](https://docker-py.readthedocs.io/en/stable/images.html#docker.models.images.ImageCollection.build) for them all. The `fetch` fixture factory supports all parameters that can be passed to the docker-py `pull` method. See [here](https://docker-py.readthedocs.io/en/stable/images.html#docker.models.images.ImageCollection.pull) for them all.

The default scope for this factory is `session`. This means the fixture will only build or fetch once per py.test invocation. The fixture will not be triggered until a test (or other fixture) tries to use it. This means you won't waste time building an image if you aren't running the test that uses it.


### Networks

By default any containers you create with the `container()` fixture factory will run on your default docker network. You can create a dedicated network for your test with the `network()` fixture factory.

```python
from pytest_docker_tools import network

frontend_network = network()
```

The `network` fixture factory supports all parameters that can be passed to the docker-py network `create` method. See [here](https://docker-py.readthedocs.io/en/stable/networks.html#docker.models.networks.NetworkCollection.create) for them all.

The default scope for this factory is `function`. This means a new network will be created for each test that is executed.

The network will be removed after the test using it has finished.


### Volumes

In the ideal case a Docker container instance is read only. No data inside the container is written to, if it is its to a volume. If you are testing that your service can run read only you might want to mount a rw volume. You can use the `volume()` fixture factory to create a Docker volume with a lifecycle tied to your tests.

```python
from pytest_docker_tools import volume

backend_storage = volume()
```

The `volume` fixture factory supports all parameters that can be passed to the docker-py volume `create` method. See [here](https://docker-py.readthedocs.io/en/stable/volumes.html#docker.models.volumes.VolumeCollection.create) for them all.

In addition you can specify a `initial_content` dictionary. This allows you to seed a volume with a small set of initial state. In the following example we'll preseed a minio service with 2 buckets and 1 object in 1 of those buckets.

```python
from pytest_docker_tools import container, fetch, volume


minio_image = fetch(repository='minio/minio:latest')

minio_volume = volume(
    initial_content={
        'bucket-1': None,
        'bucket-2/example.txt': b'Test file 1',
    }
)

minio = container(
    image='{minio_image.id}',
    command=['server', '/data'],
    volumes={
        '{minio_volume.name}': {'bind': '/data'},
    },
    environment={
        'MINIO_ACCESS_KEY': 'minio',
        'MINIO_SECRET_KEY': 'minio123',
    },
)

def test_volume_is_seeded(minio):
    files = minio.get_files('/data')
    assert files['data/bucket-2/example.txt'] == b'Test file 1'
    assert files['data/bucket-1'] == None
```

The `minio_volume` container will be created with an empty folder (`bucket-1`) and a text file called `example.txt` in a seperate folder called `bucket-2`.

The default scope for this factory is `function`. This means a new volume will be created for each test that is executed. The volume will be removed after the test using it has finished.


## Fixtures

### docker_client

The `docker_client` fixture returns an instance of the official docker client.

```python
def test_container_created(docker_client, fakedns):
    for c in docker_client.containers.list(ignore_removed=True):
        if c.id == fakedns.id:
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

### Testing build artifacts

We often find ourselves using a set of tests against a container we've built at test time (with `build()`) but then wanting to use the same tests with an artifact generated on our CI platform (with `image()`). This ended up looking like this:

```
if not os.environ.get('IMAGE_ID', ''):
    image = build(path='examples/resolver-service/dns')
else:
    image = image(name=os.environ['IMAGE_ID'])
```

But now you can just do:

```python
from pytest_docker_tools import image_or_build

image = image_or_build(
    environ_key='IMAGE_ID',
    path='examples/resolver-service/dns',
)

def test_image(image):
    assert image.attrs['Os'] == 'linux'
```


### Network differences between dev env and CI

Another common difference between your dev environment and your CI environment might be that your tests end up running in Docker on your CI. If you bind-mount your `docker.sock` then your tests might end up running on the same container network as the containers you are testing, and unable to access any port you are mapping to the host box. In otherwords:

 * On your dev machine your tests might access locahost:8000 to access your test instance (ports mapped to host)
 * On your CI machine they might need to access 172.16.0.5:8000 to access your test instance

The container object has a `get_addr` helper which will return the right thing depending on the environment it is in.

```python
from pytest_docker_tools import container

apiserver = container(
  image='{apiserver_image.id}',
  ports={'8080/tcp': None}
)

def test_connect_my_service(apiserver):
    ip, port = apiserver.get_addr('8080/tcp')
    # ... connect to ip:port ...
```


### Client fixtures

You will probably want to create an API client for the service you are testing. Although we've already done this in the README, its worth calling it out. You can define a client fixture, have it depend on your docker containers, and then only have to reference the client from your tests.

```python
# conftest.py

from http.client import HTTPConnection

import pytest
from pytest_docker_tools import build, container

fakedns_image = build(
    path='examples/resolver-service/dns',
)

fakedns = container(
    image='{fakedns_image.id}',
    environment={
        'DNS_EXAMPLE_COM__A': '127.0.0.1',
    }
)

apiserver_image = build(
    path='examples/resolver-service/api',
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
```

And then reference it from your tests:

```python
# test_the_test_client.py

import json


def test_api_server(apiclient):
    apiclient.request('GET', '/')
    response = apiclient.getresponse()
    assert response.status == 200
    result = json.loads(response.read())
    assert result['result'] == '127.0.0.1'
```

In this example, any test that uses the `hpfeeds_client` fixture will get a properly configure client connected to a broker running in a Docker container on an ephemeral high port. When the test finishes the client will cleanly disconnect, and the docker container will be thrown away.


### Fixture overloading

Complicated environments can be defined with fixture factories. They form a directed acyclic graph. By using fixture overloading it is possible to (in the context of a single test module) replace a node in that dependency graph without having to redefine the entire environment.

#### Replacing a container fixture without having to redefine its dependents

You can define a fixture in your `conftest.py`:

```python
# conftest.py

from http.client import HTTPConnection

import pytest
from pytest_docker_tools import build, container

fakedns_image = build(
    path='examples/resolver-service/dns',
)

fakedns = container(
    image='{fakedns_image.id}',
    environment={
        'DNS_EXAMPLE_COM__A': '127.0.0.1',
    }
)

apiserver_image = build(
    path='examples/resolver-service/api',
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
```

You can then overload these fixtures in your test modules. For example, if redis had a magic replication feature and you want to test for an edge case with your API you could in your `test_smoketest_alternate.py`:

```python
# test_smoketest_alternate.py

import json

from pytest_docker_tools import container

fakedns = container(
    image='{fakedns_image.id}',
    environment={
        'DNS_EXAMPLE_COM__A': '192.168.192.168',
    }
)

def test_api_server(apiclient):
    apiclient.request('GET', '/')
    response = apiclient.getresponse()
    assert response.status == 200
    result = json.loads(response.read())
    assert result['result'] == '192.168.192.168'
```

Here we have redefined the fakedns container locally in `test_smoketest_alternate`. It is able to use the `fakedns_image` fixture we defined in `conftest.py`. More crucially though, in `test_smoketest_alternate.py` when we use the core `apiclient` fixture it actually pulls in the local definition of `fakedns` and not the one from `conftest.py`! You don't have to redefine anything else. It just works.


#### Injecting fixture configuration through fixtures

You can pull in normal py.test fixtures from your fixture factory too. This means we can use fixture overloading and pass in config. In your `conftest.py`:

```python
# conftest.py

from http.client import HTTPConnection

import pytest
from pytest_docker_tools import build, container

fakedns_image = build(
    path='examples/resolver-service/dns',
)

fakedns = container(
    image='{fakedns_image.id}',
    environment={
        'DNS_EXAMPLE_COM__A': '{example_com_a}',
    }
)

apiserver_image = build(
    path='examples/resolver-service/api',
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


@pytest.fixture
def example_com_a():
    return '127.0.0.1'

```

When a test uses the apiclient fixture now they will get the fakedns container configured as normal. However you can redefine the fixture in your test module - and the other fixtures will still respect it. For example:

```python
# test_smoketest_alternate.py

import json

import pytest


@pytest.fixture
def example_com_a():
    return '192.168.192.168'


def test_api_server(apiclient):
    apiclient.request('GET', '/')
    response = apiclient.getresponse()
    assert response.status == 200
    result = json.loads(response.read())
    assert result['result'] == '192.168.192.168'
```

Your `api_server` container (and its `redis` backend) will be built as normal, only in this one test module it will use its sqlite backend.


### Fixture parameterisation

You can create parameterisation fixtures. Perhaps you wan to run all your `api_server` tests against both of your authentication backends. Perhaps you have a fake that you want to test multiple configurations of.

In your `conftest.py`:

```python
# conftest.py

from http.client import HTTPConnection

import pytest
from pytest_docker_tools import build, container

fakedns_image = build(
    path='examples/resolver-service/dns',
)

fakedns_localhost = container(
    image='{fakedns_image.id}',
    environment={
        'DNS_EXAMPLE_COM__A': '127.0.0.1',
    }
)

fakedns_alternate = container(
    image='{fakedns_image.id}',
    environment={
        'DNS_EXAMPLE_COM__A': '192.168.192.168',
    }
)

@pytest.fixture(scope='function', params=['fakedns_localhost', 'fakedns_alternate'])
def fakedns(request):
      return request.getfixturevalue(request.param)

apiserver_image = build(
    path='examples/resolver-service/api',
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
```

The test is the same as the first example, only now it will be tested against 2 different fake configurations.

```python
# test_smoketest.py

import ipaddress
import json


def test_api_server(apiclient):
    apiclient.request('GET', '/')
    response = apiclient.getresponse()
    assert response.status == 200
    result = json.loads(response.read())
    ipaddress.ip_address(result['result'])
```

This test will be invoked twice - once against the memory backend, and once against the sqlite backend.


### Fixture wrappers

You can wrap your fixtures with a `wrapper_class`. This allows you to add helper methods to fixtures for use in your tests. In the case of the `container` fixture factory you can also implement `ready()` to add additional container readyness checks.

In previous tests we've created an entire test client fixture. With `wrapper_class` we could hang this convenience method off the fixture itself instead:

```python
# test_fixture_wrappers.py

import ipaddress
import json
import random

from http.client import HTTPConnection

import pytest
from pytest_docker_tools import build, container
from pytest_docker_tools import wrappers


class Container(wrappers.Container):

    def ready(self):
        # This is called until it returns True - its a great hook for e.g.
        # waiting until a log message appears or a pid file is created etc
        if super().ready():
            return random.choice([True, False])
        return False

    def client(self):
        port = self.ports['8080/tcp'][0]
        return HTTPConnection(f'localhost:{port}')


fakedns_image = build(
    path='examples/resolver-service/dns',
)

fakedns = container(
    image='{fakedns_image.id}',
    environment={
        'DNS_EXAMPLE_COM__A': '127.0.0.1',
    }
)

apiserver_image = build(
    path='examples/resolver-service/api',
)

apiserver = container(
    image='{apiserver_image.id}',
    ports={
        '8080/tcp': None,
    },
    dns=['{fakedns.ips.primary}'],
    wrapper_class=Container,
)


def test_container_wrapper_class(apiserver):
    client = apiserver.client()
    client.request('GET', '/')
    response = client.getresponse()
    assert response.status == 200
    result = json.loads(response.read())
    ipaddress.ip_address(result['result'])

```

## Hacking

Set up a virtualenv for development:

```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -U pip
$ pip install flit -r requirements.txt
$ flit install --symlink
```

Run tests and check coverage:

```
$ coverage run --source pytest_docker_tools -m py.test
$ coverage html
$ $BROWSER htmlcov/index.html
```

Check style:

```
$ flake8 pytest_docker_tools tests
```
