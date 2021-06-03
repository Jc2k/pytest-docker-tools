from _pytest.pytester import Pytester
from docker.client import DockerClient


def test_image(request, pytester: Pytester, docker_client: DockerClient):
    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import image",
                "memcache_image = image(name='memcached:latest')",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_container="\n".join(
            (
                "def test_session_1(memcache_image):",
                "    assert 'memcached:latest' in memcache_image.tags",
            )
        )
    )

    docker_client.images.pull(repository="memcached:latest")

    result = pytester.runpytest()
    result.assert_outcomes(passed=1, errors=0)
