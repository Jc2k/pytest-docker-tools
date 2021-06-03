from _pytest.pytester import Pytester
from docker.client import DockerClient
from unittest import mock
import os


def test_image_or_build_env_set(request, pytester: Pytester, docker_client: DockerClient):
    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import image_or_build",
                "memcache_image = image_or_build('ENVIRON_KEY')",
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

    with mock.patch.dict(os.environ, {"ENVIRON_KEY": "memcached:latest"}):
        result = pytester.runpytest()

    result.assert_outcomes(passed=1, errors=0)


def test_image_or_build_env_not_set(request, pytester: Pytester, docker_client: DockerClient):
    # A fake build.
    pytester.makefile(
        "",
        Dockerfile="\n".join(
            (
                "FROM alpine:3.13 AS builder",
                "LABEL test_image_or_build_env_not_set=yes",
            )
        ),
    )

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import image_or_build",
                "memcache_image = image_or_build('ENVIRON_KEY', path='.')",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_container="\n".join(
            (
                "def test_session_1(memcache_image):",
                "    assert 'test_image_or_build_env_not_set' in memcache_image.labels",
            )
        )
    )

    with mock.patch.dict(os.environ, {}):
        result = pytester.runpytest()

    result.assert_outcomes(passed=1, errors=0)
