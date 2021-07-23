import base64
import hashlib
import json
import os
import sys
import time
from typing import Any, Callable, Dict

from _pytest.fixtures import SubRequest
from docker.models.containers import Container
from docker.models.networks import Network
from docker.models.volumes import Volume

from .exceptions import TimeoutError

LABEL_REUSABLE = "pytest-docker-tools.reusable"
LABEL_SIGNATURE = "pytest-docker-tools.signature"


def wait_for_callable(message: str, func: Callable, timeout: int = 30) -> None:
    """
    Runs a callable once a second until it returns True or we hit the timeout.
    """
    sys.stdout.write(message)
    try:
        for i in range(timeout):
            sys.stdout.write(".")
            sys.stdout.flush()

            if func():
                return

            time.sleep(1)
    finally:
        sys.stdout.write("\n")

    raise TimeoutError(f"Timeout of {timeout}s exceeded")


def tests_inside_container() -> bool:
    """ Returns True if tests are running inside a Linux container """

    return os.path.isfile("/.dockerenv") or os.path.isfile("/run/.containerenv")


def is_reusable_container(container: Container) -> bool:
    return container.attrs["Config"]["Labels"].get(LABEL_REUSABLE) == "True"


def is_reusable_network(network: Network) -> bool:
    return network.attrs["Labels"].get(LABEL_REUSABLE) == "True"


def is_reusable_volume(volume: Volume) -> bool:
    labels = volume.attrs["Labels"]
    return labels and labels.get(LABEL_REUSABLE) == "True"


def set_reusable_labels(kwargs: Dict[str, Any], request: SubRequest) -> None:
    labels = kwargs.setdefault("labels", {})

    labels.update(
        {
            "creator": "pytest-docker-tools",
            LABEL_REUSABLE: str(request.config.option.reuse_containers),
        }
    )


class Base64Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> str:
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode("utf-8")
        return super().default(obj)


def hash_params(kwargs: Dict[str, Any]) -> str:
    rendered = json.dumps(kwargs, cls=Base64Encoder, sort_keys=True).encode("utf-8")
    signature = hashlib.sha256(rendered).hexdigest()
    return signature


def set_signature(kwargs: Dict[str, Any], signature: str) -> None:
    labels = kwargs.setdefault("labels", {})
    labels[LABEL_SIGNATURE] = signature


def check_signature(labels: Dict[str, Any], signature: str) -> bool:
    return labels.get(LABEL_SIGNATURE, "") == signature


def is_using_network(container: Container, network: Network) -> bool:
    settings = container.attrs.get("NetworkSettings", {})
    return network.name in settings.get("Networks", {})


def is_using_volume(container: Container, volume: Volume) -> bool:
    for mount in container.attrs.get("Mounts", []):
        if mount["Type"] != "volume":
            continue
        if mount["Name"] == volume.name:
            return True
    return False


class _FixtureRef:
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name


fxtr = _FixtureRef
