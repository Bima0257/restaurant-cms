import re


def validate_password(password: str, email: str = "") -> str | None:
    if len(password) < 8:
        return "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter (A-Z)"

    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter (a-z)"

    if not re.search(r"\d", password):
        return "Password must contain at least one number (0-9)"

    if not re.search(r"[@#!%\^&\*\(\)_\+\-=\[\]{};':\"\\|,.<>\/?~`]", password):
        return "Password must contain at least one special character (e.g. @, #, !, %, &)"

    if email and password.lower() == email.lower():
        return "Password cannot be the same as email"

    return None
