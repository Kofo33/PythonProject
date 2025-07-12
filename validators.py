import re

EMAIL_VALIDATE_PATTERN = r"^\S+@\S+\.\S+$"
PASSWORD_VALIDATE_PATTERN = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{16,}$"

def validate_email(mail: str) -> bool:
    return bool(re.match(EMAIL_VALIDATE_PATTERN, mail))

def validate_password(password: str) -> bool:
    return bool(re.match(PASSWORD_VALIDATE_PATTERN, password))