import docker
import pytest

from .wrappers import Container


@pytest.fixture(scope='session')
def docker_client(request):
    ''' A Docker client configured from environment variables '''
    return docker.from_env()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    This hook allows Docker containers to contribute their logs to the py.test
    report.
    '''

    outcome = yield
    rep = outcome.get_result()

    if not rep.failed:
        return

    if 'request' not in item.funcargs:
        return

    for name, fixturedef in item.funcargs['request']._fixture_defs.items():
        if not hasattr(fixturedef, 'cached_result'):
            continue
        fixture = fixturedef.cached_result[0]
        if isinstance(fixture, Container):
            rep.sections.append((
                name + ': ' + fixture.name,
                fixture.logs(),
            ))
