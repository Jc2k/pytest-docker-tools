import textwrap

from .templates import find_fixtures_in_params, resolve_fixtures_in_params


def build_fixture_function(callable, scope, wrapper_class, kwargs):
    name = callable.__name__
    docstring = [
        "An instance of {}.{} created with the following:\n".format(
            name, callable.__module__
        )
    ]
    docstring.extend(f"        {key}: {value}" for key, value in kwargs.items())
    docstring = "\n".join(docstring)

    fixtures = find_fixtures_in_params(kwargs).union({"request", "docker_client"})
    fixtures_str = ",".join(fixtures)

    template = textwrap.dedent(
        f"""
    import pytest

    def {name}({fixtures_str}):
        \'\'\'
        {docstring}
        \'\'\'
        real_kwargs = resolve_fixtures_in_params(request, kwargs)
        return _{name}(request, docker_client, wrapper_class=wrapper_class, **real_kwargs)

    {name}.__module__ = callable.__module__
    {name} = pytest.fixture(scope=scope)({name})
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
