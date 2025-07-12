from services.user_service import load_users
from services.product_service import load_products
from views.auth_view import display_start_menu, handle_user_choice
from views.dashboard_view import dashboard

def main():
    load_users()
    load_products()

    print("Welcome to the E-Commerce App! 💳")

    while True:
        display_start_menu()
        user_choice = input(
            "Do you wish to Sign In or Sign Up? Enter [1-3]\n[To exit, enter 'quit'/'exit']: ").strip().lower()
        if handle_user_choice(user_choice) and current_user:
            dashboard()

if __name__ == "__main__":
    main()