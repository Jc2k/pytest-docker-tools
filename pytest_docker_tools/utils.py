import sys
import time


def wait_for_callable(message, callable, timeout=30):
    '''
    Runs a callable once a second until it returns True or we hit the timeout.
    '''
    sys.stdout.write(message)
    try:
        for i in range(timeout):
            sys.stdout.write('.')
            sys.stdout.flush()

            if callable():
                return

            time.sleep(1)
    finally:
        sys.stdout.write('\n')

    raise RuntimeError('Timeout exceeded')
