cart = []

class CartItem:
    def __init__(self, product_id, quantity, name, price):
        self.product_id = product_id
        self.quantity = quantity
        self.name = name
        self.price = price