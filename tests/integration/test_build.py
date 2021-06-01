from _pytest.pytester import Pytester
from docker.client import DockerClient
from docker.errors import ImageNotFound
import pytest


def test_tag_stages(request, pytester: Pytester, docker_client: DockerClient):
    builder_tag = "localhost/pytest-docker-tools/buildtest:builder"
    latest_tag = "localhost/pytest-docker-tools/buildtest:latest"

    def _cleanup():
        for tag in (builder_tag, latest_tag):
            try:
                docker_client.images.remove(tag)
            except ImageNotFound:
                return

    request.addfinalizer(_cleanup)

    with pytest.raises(ImageNotFound):
        for tag in (builder_tag, latest_tag):
            docker_client.images.get(tag)

    # A fake multi stage build.
    pytester.makefile(
        "",
        Dockerfile="\n".join(
            (
                "FROM alpine:3.13 AS builder",
                "RUN touch /hello-intermediate-step",
                "RUN touch /hello",
                "FROM alpine:3.13",
                "COPY --from=builder /hello /hello",
            )
        ),
    )

    pytester.makeconftest(
        "\n".join(
            (
                "from pytest_docker_tools import build",
                "myimage = build(",
                "    path='.',",
                f"    tag='{latest_tag}',",
                f"    stages={{'builder': '{builder_tag}'}},",
                ")",
            )
        )
    )

    pytester.makepyfile(
        test_reusable_network="\n".join(
            (
                "def test_session_1(myimage):",
                f"    assert '{latest_tag}' in myimage.tags",
            )
        )
    )

    result = pytester.runpytest()
    result.assert_outcomes(passed=1)

    latest = docker_client.images.get(latest_tag)
    assert latest is not None

    builder = docker_client.images.get(builder_tag)
    assert builder is not None

    assert latest.id != builder.id
