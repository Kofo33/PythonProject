from ..utils.helpers import hash_password
from ..models.user import users, current_user

def verify_current_password() -> bool:
    password = input("Enter your password to verify: ").strip()
    if not password:
        print("Password cannot be empty")
        return False
    return hash_password(password) == current_user['password_hash']