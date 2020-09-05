class TimeoutError(Exception):
    pass


class ContainerError(Exception):
    def __init__(self, container, *args, **kwargs):
        self._container = container
        super().__init__(*args, **kwargs)


class ContainerFailed(ContainerError):
    pass


class ContainerNotReady(ContainerError):
    pass
