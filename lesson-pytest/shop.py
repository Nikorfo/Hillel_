import json
import logging
import os
import random
import warnings


def discount(price, percent):
    if not 0 <= percent <= 100:
        raise ValueError(f"percent must be 0..100, got {percent}")
    return round(price * (1 - percent / 100), 2)


def delivery(total, express=False):
    price = 0 if total >= 1000 else 50
    if express:
        price += 100
    return price


def split_bill(total, people):
    if people <= 0:
        raise ValueError("people must be > 0")
    return total / people


def username(first, last):
    return f"{first}.{last}".lower()


def profile(first, last, email):
    if "@" not in email:
        raise ValueError(f"bad email: {email}")
    return {"username": username(first, last), "email": email.lower(), "roles": ["customer"]}


def old_username(first, last):
    warnings.warn("use username()", DeprecationWarning)
    return username(first, last)


def receipt(items):
    for name, price in items.items():
        print(f"{name}: {price}")
    print(f"TOTAL: {sum(items.values())}")


def save_cart(items, path):
    path.write_text(json.dumps(items))


def load_cart(path):
    if not path.exists():
        logging.warning("cart file not found")
        return {}
    return json.loads(path.read_text())


def lucky_discount():
    return 10 if random.random() < 0.1 else 0


def currency():
    return os.environ.get("SHOP_CURRENCY", "UAH")
