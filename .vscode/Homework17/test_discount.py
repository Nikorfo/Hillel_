import pytest

from shop import discount

def test_discount_10_percent():
    assert discount( 100, 10  ) == 90

def test_discount_zero_percent():
    assert discount( 100, 0   )  == 100

def test_discount_over_100_percent_raises():
    with pytest.raises(ValueError):
        discount( 100, 150 )