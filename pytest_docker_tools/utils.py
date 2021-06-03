import base64
import hashlib
import json
import os
import sys
import time

from .exceptions import TimeoutError

LABEL_REUSABLE = "pytest-docker-tools.reusable"
LABEL_SIGNATURE = "pytest-docker-tools.signature"


def wait_for_callable(message, callable, timeout=30):
    """
    Runs a callable once a second until it returns True or we hit the timeout.
    """
    sys.stdout.write(message)
    try:
        for i in range(timeout):
            sys.stdout.write(".")
            sys.stdout.flush()

            if callable():
                return

            time.sleep(1)
    finally:
        sys.stdout.write("\n")

    raise TimeoutError(f"Timeout of {timeout}s exceeded")


def tests_inside_container():
    """ Returns True if tests are running inside a Linux container """

    return os.path.isfile("/.dockerenv") or os.path.isfile("/run/.containerenv")


def is_reusable_container(container):
    return container.attrs["Config"]["Labels"].get(LABEL_REUSABLE) == "True"


def is_reusable_network(network):
    return network.attrs["Labels"].get(LABEL_REUSABLE) == "True"


def is_reusable_volume(volume):
    labels = volume.attrs["Labels"]
    return labels and labels.get(LABEL_REUSABLE) == "True"


def set_reusable_labels(kwargs, request):
    labels = kwargs.setdefault("labels", {})

    labels.update(
        {
            "creator": "pytest-docker-tools",
            LABEL_REUSABLE: str(request.config.option.reuse_containers),
        }
    )


class Base64Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode("utf-8")
        return super().default(obj)


def hash_params(kwargs):
    rendered = json.dumps(kwargs, cls=Base64Encoder, sort_keys=True).encode("utf-8")
    signature = hashlib.sha256(rendered).hexdigest()
    return signature


def set_signature(kwargs, signature):
    labels = kwargs.setdefault("labels", {})
    labels[LABEL_SIGNATURE] = signature


def check_signature(labels, signature):
    return labels.get(LABEL_SIGNATURE, "") == signature


def is_using_network(container, network):
    settings = container.attrs.get("NetworkSettings", {})
    return network.name in settings.get("Networks", {})


def is_using_volume(container, volume):
    for mount in container.attrs.get("Mounts", []):
        if mount["Type"] != "volume":
            continue
        if mount["Name"] == volume.name:
            return True
    return False
