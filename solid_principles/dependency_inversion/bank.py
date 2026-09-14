from abc import ABC, abstractmethod


# =====================================================================
# Core Domain Models (Carried over from Interface Segregation)
# =====================================================================


class BankAccount(ABC):
    """Base class representing the fundamental identity and operations of an account."""

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
            raise ValueError(f"Insufficient funds for {self.owner}.")
        self.balance -= amount

    @abstractmethod
    def calculate_interest(self) -> float:
        """Calculate interest specific to this account type."""
        pass


class Investable(ABC):
    """Segregated interface for accounts that support market investments (ISP)."""

    @abstractmethod
    def invest(self, amount: float, asset_name: str) -> None:
        pass


# =====================================================================
# Abstraction Layer (DIP: Both High-Level & Low-Level depend on this)
# =====================================================================


class Notifier(ABC):
    """Abstract interface for sending notifications.

    High-level services depend on this abstraction, NOT on concrete delivery tools.
    """

    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        """Send a notification message to the recipient."""
        pass


# =====================================================================
# Low-Level Concrete Implementations (Details that depend on Notifier)
# =====================================================================


class SMSNotifier(Notifier):
    """Low-level module: Sends SMS text messages."""

    def send(self, recipient: str, message: str) -> None:
        print(f"[SMS to {recipient}]: {message}")


class EmailNotifier(Notifier):
    """Low-level module: Sends emails."""

    def send(self, recipient: str, message: str) -> None:
        print(f"[Email to {recipient}@bank.com]: {message}")


class PushNotificationService(Notifier):
    """Low-level module: Sends mobile app push notifications."""

    def send(self, recipient: str, message: str) -> None:
        print(f"[Push Alert to {recipient}'s App]: {message}")


# =====================================================================
# High-Level Service (DIP: Depends strictly on Notifier abstraction via DI)
# =====================================================================


class BankTransactionService:
    """High-level module managing customer transactions.

    Applies Dependency Inversion: depends on the Notifier abstraction,
    injected through the constructor (Dependency Injection).
    """

    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def set_notifier(self, notifier: Notifier) -> None:
        """Allows swapping the notification tool dynamically at runtime."""
        self.notifier = notifier

    def process_deposit(self, account: BankAccount, amount: float) -> None:
        account.deposit(amount)
        self.notifier.send(
            account.owner,
            f"Deposited ${amount:.2f}. New Balance: ${account.balance:.2f}",
        )

    def process_withdrawal(self, account: BankAccount, amount: float) -> None:
        account.withdraw(amount)
        self.notifier.send(
            account.owner,
            f"Withdrew ${amount:.2f}. Remaining Balance: ${account.balance:.2f}",
        )

    def process_investment(
        self, account: Investable, amount: float, asset_name: str
    ) -> None:
        account.invest(amount, asset_name)
        # account is also a BankAccount with an owner attribute
        owner = getattr(account, "owner", "Customer")
        self.notifier.send(
            owner,
            f"Invested ${amount:.2f} in {asset_name}. Portfolio updated!",
        )


class AccountFormatter:
    """Formatter to present account data."""

    def to_json(self, account: BankAccount) -> dict:
        return {
            "owner": account.owner,
            "balance": account.balance,
            "account_type": type(account).__name__,
        }
