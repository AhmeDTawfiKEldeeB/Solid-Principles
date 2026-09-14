from solid_principles.interface_segregation.bank import (
    BankAccount,
    Investable,
)


class SavingsAccount(BankAccount):
    """A savings account.

    Only inherits from BankAccount because it does not support investments.
    """

    def calculate_interest(self) -> float:
        return self.balance * 0.05


class CheckingAccount(BankAccount):
    """A checking account.

    Only inherits from BankAccount because it does not support investments.
    """

    def calculate_interest(self) -> float:
        return self.balance * 0.02


class InvestmentAccount(BankAccount, Investable):
    """An investment account.

    Inherits from BankAccount and implements the Investable interface.
    """

    def __init__(self, owner: str, balance: float = 0.0):
        super().__init__(owner, balance)
        self.portfolio: dict[str, float] = {}

    def calculate_interest(self) -> float:
        return self.balance * 0.08

    def invest(self, amount: float, asset_name: str) -> None:
        if amount <= 0:
            raise ValueError("Investment amount must be positive.")
        if amount > self.balance:
            raise ValueError(
                f"Insufficient funds in cash balance to invest ${amount:.2f} in {asset_name}."
            )
        self.balance -= amount
        self.portfolio[asset_name] = self.portfolio.get(asset_name, 0.0) + amount
