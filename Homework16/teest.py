

class Account:
    "Банківський рахунок є 1 публічним методом withdraw "

    def __init__(self, balance: float, overdraft_limit: float = 0):
        self._balance = balance
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> float:
        
        if amount <= 0:
            raise ValueError("Сума має бути + ")

        if amount <= self._balance:
            self._balance -= amount
        elif amount <= self._balance + self._overdraft_limit:
            self._balance -= amount
        else:
            raise ValueError("Недостатньо коштів ")

        return self._balance



def test_withdraw_regular():
    acc = Account(balance=100)
    assert acc.withdraw(30) == 70
    assert acc.withdraw(70) == 0


def test_withdraw_uses_overdraft():
    acc = Account(balance=50, overdraft_limit=100)
    assert acc.withdraw(120) == -70
    assert acc.withdraw(30) == -100


def test_withdraw_rejects_non_positive_amount():
    acc = Account(balance=100)
    for bad in (0, -5):
        try:
            acc.withdraw(bad)
            assert False, "Очікувався ValueError "
        except ValueError as e:
             assert str(e) == "Сума має бути додатною "
    assert acc.withdraw(1) == 99  


def test_withdraw_rejects_over_limit_and_keeps_balance():
    acc = Account(balance=50, overdraft_limit=100)
    try:
        acc.withdraw(151)
        assert False, "Очікувався ValueError "
    except ValueError as e:
        assert str(e) == "Недостатньо коштів "
    assert acc.withdraw(150) == -100  


def test_no_overdraft_by_default():
    acc = Account(balance=10)
    try:
        acc.withdraw(10.01)
        assert False, "Очікувався ValueError "
    except ValueError:
        pass


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        print(f"OK  {t.__name__}")
    print(f"Усі тести пройдено: {len(tests)}")



