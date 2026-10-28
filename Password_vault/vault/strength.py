import re

SEQUENCES = ("0123", "1234", "2345", "3456", "4567", "5678", "6789",
             "abcd", "qwer", "asdf", "zxcv")


def evaluate(password: str):
    """Повертає (рівень, список порад)."""
    score, tips = 0, []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        tips.append("Використай щонайменше 8 символів (ліпше 12+)")

    checks = [
        (r"[a-z]", "малі літери"),
        (r"[A-Z]", "великі літери"),
        (r"\d", "цифри"),
        (r"[^a-zA-Z0-9\s]", "спеціальні символи"),
    ]
    for pattern, name in checks:
        if re.search(pattern, password):
            score += 1
        else:
            tips.append(f"Додай {name}")

    if re.search(r"(.)\1{2,}", password):
        score -= 1
        tips.append("Уникай повторів одного символу поспіль")
    if any(seq in password.lower() for seq in SEQUENCES):
        score -= 1
        tips.append("Уникай послідовностей типу 1234 або qwer")
    if re.search(r"(?i)password|qwerty|admin", password):
        score -= 2
        tips.append("Не використовуй поширені слова (password, qwerty, admin)")

    level = "слабкий" if score <= 2 else "середній" if score <= 4 else "сильний"
    return level, tips
