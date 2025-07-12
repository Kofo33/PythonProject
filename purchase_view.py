import time
from typing import List

from ..models.user import current_user
from ..models.cart import cart
from ..services.cart_service import view_cart, add_to_cart, update_cart_item, remove_from_cart, clear_cart
from ..services.product_service import products

from ..services.user_service import save_users


def display_purchase_menu():
    """
    Display purchase menu
    :return:None
    """
    print(f"\n{'===' * 8} Purchase Items {'===' * 8}")
    print("1. Search Items")
    print("2. Manage Cart")
    print("3. Checkout")
    print("4. Back to Store Menu")


def search_products():
    """
    Search for products in inventory based on user input.

    Prompts user for search terms and searches through the global products list.
    Performs case-insensitive partial matching on product names.
    If multiple search terms are provided, matches products containing ANY of the terms.

    Returns:
        List[Dict]: List of matching product dictionaries. Each product contains:
                   - 'id': Unique product identifier
                   - 'name': Product name
                   - 'price': Product price
                   - 'stock': Available stock quantity
                   Returns empty list if no matches found or invalid input.

    Global Variables:
        products (List[Dict]): Global inventory list that gets searched

    Note:
        - Performs partial string matching (case-insensitive)
        - Displays formatted search results to console
        - Handles empty input gracefully
        - Avoids duplicate results when multiple terms match same product
    """
    query = input("\nEnter search query: ").strip()
    if not query:
        print("Please enter a search term")
        return []

    search_terms: List[str] = query.split()
    results = []

    for product in products:
        for term in search_terms:
            if term.lower() in product['name'].lower():
                results.append(product)

    if not results:
        print("\nNo matching items found")
        return []

    print("\n=== Search Results ===")
    for i, product in enumerate(results, 1):
        print(f"{i}. {product['name']} - NGN {product['price']:,.2f} ({product['stock']} available)")

    return results


def handle_search_results(results: list[dict]) -> None:
    """
    Handle user interactions with search results.

    Displays a menu allowing users to:
    1. Add a selected item to their cart (with stock validation)
    2. Perform a new search
    3. Return to the purchase menu

    Args:
        results (list[dict]): List of product dictionaries from search results.
                            Each product should contain 'id', 'name', 'price', and 'stock' keys.

    Returns:
        None

    Note:
        - Validates item selection bounds and stock availability
        - Handles invalid input gracefully with error messages
        - Continues looping until user chooses to search again or go back
    """
    while True:
        print("\n1. Add to Cart")
        print("2. Search Again")
        print("3. Back to Purchase Menu")

        choice: str = input("Enter choice (1-3): ").strip()

        if choice == "1":
            try:
                selection: int = int(input("Enter item number to add: ")) - 1
                if 0 <= selection < len(results):
                    product = results[selection]
                    if product['stock'] <= 0:
                        print("❌ Item out of stock")
                        continue
                    add_to_cart(product)
                else:
                    print("💢 Invalid item number!")
            except ValueError:
                print("Invalid input")
        elif choice == "2":
            search_products()
            break
        elif choice == "3":
            break
        else:
            print("Invalid choice")


def handle_cart_management() -> None:
    """
    Interactive menu for managing cart items (modify quantity, remove items, clear cart).

    Continues until user chooses to exit or cart becomes empty.
    """
    print("Handle cart Management")
    while True:
        total: float = view_cart()
        if not cart:
            print("Cart is empty! 🛒")
            break
        if total == 0.0:
            break

        print("\n1. Change Quantity")
        print("2. Remove Item")
        print("3. Clear Cart")
        print("4. Back to Purchase Menu")

        user_choice: str = input("Enter choice (1-4): ").strip()

        if user_choice == "1":
            try:
                item_id: int = int(input("Enter item number to modify: ")) - 1
                new_quantity: int = int(input("Enter new quantity: "))
                update_cart_item(item_id, new_quantity)
            except ValueError:
                print("❌ Please enter a valid number")
        elif user_choice == "2":
            try:
                selected_item_index: int = int(input("Enter item number to remove: ")) - 1
                remove_from_cart(selected_item_index)
            except ValueError:
                print("❌ Please enter a valid number")
        elif user_choice == "3":
            confirm = input("Are you sure you want to clear the cart? (y/n): ").lower()
            if confirm == 'y':
                clear_cart()
                break
        elif user_choice == "4":
            break
        else:
            print("Invalid choice")


def checkout():
    """
    Process checkout for items in cart.

    Validates sufficient wallet balance, confirms purchase with user,
    deducts total from balance, and clears cart upon successful purchase.
    """
    global current_user, cart

    total = view_cart()
    if total == 0:
        return

    print(f"\nOrder Summary:")
    print(f"Total Amount: NGN {total:,.2f}")
    print(f"Your Balance: NGN {current_user['balance']:,.2f}")
    print(f"Balance After Purchase: NGN {current_user['balance'] - total:,.2f}")

    if total > current_user['balance']:
        print("\nInsufficient funds. Please fund your wallet.")
        return

    confirm = input("\nConfirm purchase (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            transaction_id = f"TXN{int(time.time())}"  # Simple transaction ID to mock real transaction id
            current_user['balance'] -= total
            save_users()
            cart.clear()
            print(f"\n✅ Purchase successful! Transaction ID: {transaction_id}")
            print("Thank you for your order. 💳")
        except Exception as e:
            print(f"❌ Error saving transaction: {e}")

    else:
        print("\n❌ Purchase cancelled")


def purchase_menu():
    """
    Main purchase menu interface.

    Provides options for product search, cart management, checkout, and exit.
    Continues until user chooses to exit.
    """
    while True:
        display_purchase_menu()
        purchase_choice: str = input("Enter choice (1-4): ").strip()
        if purchase_choice == "1":
            results = search_products()
            if results:
                handle_search_results(results)
        elif purchase_choice == "2":
            handle_cart_management()
        elif purchase_choice == "3":
            if cart:
                checkout()
            else:
                print("Your cart is empty! Add items before checkout.")
        elif purchase_choice == "4":
            break
        else:
            print("Invalid choice! Please enter 1-4 💢")
