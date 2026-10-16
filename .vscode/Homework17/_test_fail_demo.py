import pytest

from shop import discount, delivery

@pytest.mark.parametrize("percent", [0, 50, 75, 100])
def test_discount_not_negatvie_works( percent ):
    assert discount(100, percent) >= 0


@pytest.mark.parametrize(
        ( "total", "express", "expected" ),
        [
            (100, False, 50),
            (999, False, 50),
            (1000, False, 0),
            (100, True, 150),
            (1000, True, 100),
        ],
        ids=["small", "just-below", "aaa", "bbb", "ccc"]
)
def test_delivery(total, express, expected):
    assert delivery(total, express) == expected
