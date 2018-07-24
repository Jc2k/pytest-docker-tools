import docker
import pytest

from .wrappers import Container


@pytest.fixture(scope='session')
def docker_client(request):
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

    for name, fixture in item.funcargs.items():
        if isinstance(fixture, Container):
            rep.sections.append((
                name + ': ' + fixture.name,
                fixture.logs(),
            ))
