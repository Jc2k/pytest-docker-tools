import os

from .build import build
from .image import image


def image_or_build(environ_key, **kwargs):
    if environ_key in os.environ:
        return image(name=os.environ[environ_key])
    return build(**kwargs)
