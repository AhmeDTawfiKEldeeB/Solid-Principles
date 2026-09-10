from abc import ABC, abstractmethod


class BankAccount(ABC):

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    @abstractmethod
    def calculate_interest(self):
        """Calculate interest specific to this account type."""
        pass


class InterestCalculator:

    def calculate_interest(self, account: BankAccount):
        return account.calculate_interest()


class AccountFormatter:

    def to_json(self, account):
        return {
            "owner": account.owner,
            "balance": account.balance,
            "account_type": type(account).__name__,
        }
