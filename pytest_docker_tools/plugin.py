import docker
import pytest

from .exceptions import ContainerError
from .wrappers import Container


@pytest.fixture(scope="session")
def docker_client(request) -> docker.client.DockerClient:
    """ A Docker client configured from environment variables """
    return docker.from_env()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    This hook allows Docker containers to contribute their logs to the py.test
    report.
    """

    outcome = yield
    rep = outcome.get_result()

    if not rep.failed:
        return

    if call.excinfo and isinstance(call.excinfo.value, ContainerError):
        container = call.excinfo.value._container
        rep.sections.append((container.name, container.logs()))

    if "request" not in item.funcargs:
        return

    for name, fixturedef in item.funcargs["request"]._fixture_defs.items():
        if not hasattr(fixturedef, "cached_result") or not fixturedef.cached_result:
            continue
        fixture = fixturedef.cached_result[0]
        if isinstance(fixture, Container):
            rep.sections.append(
                (
                    name + ": " + fixture.name,
                    fixture.logs(),
                )
            )


def pytest_addoption(parser):
    group = parser.getgroup("pytest-docker-tools", "Pytest Docker Tools")
    group.addoption(
        "--reuse-containers",
        action="store_true",
        dest="reuse_containers",
        help="reuse existing containers instead of always creating new ones. Requires the 'name' attribute to be set"
        "on container definition",
    )
