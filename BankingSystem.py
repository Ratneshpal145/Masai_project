import os
import hashlib

class BankSystem:
    def __init__(self):
        self.users_file = 'users.txt'
        self.transactions_file = 'transactions.txt'
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password_hash, balance = line.strip().split(',')
                    self.users[username] = {'password_hash': password_hash, 'balance': float(balance)}

    def save_users(self):
        with open(self.users_file, 'w') as file:
            for username, data in self.users.items():
                file.write(f"{username},{data['password_hash']},{data['balance']}\n")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self, username, password):
        if username in self.users:
            print("Username already exists.")
            return False
        self.users[username] = {'password_hash': self.hash_password(password), 'balance': 0.0}
        self.save_users()
        print("Account created successfully.")
        return True

    def login(self, username, password):
        if username in self.users and self.users[username]['password_hash'] == self.hash_password(password):
            print("Login successful.")
            return True
        print("Invalid username or password.")
        return False

    def log_transaction(self, username, transaction):
        with open(self.transactions_file, 'a') as file:
            file.write(f"{username},{transaction}\n")

    def deposit(self, username, amount):
        if amount <= 0:
            print("Invalid amount.")
            return False
        self.users[username]['balance'] += amount
        self.save_users()
        self.log_transaction(username, f"Deposit: {amount}")
        print(f"Deposited {amount}. New balance: {self.users[username]['balance']}")
        return True

    def withdraw(self, username, amount):
        if amount <= 0 or amount > self.users[username]['balance']:
            print("Invalid amount.")
            return False
        self.users[username]['balance'] -= amount
        self.save_users()
        self.log_transaction(username, f"Withdraw: {amount}")
        print(f"Withdrew {amount}. New balance: {self.users[username]['balance']}")
        return True

    def check_balance(self, username):
        print(f"Current balance: {self.users[username]['balance']}")
        return self.users[username]['balance']

def main():
    bank_system = BankSystem()
    while True:
        print("\n1. Create Account\n2. Login\n3. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            bank_system.create_account(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if bank_system.login(username, password):
                while True:
                    print("\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Logout")
                    choice = input("Enter choice: ")
                    if choice == '1':
                        amount = float(input("Enter amount to deposit: "))
                        bank_system.deposit(username, amount)
                    elif choice == '2':
                        amount = float(input("Enter amount to withdraw: "))
                        bank_system.withdraw(username, amount)
                    elif choice == '3':
                        bank_system.check_balance(username)
                    elif choice == '4':
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()