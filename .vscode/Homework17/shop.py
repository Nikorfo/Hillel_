import pytest
import sqlite3

from shop import profile


@pytest.fixture
def test_fixture():
    return 10

@pytest.fixture
def ann():
    return profile("Ann", "Lee", "test@email.ua")

@pytest.fixture
def make_user():
    def _make( first="Ann", last="Lee", email="test@email.ua" ):
        return profile(first, last, email)
    return _make


@pytest.fixture
def db():
    # setup
    print("\n [DB] -- open")
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE users (name TEXT)")

    yield connection        # ТУТ відбувається тест

    # tear down
    connection.close()
    print("\n [DB] -- closed")


@pytest.fixture(scope="module")
def settings():
    return {} 


@pytest.fixture(params=["UAH", "USD", "EUR"])
def code(request):
    return request.param

@pytest.fixture(autouse=True)
def test_prepare():
    # PREPARE
    yield
    # TEAR DOWN
