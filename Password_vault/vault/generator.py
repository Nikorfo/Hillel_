import secrets
import string

SYMBOLS = "!@#$%^&*()-_=+[]{}"


def generate_password(length=16, upper=True, digits=True, symbols=True) -> str:
    pools = [string.ascii_lowercase]
    if upper:
        pools.append(string.ascii_uppercase)
    if digits:
        pools.append(string.digits)
    if symbols:
        pools.append(SYMBOLS)

    if length < len(pools):
        raise ValueError(f"Мінімальна довжина для обраних наборів: {len(pools)}")

    alphabet = "".join(pools)
    chars = [secrets.choice(pool) for pool in pools]
    chars += [secrets.choice(alphabet) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

