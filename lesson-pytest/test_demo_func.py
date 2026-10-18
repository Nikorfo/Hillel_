import pytest

from shop import split_bill, old_username, username


# def test_float():
#     assert 0.1 + 0.1 + 0.1 == 0.3

def test_correct_float():
    # 3.33001
    # 3.33002
    assert split_bill( 10, 3 ) == pytest.approx(3.33, abs=0.01)


def test_split_bill_fails():
    with pytest.raises(ValueError):
        split_bill(10, 0)

def test_old_username():
    with pytest.warns(DeprecationWarning, match="username"):
        old_username("a", "b")
