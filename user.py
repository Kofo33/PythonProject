users = []
current_user = None

class User:
    def __init__(self, username, email, password_hash, balance=0):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.balance = balance
