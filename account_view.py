from ..models.user import users, current_user, cart
from ..utils.auth import verify_current_password
from ..utils.validators import validate_email, validate_password
from ..services.user_service import save_users


def display_account_menu():
    """Display account management menu"""
    print(f"\n{'===' * 8} Manage Account {'===' * 8}")
    print("1. Change Username")
    print("2. Change Email")
    print("3. Change Password")
    print("4. View Account Details")
    print("5. Reset Balance")
    print("6. Delete Account")
    print("7. Back to Store Menu")


def change_username() -> None:
    """
    Change the current user's username after password verification.

    Requires current password confirmation and ensures new username
    is not empty and unique across all users.
    """
    while True:
        if not verify_current_password():
            print("Incorrect password ❌")
            return
        new_username: str = input("Enter new username: ").strip()
        if not new_username:
            print("Username cannot be empty")
            continue
        if len(new_username) < 2:
            print("Username must be at least 2 characters")
            continue
        if not new_username.isalnum():
            print("Username must contain only letters and numbers")
            continue
        for user in users:
            if user['username'] == new_username:
                print("Username already taken! ❌")
                continue
        break

    try:
        current_user['username'] = new_username
        save_users()
        print("\nUsername updated successfully ✅")
    except Exception as e:
        print(f"Error saving username: {e}")


def change_email() -> None:
    """
    Change the current user's email address after password verification.

    Requires current password confirmation and ensures new email
    has valid format and is unique across all users.
    """
    global current_user

    if not verify_current_password():
        print("Incorrect password")
        return

    while True:
        new_email = input("Enter new email: ").strip().lower()
        if not validate_email(new_email):
            print("Email is not correct! 😒")
            continue

        email_exists = False
        for user in users:
            if user['email'] == new_email:
                print("Email already exist! ❌")
                email_exists = True
                break
        if not email_exists:
            break
        break
    try:
        current_user['email'] = new_email
        save_users()
        print("\nEmail updated successfully! 📧")
    except Exception as e:
        print(f"Error saving email: {e}")


def change_password() -> None:
    """
    Change the current user's password after verification.

    Requires current password confirmation and ensures new password
    meets security requirements (16+ chars, uppercase, lowercase,
    number, special character). Final confirmation before applying changes.
    """
    global current_user

    if not verify_current_password():
        print("Incorrect password")
        return

    print("\nNew password must be at least 16 characters with:")
    print("- At least one uppercase letter")
    print("- At least one lowercase letter")
    print("- At least one number")
    print("- At least one special character")

    while True:
        new_password = input("Enter new password: ").strip()
        if not validate_password(new_password):
            print("Password does not meet requirements")
            continue

        confirm_password = input("Confirm new password: ").strip()
        if new_password != confirm_password:
            print("Passwords do not match")
            continue
        if hash_password(new_password) == current_user['password_hash']:
            print("New password cannot be the same as current password")
            continue
        break

    confirm = input("Are you sure you want to change your password? (y/n): ").strip().lower()
    if confirm == 'y':

        try:
            save_users()
            print("\nPassword changed successfully ✅")
        except Exception as e:
            print(f"Error saving password: {e}")
    else:
        print("\nPassword change cancelled")


def view_account_details() -> None:
    """
    Display the current user's account information after password verification.

    Shows username, email, and current wallet balance.
    Requires password confirmation for security.
    """
    if not verify_current_password():
        print("Incorrect password")
        return

    print("\n" + "=" * 30)
    print("      ACCOUNT DETAILS")
    print("=" * 30)
    print(f"Username:  {current_user['username']}")
    print(f"Email:     {current_user['email']}")
    print(f"Balance:   NGN {current_user['balance']:,.2f}")
    print("\n" + "=" * 30)


def reset_balance() -> None:
    """
    Reset the current user's wallet balance to zero.

    Requires password verification and user confirmation before proceeding.
    This action is irreversible and will permanently remove all funds.
    """
    global current_user

    if not verify_current_password():
        print("Incorrect password")
        return
    print(f"\nCurrent balance: NGN {current_user['balance']:,.2f}")
    confirm: str = input("Are you sure you want to reset your balance to zero? (y/n): ").strip().lower()
    if confirm == 'y':
        if current_user['balance'] > 50000:  # For large amounts
            print("⚠️  WARNING: You have a significant balance!")
            confirm_again: str = input("Type 'RESET' to confirm: ").strip()
            if confirm_again != 'RESET':
                print("\nBalance reset cancelled")
                return
        current_user['balance'] = 0.0
        try:
            save_users()
            print("\nBalance reset to zero ✅")
        except Exception as e:
            print(f"Error saving balance reset: {e}")
    else:
        print("\nBalance reset cancelled")


def delete_account() -> bool:
    def delete_account() -> bool:
        """
        Delete the current user's account after verification and confirmation.

        Requires password verification and explicit user confirmation.
        Removes user from system, clears current session, and returns to main menu.

        Returns:
            bool: True if account was deleted, False if cancelled or failed
        """
        global current_user, users, cart

        if not verify_current_password():
            print("Incorrect password")
            return False

        if current_user['balance'] > 0:
            print(f"⚠️  WARNING: You have NGN {current_user['balance']:,.2f} in your wallet!")
            print("This balance will be permanently lost if you delete your account.")

        confirm = input("ARE YOU SURE YOU WANT TO DELETE YOUR ACCOUNT? THIS CANNOT BE UNDONE! (y/n): ").strip().lower()
        if confirm == 'y':
            confirm2 = input("Type 'DELETE' to confirm deletion: ").strip()
            if confirm2 != 'DELETE':
                print("\nAccount deletion cancelled")
                return False
            users.remove(current_user)
            try:
                save_users()
                current_user = None
                cart = []
                print("\nAccount deleted successfully. Returning to main menu. 🗑️")
                return True
            except Exception as e:
                print(f"Error deleting account: {e}")
                # Could potentially restore user to list
                return False
        else:
            print("\nAccount deletion cancelled")
            return False


def account_menu() -> None:
    """
    Handle account management menu operations.

    Provides options for users to modify account settings including username,
    email, password, view details, reset balance, and delete account.
    Continues until user chooses to exit or account is deleted.
    """
    while True:
        display_account_menu()
        user_choice: str = input("Enter choice (1-7): ").strip()
        if user_choice == '1':
            change_username()
        elif user_choice == '2':
            change_email()
        elif user_choice == '3':
            change_password()
        elif user_choice == '4':
            view_account_details()
        elif user_choice == "5":
            reset_balance()
        elif user_choice == "6":
            if delete_account():
                return  # Return to main menu if account deleted
        elif user_choice == "7":
            break
        else:
            print("Invalid choice")
