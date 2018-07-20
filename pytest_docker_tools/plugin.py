import docker
import pytest


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

    if rep.when != 'call':
        return

    if not rep.failed:
        return

    for name, fixture in item.funcargs.items():
        if isinstance(fixture, dict) and 'container' in fixture:
            container = fixture['container']
            rep.sections.append((
                name + ': ' + container.name,
                container.logs().decode('utf-8'),
            ))
