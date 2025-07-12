import os
import random
import string
import hashlib

def ensure_data_directory():
    if not os.path.exists('data'):
        os.makedirs('data')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_password() -> str:
    numbers_pass_chars = string.digits
    lower_pass_chars = string.ascii_lowercase
    upper_pass_chars = string.ascii_uppercase
    sym_pass_chars = string.punctuation

    password = [
        random.choice(numbers_pass_chars),
        random.choice(lower_pass_chars),
        random.choice(upper_pass_chars),
        random.choice(sym_pass_chars)
    ]
    all_pass_chars = numbers_pass_chars + lower_pass_chars + upper_pass_chars + sym_pass_chars[0]
    for _ in range(12):
        password.append(random.choice(all_pass_chars))
    random.shuffle(password)
    return ''.join(password)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()