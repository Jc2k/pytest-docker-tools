import textwrap

from .templates import find_fixtures_in_params, resolve_fixtures_in_params


def build_fixture_function(callable, scope, kwargs):
    name = callable.__name__
    docstring = getattr(callable, '__doc__', '').format(**kwargs)
    fixtures = find_fixtures_in_params(kwargs).union(set(('request', 'docker_client')))
    fixtures_str = ','.join(fixtures)

    template = textwrap.dedent(f'''
    import pytest

    @pytest.fixture(scope=scope)
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
        'scope': scope,
    }
    exec(template, globals)
    return globals[name]


def fixture_factory(scope='function'):
    def inner(callable):
        def factory(*, scope=scope, **kwargs):
            return build_fixture_function(callable, scope, kwargs)
        factory.__name__ = callable.__name__
        factory.__doc__ = getattr(callable, '__doc__', '')
        return factory
    return inner
