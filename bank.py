class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount


class InterestCalculator:

    def calculate_interest(self, account):
        return account.balance * 0.05


class AccountFormatter:

    def to_json(self, account):
        return {
            "owner": account.owner,
            "balance": account.balance,
        }