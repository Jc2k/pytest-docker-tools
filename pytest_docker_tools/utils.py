import os
import sys
import time

from .exceptions import TimeoutError

LABEL_REUSABLE = "pytest-docker-tools.reusable"


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
    return volume.attrs["Labels"].get(LABEL_REUSABLE) == "True"


def set_reusable_labels(kwargs, request):
    labels = kwargs.setdefault("labels", {})

    labels.update(
        {
            "creator": "pytest-docker-tools",
            LABEL_REUSABLE: str(request.config.option.reuse_containers),
        }
    )
