from typing import Any

from docker.models.containers import Container


class TimeoutError(Exception):
    pass


class ContainerError(Exception):
    def __init__(self, container: Container, *args: Any, **kwargs: Any) -> None:
        self._container = container
        super().__init__(*args, **kwargs)


class ContainerFailed(ContainerError):
    pass


class ContainerNotReady(ContainerError):
    pass
