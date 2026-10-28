import sqlite3

import pytest

from vault import crypto, db

SALT = b"0123456789abcdef"


@pytest.fixture(autouse=True)
def fast_kdf(mocker):
    """Менше ітерацій, щоб тести були швидкими"""
    mocker.patch("vault.crypto.ITERATIONS", 1000)


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row 
    db.init_schema(c)
    yield c
    c.close()


@pytest.fixture
def key():
    return crypto.derive_key("master-pass", SALT)
 