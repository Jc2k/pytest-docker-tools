"""
This module contains a wrapper that adds some helpers to a Docker Container
object that are useful for integration testing.
"""

import io
import tarfile

from pytest_docker_tools.exceptions import (
    ContainerFailed,
    ContainerNotReady,
    TimeoutError,
)
from pytest_docker_tools.utils import tests_inside_container, wait_for_callable


class _Map:
    def __init__(self, container):
        self._container = container

    def values(self):
        return [self[k] for k in self.keys()]

    def items(self):
        return [(k, self[k]) for k in self.keys()]

    def __iter__(self):
        return iter(self.keys())


class IpMap(_Map):
    @property
    def primary(self):
        return next(iter(self.values()))

    def keys(self):
        return self._container.attrs["NetworkSettings"]["Networks"].keys()

    def __getitem__(self, key):
        if not isinstance(key, str):
            key = key.name

        networks = self._container.attrs["NetworkSettings"]["Networks"]
        if key not in networks:
            raise KeyError(f"Unknown network: {key}")

        return networks[key]["IPAddress"]


class PortMap(_Map):
    def __init__(self, container):
        self._container = container

    def keys(self):
        return self._container.attrs["NetworkSettings"]["Ports"].keys()

    def __getitem__(self, key):
        ports = self._container.attrs["NetworkSettings"]["Ports"]
        if key not in ports:
            raise KeyError(f"Unknown port: {key}")

        if not ports[key]:
            return []

        return [int(p["HostPort"]) for p in ports[key]]


class Container:
    def __init__(self, container):
        self._container = container
        self.ips = IpMap(container)
        self.ports = PortMap(container)

    def ready(self):
        self._container.reload()

        if self.status == "exited":
            raise ContainerFailed(
                self,
                f"Container {self.name} has already exited before we noticed it was ready",
            )

        if self.status != "running":
            return False

        networks = self._container.attrs["NetworkSettings"]["Networks"]
        for name, network in networks.items():
            if not network["IPAddress"]:
                return False

        # If a user has exposed a port then wait for LISTEN socket to show up in netstat
        ports = self._container.attrs["NetworkSettings"]["Ports"]
        for port, listeners in ports.items():
            if not listeners:
                continue

            port, proto = port.split("/")

            assert proto in ("tcp", "udp")

            if proto == "tcp" and port not in self.get_open_tcp_ports():
                return False

            if proto == "udp" and port not in self.get_open_udp_ports():
                return False

        return True

    @property
    def attrs(self):
        return self._container.attrs

    @property
    def id(self):
        return self._container.id

    @property
    def name(self):
        return self._container.name

    @property
    def env(self):
        kv_pairs = map(
            lambda v: v.split("=", 1), self._container.attrs["Config"]["Env"]
        )
        return {k: v for k, v in kv_pairs}

    @property
    def status(self):
        return self._container.status

    def exec_run(self, *args, **kwargs):
        return self._container.exec_run(*args, **kwargs)

    def reload(self):
        return self._container.reload()

    def restart(self, timeout=10):
        self._container.restart(timeout=timeout)

        try:
            wait_for_callable(
                "Waiting for container to be ready after restart", self.ready
            )
        except TimeoutError:
            raise ContainerNotReady(
                self, "Timeout while waiting for container to be ready after restart"
            )

    def kill(self, signal=None):
        return self._container.kill(signal)

    def remove(self, *args, **kwargs):
        raise RuntimeError(
            "Do not remove this container manually. It will be removed automatically by py.test after the test finishes."
        )

    def logs(self):
        return self._container.logs().decode("utf-8")

    def get_files(self, path):
        """
        Retrieve files from a container at a given path.

        This is meant for extracting log files from a container where it is not
        using the docker logging capabilities.
        """

        archive_iter, _ = self._container.get_archive(path)

        archive_stream = io.BytesIO()
        [archive_stream.write(chunk) for chunk in archive_iter]
        archive_stream.seek(0)

        archive = tarfile.TarFile(fileobj=archive_stream)
        files = {}
        for info in archive.getmembers():
            if not info.isfile():
                files[info.name] = None
                continue
            reader = archive.extractfile(info.name)
            files[info.name] = reader.read()

        return files

    def get_text(self, path):
        text = {}
        for path, bytes in self.get_files(path).items():
            if bytes is None:
                text[path] = None
                continue
            text[path] = bytes.decode("utf-8")
        return text

    def get_open_tcp_ports(self):
        """ Gets all TCP sockets in the LISTEN state """
        netstat = (
            self._container.exec_run("cat /proc/net/tcp /proc/net/tcp6")[1]
            .decode("utf-8")
            .strip()
        )

        ports = []
        for line in netstat.split("\n"):
            # Not interested in empty lines
            if not line:
                continue

            line = line.split()

            # Only interested in listen sockets
            if line[3] != "0A":
                continue

            ports.append(str(int(line[1].split(":", 1)[1], 16)))

        return ports

    def get_open_udp_ports(self):
        """ Gets all UDP sockets in the LISTEN state """
        netstat = (
            self._container.exec_run("cat /proc/net/udp /proc/net/udp6")[1]
            .decode("utf-8")
            .strip()
        )

        ports = []
        for line in netstat.split("\n"):
            # Not interested in empty lines
            if not line:
                continue

            line = line.split()

            # If we are listening on a UDP port it will appear in /proc/net/udp
            # and state will be '07'
            if line[3] != "07":
                continue

            ports.append(str(int(line[1].split(":", 1)[1], 16)))

        return ports

    def get_addr(self, port):
        if tests_inside_container():
            return (self.ips.primary, int(port.split("/")[0]))
        else:
            return ("127.0.0.1", self.ports[port][0])
