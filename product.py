products = []

class Product:
    def __init__(self, id, name, price, stock=10):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock