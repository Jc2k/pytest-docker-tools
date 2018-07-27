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

    if 'request' in item.funcargs:
        for name, fixturedef in item.funcargs['request']._fixture_defs.items():
            fixture = fixturedef.cached_result[0]
            if isinstance(fixture, Container):
                rep.sections.append((
                    name + ': ' + fixture.name,
                    fixture.logs(),
                ))
    else:
        for name, fixture in item.funcargs.items():
            if isinstance(fixture, Container):
                rep.sections.append((
                    name + ': ' + fixture.name,
                    fixture.logs(),
                ))
