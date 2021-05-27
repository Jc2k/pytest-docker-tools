import os
import sys
import time

from .exceptions import TimeoutError

LABEL_REUSABLE_CONTAINER = "pytest-docker-tools.reusable-container"


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
    return container.attrs["Config"]["Labels"].get(LABEL_REUSABLE_CONTAINER) == "True"
