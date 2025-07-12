import os
from ..models.user import users
from ..utils.helpers import ensure_data_directory


def load_users() -> None:
    """
    Load user accounts from data/accounts.txt file.

    Reads CSV format: username,email,password_hash,balance
    Skips empty lines and malformed entries. Creates empty users list
    if file doesn't exist.
    """
    global users
    users = []
    try:
        with open('data/accounts.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    username, email, password_hash, balance = line.split(',')
                    if not username.strip() or not email.strip() or not password_hash.strip():
                        continue
                    balance_float = float(balance.strip())
                    if balance_float < 0:
                        continue
                    users.append({
                        'username': username.strip(),
                        'email': email.strip(),
                        'password_hash': password_hash.strip(),
                        'balance': float(balance.strip())
                    })
                except ValueError:
                    continue
    except (FileNotFoundError, PermissionError) as e:
        print(f"Could not load users: {e}")


def save_users():
    ensure_data_directory()
    with open('data/accounts.txt', 'w') as f:
        for user in users:
            line = f"{user['username']},{user['email']},{user['password_hash']},{user['balance']}\n"
            f.write(line)
