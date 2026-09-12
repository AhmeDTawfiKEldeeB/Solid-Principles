from abc import ABC, abstractmethod


class BankAccount(ABC):

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    @abstractmethod
    def calculate_interest(self):
        """Calculate interest specific to this account type."""
        pass

class WithdrawableAccount(BankAccount):
    """A base class for accounts that support withdrawals."""
    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception("Insufficient funds.")
        if amount<=0:
            raise Exception("Withdrawal amount must be positive.")
        self.balance -= amount
    

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

class BankServices:

    @staticmethod
    def process_deposit( account: BankAccount, amount: float):
        account.deposit(amount)

    @staticmethod
    def process_withdrawal(account: WithdrawableAccount, amount: float):
        account.withdraw(amount)