from typing import Dict

def add_to_cart(product):
    """
    Add a product to the shopping cart and update inventory.

    If the product already exists in the cart, increments its quantity by 1.
    If it's a new product, adds it to the cart with quantity 1.
    Updates the product's stock count in the inventory.

    Args:
        product (Dict): Product dictionary containing at minimum:
                       - 'id': Unique product identifier
                       - 'name': Product name for display
                       - 'price': Product price

    Returns:
        None: Function performs side effects on global cart and products lists

    Global Variables:
        cart (list): Global shopping cart list that gets modified
        products (list): Global products inventory list that gets modified

    Note:
        - Assumes product stock validation is handled by calling function
        - Modifies global state (cart and products lists)
        - Prints confirmation message to console
    """
    global cart, products

    product_in_inventory: Dict | None = None
    for p in products:
        if p['id'] == product['id']:
            product_in_inventory = p
            break

    if not product_in_inventory:
        print(f"❌ Product '{product['name']}' not found in inventory")
        return

    if product_in_inventory['stock'] <= 0:
        print(f"❌ '{product['name']}' is out of stock")
        return

    # Find existing cart item and update quantity or add as a new item
    for item in cart:
        if item['product_id'] == product['id']:
            item['quantity'] += 1
            break
    else:
        cart.append({
            'product_id': product['id'],
            'quantity': 1,
            'name': product['name'],
            'price': product['price']
        })

    # Update inventory (we already found the product above through the validation, this is why we did the validation again)
    product_in_inventory['stock'] -= 1

    print(f"✅ Added {product['name']} to cart")
    print(f"📦 Remaining stock: {product_in_inventory['stock']}")


def update_cart_item(item_id: int, quantity: int) -> bool:
    """
      Update the quantity of an item in the shopping cart.

      Updates both the cart quantity and adjusts the product inventory accordingly.
      Handles stock validation to ensure sufficient inventory is available.

      Args:
    	  item_id (int): Index of the item in the cart (0-based)
    	  quantity (int): New quantity to set for the item

      Returns:
    	  bool: True if update was successful, False otherwise

      Global Variables:
    	  cart (list): Global shopping cart list that gets modified
    	  products (list): Global products inventory list that gets modified

      Note:
    	  - Validates item_id bounds and quantity positivity
    	  - Adjusts product stock based on quantity difference
    	  - Prints appropriate error messages for validation failures
      """
    global cart, products

    if item_id < 0 or item_id >= len(cart):
        print("❌ Invalid item number")
        return False

    if quantity <= 0:
        print("Quantity must be positive")
        return False

    product_id = cart[item_id]['product_id']
    current_quantity = cart[item_id]['quantity']

    product: Dict | None = None
    for p in products:
        if p['id'] == product_id:
            product = p
            break

    if not product:
        print("Product not found in inventory")
        return False

    # Calculate the difference in quantity
    # This is very important as it keeps the products stock value uptodate or correct.
    # That is to say; we updated the product stock when we added to cart.
    quantity_diff = quantity - current_quantity

    # Check if we have enough stock for the increase
    if quantity_diff > 0 and product['stock'] < quantity_diff:
        print(f"Only {product['stock']} additional items available in inventory")
        return False

    # Update cart quantity
    cart[item_id]['quantity'] = quantity

    # Update inventory stock (subtract the difference)
    product['stock'] -= quantity_diff

    print(f"✅ Updated {cart[item_id]['name']} quantity to {quantity}")
    print(f"📦 Remaining stock: {product['stock']}")

    return True


def remove_from_cart(item_index: int) -> bool:
    """
    Remove an item from the shopping cart and restore its quantity to product stock.

    :param item_index: Index of the item to remove from the cart (0-based)
    :return: True if item was successfully removed, False if invalid index
    """
    global cart, products

    if item_index < 0 or item_index >= len(cart):
        print("❌ Invalid item number")
        return False

    product_id: int = cart[item_index]['product_id']

    for p in products:
        if p['id'] == product_id:
            p['stock'] += cart[item_index]['quantity']
            break

    del cart[item_index]
    return True


def clear_cart() -> None:
    """
    Clear all items from the cart and restore their quantities to product stock.

    Prints a confirmation message when completed.
    """
    global cart, products

    if not cart:
        print("Cart is already empty 🛒")
        return

    for item in cart:
        for p in products:
            if p['id'] == item['product_id']:
                p['stock'] += item['quantity']
                break

    cart.clear()
    print("Cart cleared successfully! 🛒")


def view_cart() -> float:
    """
    Display the contents of the shopping cart and calculate total cost.

    Shows each cart item with quantity, individual cost, and running total.
    Handles empty cart case gracefully with appropriate message.

    :returns:
        float: Total cost of all items in the cart (0.0 if cart is empty)

    Global Variables:
        cart (List[Dict]): Global shopping cart list containing items with:
                          - 'name': Product name
                          - 'quantity': Number of items
                          - 'price': Price per unit
                          - 'product_id': Unique product identifier

    Display Format:
        - Empty cart: Shows empty cart message with emoji
        - Non-empty cart: Shows formatted list with item number, name, quantity,
          and total cost per line item, followed by grand total

    Note:
        - Uses Nigerian Naira (NGN) currency formatting
        - Handles floating-point arithmetic for price calculations
        - Returns 0.0 for empty cart to enable chaining with other functions
    """
    if not cart:
        print("\nYour cart is empty 🛒")
        return 0.0

    cart_total: float = 0.0
    print(f"\n{'===' * 8} Your Cart {'===' * 8}")

    for i, item in enumerate(cart, 1):
        product_cost: float = item['price'] * item['quantity']
        cart_total += product_cost
        print(f"{i}. {item['name']} x{item['quantity']} - NGN {product_cost:,.2f}")

    print(f"{'=' * 32}")
    print(f"Cart Total: NGN {cart_total:,.2f}")
    print(f"{'=' * 32}")

    return cart_total
