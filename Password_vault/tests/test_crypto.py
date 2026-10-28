import pytest
from cryptography.fernet import InvalidToken

from vault import crypto


def test_roundtrip(key):
    token = crypto.encrypt(key, "secret")
    assert crypto.decrypt(key, token) == "secret"


def test_token_does_not_contain_plaintext(key):
    assert b"secret" not in crypto.encrypt(key, "secret")


def test_wrong_key_fails(key):
    token = crypto.encrypt(key, "secret")
    other = crypto.derive_key("other-pass", b"0123456789abcdef")
    with pytest.raises(InvalidToken):
        crypto.decrypt(other, token)


def test_verify_key(key):
    check = crypto.make_check(key)
    assert crypto.verify_key(key, check) is True
    wrong = crypto.derive_key("wrong", b"0123456789abcdef")
    assert crypto.verify_key(wrong, check) is False


def test_salts_are_unique():
    assert crypto.new_salt() != crypto.new_salt()


def test_same_password_different_salt_gives_different_key():
    assert crypto.derive_key("p", b"a" * 16) != crypto.derive_key("p", b"b" * 16)


def test_same_password_same_salt_gives_same_key():
    assert crypto.derive_key("p", b"a" * 16) == crypto.derive_key("p", b"a" * 16)
    