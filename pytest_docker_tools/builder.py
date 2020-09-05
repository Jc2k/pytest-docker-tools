import textwrap

from .templates import find_fixtures_in_params, resolve_fixtures_in_params


def build_fixture_function(callable, scope, wrapper_class, kwargs):
    name = callable.__name__
    docstring = "Docker image"
    if "path" in kwargs:
        docstring = getattr(callable, "__doc__", "").format(**kwargs)
    fixtures = find_fixtures_in_params(kwargs).union({"request", "docker_client"})
    fixtures_str = ",".join(fixtures)

    template = textwrap.dedent(
        f"""
    import pytest

    @pytest.fixture(scope=scope)
    def {name}({fixtures_str}):
        \'\'\'
        {docstring}
        \'\'\'
        real_kwargs = resolve_fixtures_in_params(request, kwargs)
        return _{name}(request, docker_client, wrapper_class=wrapper_class, **real_kwargs)
    """
    )
    globals = {
        "resolve_fixtures_in_params": resolve_fixtures_in_params,
        f"_{name}": callable,
        "kwargs": kwargs,
        "scope": scope,
        "wrapper_class": wrapper_class,
    }
    exec(template, globals)
    return globals[name]


def fixture_factory(scope="function"):
    wrapper_class = None

    def inner(callable):
        def factory(*, scope=scope, wrapper_class=wrapper_class, **kwargs):
            return build_fixture_function(callable, scope, wrapper_class, kwargs)

        factory.__name__ = callable.__name__
        factory.__doc__ = getattr(callable, "__doc__", "")
        return factory

    return inner
