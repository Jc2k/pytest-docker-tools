import textwrap

import pytest

from .templates import find_fixtures_in_params, resolve_fixtures_in_params


def build_fixture_function(callable, kwargs):
    name = callable.__name__
    docstring = getattr(callable, '__doc__', '').format(**kwargs)
    fixtures = find_fixtures_in_params(kwargs).union(set(('request', 'docker_client')))
    fixtures_str = ','.join(fixtures)

    template = textwrap.dedent(f'''
    def {name}({fixtures_str}):
        \'\'\'
        {docstring}
        \'\'\'
        real_kwargs = resolve_fixtures_in_params(request, kwargs)
        return _{name}(request, docker_client, **real_kwargs)
    ''')
    globals = {
        'resolve_fixtures_in_params': resolve_fixtures_in_params,
        f'_{name}': callable,
        'kwargs': kwargs,
    }
    exec(template, globals)
    return globals[name]


def fixture_factory(scope='function'):
    def inner(callable):
        def factory(*, scope='function', **kwargs):
            fixture_factory = build_fixture_function(callable, kwargs)
            pytest.fixture(scope=scope)(fixture_factory)
            return fixture_factory
        factory.__name__ = callable.__name__
        factory.__doc__ = getattr(callable, '__doc__', '')
        return factory
    return inner
