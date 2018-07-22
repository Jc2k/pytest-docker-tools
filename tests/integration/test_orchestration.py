'''
This module contains tests of the 'orchestration' of dependent docker units.
If a container depends on an image and a container, and that container depends
on another container, and so on, then all the contains should be built in the
right order.
'''

from pytest_docker_tools import factories

factories.container(
    'redis0',
    image=factories.repository_image('redis'),
    environment={
        'MARKER': 'redis0-0sider',
    }
)

factories.container(
    'mycontainer',
    image=factories.image('foobar', 'tests/integration'),
    network=factories.network('mynetwork'),
    volumes={
        factories.volume('myvolume'): {'bind': '/var/tmp'},
    },
    environment={
        'REDIS_IP': lambda redis0: redis0.ips.primary,
    },
    dns=['{redis0.ips.primary}'],
)


def test_related_container_created(docker_client, mycontainer):
    ''' Creating mycontainer should pull in redis0 because we depend on it to calculate an env variable '''
    for container in docker_client.containers.list():
        if 'MARKER=redis0-0sider' in container.attrs['Config']['Env']:
            break
    else:
        assert False, 'redis0 not running'


def test_gets_related_container_ip(redis0, mycontainer):
    ''' The lambda we passed to environment should have been executed with the redis fixture value '''
    redis_ip_env = f'REDIS_IP={redis0.ips.primary}'
    env = mycontainer.attrs['Config']['Env']
    assert redis_ip_env in env


def test_gets_volume(myvolume, mycontainer):
    ''' The container should have a volume configured pointing at our fixturized volume '''
    for mount in mycontainer.attrs['Mounts']:
        if mount['Name'] == myvolume.name:
            break
    else:
        assert False, 'Could not find attached volume'


def test_gets_network(mynetwork, mycontainer):
    ''' The container should be attached to our fixturized network '''
    assert mynetwork.name in mycontainer.ips


def test_gets_dns_ip(redis0, mycontainer):
    ''' The container should be attached to our fixturized network '''
    assert redis0.ips.primary == mycontainer.attrs['HostConfig']['Dns'][0]
