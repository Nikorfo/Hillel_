import pytest

from vault.strength import evaluate


@pytest.mark.parametrize(
    "pwd, level",
    [
        ("abc", "слабкий"),
        ("password", "слабкий"),
        ("Abcdef12", "середній"),
        ("xK9#mQ2$vL7!pR", "сильний"),
    ],
)
def test_levels(pwd, level):
    assert evaluate(pwd)[0] == level


def test_tip_for_short_password():
    _, tips = evaluate("abc")
    assert any("8 символів" in t for t in tips)


def test_repeats_detected():
    _, tips = evaluate("aaaXk9#mQ2$v")
    assert any("повтор" in t for t in tips)


def test_sequence_detected():
    _, tips = evaluate("Xk1234#mQ2$v")
    assert any("послідовност" in t for t in tips)


def test_common_word_detected():
    _, tips = evaluate("MyPassword#99")
    assert any("поширені" in t for t in tips) 
