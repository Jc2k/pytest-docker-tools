'''
An opionated set of helpers for defining Docker integration test environments with py.test fixtures.
'''

from .factories import build, container, fetch, image, image_or_build, network, volume


__version__ = '0.0.12'


__all__ = [
    'build',
    'container',
    'fetch',
    'image',
    'image_or_build',
    'network',
    'volume',
]
