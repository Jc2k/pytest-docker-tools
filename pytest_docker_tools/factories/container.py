import inspect

import pytest


def get_addresses(container):
    networks = container.attrs['NetworkSettings']['Networks']
    addresses = {}
    for name, network in networks.items():
        if not network['IPAddress']:
            return {}
        addresses[name] = network['IPAddress']
    return addresses


def create_container(request, docker_client, *args, **kwargs):
    kwargs.update({'detach': True})

    container = docker_client.containers.run(*args, **kwargs)
    request.addfinalizer(lambda: container.remove(force=True))

    ips = get_addresses(container)
    while not ips:
        container.reload()
        ips = get_addresses(container)

    container_ip = next(iter(ips.values()))

    return {
        'container': container,
        'ip': container_ip,
        'logs': lambda: container.logs().decode('utf-8'),
    }


def _process_image(request, image):
    if hasattr(image, '_pytestfixturefunction'):
        return request.getfixturevalue(image._pytestfixturefunction.name).id
    return image


def _process_network(request, network):
    if hasattr(network, '_pytestfixturefunction'):
        return request.getfixturevalue(network._pytestfixturefunction.name).id
    return network


def _process_volumes(request, volumes):
    vols = {}
    for key, val in volumes.items():
        if hasattr(key, '_pytestfixturefunction'):
            key = request.getfixturevalue(key._pytestfixturefunction.name).id
        vols[key] = val
    return vols


def _process_environment(request, environment):
    env = {}
    for key, val in environment.items():
        if callable(val):
            val = val(*[request.getfixturevalue(f) for f in inspect.getargspec(val)[0]])
        env[key] = val
    return env


def container(name, image, *, scope='function', **kwargs):
    '''
    Fixture factory for creating containers. For example in your conftest.py
    you can:

        from pytest_docker_tools import container_fixture

        test_container = container_fixture('test_container', 'redis')

    This will create a container called 'test_container' from the 'redis' image.
    '''

    def container(request, docker_client):
        local_kwargs = dict(kwargs)

        if 'network' in local_kwargs:
            local_kwargs['network'] = _process_network(request, local_kwargs.pop('network'))

        environment = _process_environment(request, local_kwargs.pop('environment', {}))
        volumes = _process_volumes(request, local_kwargs.pop('volumes', {}))

        container = create_container(
            request,
            docker_client,
            _process_image(request, image),
            environment=environment,
            volumes=volumes,
            **local_kwargs
        )

        return container

    container.__name__ = name
    pytest.fixture(scope=scope, name=name)(container)

    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    setattr(module, name, container)

    return container
