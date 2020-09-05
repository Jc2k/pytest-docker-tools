import os
import sys
import time

from .exceptions import TimeoutError


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

    if not os.path.exists("/proc/1/sched"):
        return False

    with open("/proc/1/sched") as fp:
        line1 = fp.read().split("\n")[0]

    # Right now this file contains a header like this which leaks the actual pid
    #     systemd (1, #threads: 1)
    # If its not '1' we have detected containment

    init, info = line1.split(" ", 1)
    pid, threads = info.strip("(").rstrip(")").split(", ", 1)
    return pid != "1"
