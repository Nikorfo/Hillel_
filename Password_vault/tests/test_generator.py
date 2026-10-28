import re

import pytest

from vault.generator import generate_password


@pytest.mark.parametrize("length", [8, 16, 32])
def test_length(length):
    assert len(generate_password(length)) == length


def test_contains_all_types():
    pwd = generate_password(20)
    assert re.search(r"[a-z]", pwd)
    assert re.search(r"[A-Z]", pwd)
    assert re.search(r"\d", pwd)
    assert re.search(r"[^a-zA-Z0-9]", pwd)


def test_no_symbols():
    assert not re.search(r"[^a-zA-Z0-9]", generate_password(30, symbols=False))


def test_no_digits():
    assert not re.search(r"\d", generate_password(30, digits=False))


def test_too_short():
    with pytest.raises(ValueError):
        generate_password(2)


def test_passwords_differ():
    assert generate_password(20) != generate_password(20)