import pytest

from pytest_docker_tools.utils import check_signature, hash_params, set_signature


def test_hash_params():
    """
    Test generating signatures for fixture factory kwargs.
    """
    assert (
        hash_params(
            {
                "name": "my-name",
                "labels": {
                    "label1": "label",
                },
            }
        )
        == "1c67a2e8dd405725a4cdf7b58fed3e948aed135ac25c494a3b336c83a72ac0c8"
    )


def test_hash_params_raises():
    """
    Make sure that we still catch invalid kwargs when generating signature hashes.

    This is really just to get full coverage of the JSONEncoder subclass.
    We shouldn't hit this exception on the happy path.
    """
    with pytest.raises(TypeError):
        hash_params(
            {
                "name": "my-name",
                "labels": {
                    "label1": object(),
                },
            }
        )


def test_check_signature():
    signature = "1c67a2e8dd405725a4cdf7b58fed3e948aed135ac25c494a3b336c83a72ac0c8"
    labels = {
        "pytest-docker-tools.signature": signature,
    }

    assert check_signature(labels, signature)


def test_set_signature_no_existing_labels():
    signature = "1c67a2e8dd405725a4cdf7b58fed3e948aed135ac25c494a3b336c83a72ac0c8"

    kwargs = {
        "name": "hello",
        "image": "alpine:3.13",
    }
    set_signature(kwargs, signature)

    assert kwargs == {
        "name": "hello",
        "image": "alpine:3.13",
        "labels": {
            "pytest-docker-tools.signature": signature,
        },
    }


def test_set_signature_preserve_labels():
    signature = "1c67a2e8dd405725a4cdf7b58fed3e948aed135ac25c494a3b336c83a72ac0c8"

    kwargs = {
        "name": "hello",
        "image": "alpine:3.13",
        "labels": {
            "mylabel": "hello",
        },
    }
    set_signature(kwargs, signature)

    assert kwargs == {
        "name": "hello",
        "image": "alpine:3.13",
        "labels": {
            "mylabel": "hello",
            "pytest-docker-tools.signature": signature,
        },
    }
