import sys
import time
from typing import Dict

from ..utils.helpers import generate_password, hash_password
from ..utils.validators import validate_email, validate_password
from ..services.user_service import save_users


def display_start_menu() -> None:
    """
    The function to display the start or the entry menu of the app
    :return: None
    """
    print("\n Sign In / Sign Up\n")
    print("1. Sign In")
    print("2. Sign Up")
    print("3. Exit\n")


def sign_in_user() -> bool:
    """
    Function for signing in a user with validated credentials.
    Returns: bool: True if signin was successful, False otherwise
    """
    print("\n" + "=" * 8 + "Login to your Account" + "=" * 8 + "\n")
    global current_user, users

    user_log_identity: str = input(f"Enter your Username / Email: ").strip()
    user_log_pass: str = input("Enter your password: ").strip()

    for user in users:
        if (user['username'] == user_log_identity or user['email'] == user_log_identity) \
                and user['password'] == user_log_pass:
            current_user = user
            print("\nLogin successful! 😄")
            return True

    print("\nLogin failed! Invalid credentials. 😡")
    return False


def sign_up_user() -> bool:
    """
    Function for signing up a new user with validated credentials.
    Returns: bool: True if signup was successful, False otherwise
    """
    print("\n" + "=" * 8 + "Create an Account" + "=" * 8 + "\n")
    global current_user, users

    # Username handling
    while True:
        user_reg_username: str = input(f"Enter your Username: ").strip()
        if not user_reg_username:
            print("Username cannot be empty")
            continue
        if len(user_reg_username) < 2:
            print("Username must be at least 2 characters")
            continue
        if not user_reg_username.isalnum():
            print("Username must contain only letters and numbers")
            continue
        for user in users:
            if user['username'] == user_reg_username:
                print("Username already exist! ❌")
                continue
        break

    # Email handling
    while True:
        user_reg_email: str = input("Enter your E-mail: ").strip().lower()
        if not user_reg_email:
            print("Email cannot be empty")
            continue

        if not validate_email(user_reg_email):
            print("Email is not correct! 😒")
            continue

        email_exists = False
        for user in users:
            if user['email'] == user_reg_email:
                print("Email already exist! ❌")
                email_exists = True
                break

        if not email_exists:
            break

    # Password handling

    while True:
        password_choice: str = input("Do you want to auto-gen password? [y/n]\n: ").lower().strip()
        user_reg_password: str = ""
        if password_choice in ['y', 'yes']:
            user_reg_password = generate_password()
            print(f"Your password is {user_reg_password}")
            break
        elif password_choice in ['n', 'no']:
            print("Password must be 16 characters long!")
            print("Password must contain an Uppercase letter")
            print("Password must contain a Lowercase letter")
            print("Password must contain a number")
            print("Contains at least one special character/symbol\n")

            user_pass: str = input("Enter your password: ").strip()
            if not validate_password(user_pass):
                print("Password doesn't meet requirements!")
                continue
            user_reg_password = user_pass
            break

        else:
            print("Invalid entry. Try again!")
            continue
    new_user: Dict = {
        'username': user_reg_username,
        'email': user_reg_email,
        'password_hash': hash_password(user_reg_password),
        'balance': 0
    }

    users.append(new_user)
    save_users()
    current_user = new_user
    print(f"Account created successfully for {user_reg_username}! ✅")
    return True


def handle_user_choice(choice: str) -> bool:
    """
    Process user menu selection
    :param choice:str
    :return: bool
    """
    if choice == '1':
        return sign_in_user()
    elif choice == '2':
        return sign_up_user()
    elif choice in ('3', 'exit', 'quit'):
        print("Thank you for using the app!\nShutting down...")
        time.sleep(1)
        sys.exit()
    else:
        print("Invalid entry! Please try again.")
        return False
