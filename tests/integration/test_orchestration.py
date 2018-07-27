'''
This module contains tests of the 'orchestration' of dependent docker units.
If a container depends on an image and a container, and that container depends
on another container, and so on, then all the contains should be built in the
right order.
'''

from pytest_docker_tools import build, container, fetch, network, volume

redis_image = fetch(repository='redis:latest')

redis0 = container(
    image='{redis_image.id}',
    environment={
        'MARKER': 'redis0-0sider',
    }
)

foobar = build(path='tests/integration')
mynetwork = network()
myvolume = volume()
mycontainer = container(
    image='{foobar.id}',
    network='{mynetwork.id}',
    volumes={
        '{myvolume.id}': {'bind': '/var/tmp'},
    },
    environment={
        'REDIS_IP': lambda redis0: redis0.ips.primary,
    },
    dns=['{redis0.ips.primary}'],
)


def test_related_container_created(docker_client, mycontainer):
    ''' Creating mycontainer should pull in redis0 because we depend on it to calculate an env variable '''
    backend_ip = mycontainer.env['REDIS_IP']
    for c in docker_client.containers.list(ignore_removed=True):
        if 'MARKER=redis0-0sider' in c.attrs['Config']['Env'] and backend_ip in str(c.attrs):
            break
    else:
        assert False, 'redis0 not running'


def test_gets_related_container_ip(redis0, mycontainer):
    ''' The lambda we passed to environment should have been executed with the redis fixture value '''
    assert mycontainer.env['REDIS_IP'] == redis0.ips.primary


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
