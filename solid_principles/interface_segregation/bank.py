from abc import ABC, abstractmethod


class BankAccount(ABC):
    """Base class representing the core operations of any bank account."""

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    @abstractmethod
    def calculate_interest(self) -> float:
        """Calculate interest specific to this account type."""
        pass


# =====================================================================
# Segregated Interface (Only accounts that support investing implement this)
# =====================================================================


class Investable(ABC):
    """Interface for accounts that support investment capabilities."""

    @abstractmethod
    def invest(self, amount: float, asset_name: str) -> None:
        """Invest a specified amount into an asset."""
        pass


# =====================================================================
# Client Services (Each depends strictly on the interface it needs)
# =====================================================================


class BankServices:
    """General banking operations (deposit & withdraw) for any BankAccount."""

    @staticmethod
    def process_deposit(account: BankAccount, amount: float) -> None:
        account.deposit(amount)

    @staticmethod
    def process_withdrawal(account: BankAccount, amount: float) -> None:
        account.withdraw(amount)


class InvestmentService:
    """Investment platform service that ONLY depends on Investable accounts."""

    @staticmethod
    def process_investment(
        account: Investable, amount: float, asset_name: str
    ) -> None:
        account.invest(amount, asset_name)


class AccountFormatter:
    """Formatter to present account data."""

    def to_json(self, account: BankAccount) -> dict:
        return {
            "owner": account.owner,
            "balance": account.balance,
            "account_type": type(account).__name__,
        }
