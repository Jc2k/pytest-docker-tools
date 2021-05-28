import pytest


@pytest.fixture()
def enable_container_reuse(request):
    request.config.option.reuse_containers = True
    yield
    request.config.option.reuse_containers = False
