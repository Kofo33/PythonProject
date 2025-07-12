import time

from ..models.user import current_user
from ..views.purchase_view import purchase_menu
from ..views.account_view import account_menu

from ..services.user_service import save_users
from ..utils.helpers import clear_screen


def display_dashboard_menu() -> None:
    clear_screen()
    print(f"\n{"===" * 8} Welcome, {current_user['username']} {"===" * 8}")
    print("1. Fund Wallet")
    print("2. Purchase Items")
    print("3. Manage Account")
    print("4. Logout")


def fund_wallet() -> None:
    """
    Add funds to the current user's wallet balance.

    Provides predefined amounts (10k, 20k, 50k, 100k) and custom amount option.
    Updates the user's balance and displays confirmation.
    """
    global current_user

    print("\n=== Fund Wallet ===")
    print(f"Current balance: NGN {current_user['balance']:,.2f}")

    options = {
        '1': 10000,
        '2': 20000,
        '3': 50000,
        '4': 100000,
        '5': "Custom Amount"
    }

    for key, value in options.items():
        print(f"{key}. NGN {value:,.2f}" if isinstance(value, int) else f"{key}. {value}")

    while True:
        fund_choice: str = input("Select amount to add (1-5): ").strip()
        if fund_choice in options:
            if fund_choice == '5':
                try:
                    amount: float = float(input("Enter custom amount: "))
                    if amount <= 0:
                        print("Amount must be a positive number 😒")
                        continue
                    elif amount > 100000000:  # Example limit
                        print("Maximum funding amount is NGN 100,000,000 at a time 🫤")
                        continue
                except ValueError:
                    print("Invalid amount ❌")
                    continue
            else:
                amount = options[fund_choice]

            current_user['balance'] += amount
            # save to the doc
            save_users()
            print(f"\nProcessing payment of NGN {amount:,.2f}...")
            time.sleep(1)
            print("Payment successful! ✅")
            break

        else:
            print("Invalid Entry! 💢")


def dashboard():
    """
    A Function for the dashboard menu
    :return:
    """
    while True:
        display_dashboard_menu()
        dashboard_choice: str = input("Enter choice (1-4): ").strip()

        if dashboard_choice == "1":
            fund_wallet()
        elif dashboard_choice == "2":
            purchase_menu()
        elif dashboard_choice == "3":
            account_menu()
        elif dashboard_choice == "4":
            global current_user, cart
            current_user = None
            cart = []
            break
        else:
            print("Invalid choice")
