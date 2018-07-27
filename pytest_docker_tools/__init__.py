'''
An opionated set of helpers for defining Docker integration test environments with py.test fixtures.
'''

from .factories import build, container, fetch, network, volume


__version__ = '0.0.5'


__all__ = [
    'build',
    'container',
    'fetch',
    'network',
    'volume',
]
