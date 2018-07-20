import io
import sys
import tarfile
import time


def get_files(container, path):
    '''
    Retrieve files from a container at a given path.

    This is meant for extracting log files from a container where it is not
    using the docker logging capabilities.
    '''

    archive_iter, _ = container.get_archive(path)

    archive_stream = io.BytesIO()
    [archive_stream.write(chunk) for chunk in archive_iter]
    archive_stream.seek(0)

    archive = tarfile.TarFile(fileobj=archive_stream)
    files = {}
    for info in archive.getmembers():
        if not info.isfile():
            continue
        reader = archive.extractfile(info.name)
        files[info.name] = reader.read().decode('utf-8')

    return files


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


def wait_for_port(container, port, timeout=10):
    '''
    Waits for a container to be listening on a given port.

    The container must have netstat installed.
    '''
    def _():
        netstat = container.exec_run('netstat -an')[1].decode('utf-8').strip()
        for line in netstat.split('\n'):
            if not line:
                continue
            line = line.split()
            if line[0].strip() not in ('tcp', 'udp'):
                continue
            if not line[3].strip().endswith(f':{port}'):
                continue
            if line[0].strip() == 'tcp' and line[5].strip() != 'LISTEN':
                continue

            # Port is open!
            return True
        else:
            return False

    return wait_for_callable(
        f'Waiting for {port} to be open in container {container.short_id}',
        _,
        timeout,
    )
