<h1 align="center">🔌 Dependency Inversion Principle (DIP)</h1>

<h2 align="center">📖 Imagine That Our Banking System Is Growing Again</h2>

In the previous chapters, we continued improving our banking system.

We started with a simple `BankAccount`, then separated its responsibilities (**SRP**),
made it open for extension (**OCP**), ensured honest substitutability (**LSP**),
and segregated the investment capability into a dedicated `Investable` interface (**ISP**).

Now the bank is getting even bigger.

New services and external integrations are being introduced to support our accounts.

For example, whenever a customer performs an operation on their account—whether it is a deposit, a withdrawal, or an investment—the bank needs to notify the account owner.

At first, the requirement is simple: send an alert to the customer.

A developer creates a `BankTransactionService` and directly couples it to a specific notification tool, such as `SMSNotifier`.

Our design may look like this:

```text
BankTransactionService (High-level)
          │
          ↓ (directly depends on)
     SMSNotifier (Low-level)
```

At first, this works.

The service knows which tool it needs, so whenever we want to process a transaction, it uses that tool.

```python
class BankTransactionService:

    def __init__(self):
        # ❌ Hardcoded dependency on a concrete low-level class!
        self.notifier = SMSNotifier()

    def process_deposit(self, account, amount):
        account.deposit(amount)
        self.notifier.send(account.owner, f"Deposited ${amount}")
```

But now imagine that the bank decides to replace or expand the notification tool.

For example, instead of sending expensive SMS messages, the bank wants to send **Emails**, or mobile **Push Notifications**.

Now we have a problem.

If `BankTransactionService` directly creates and depends on `SMSNotifier`, changing that tool means **we have to modify `BankTransactionService`**.

```text
BankTransactionService
          │
          ↓
     SMSNotifier

Later, the bank wants:

BankTransactionService
          │
          ↓
    EmailNotifier

Later still, the bank wants:

BankTransactionService
          │
          ↓
PushNotificationService
```

The high-level banking service itself should **not** need to change just because the notification delivery channel changed!

The problem is that `BankTransactionService` is **tightly coupled to a concrete implementation**.

This makes the system rigid, difficult to change, and nearly impossible to unit test without sending real messages to real customers.

This is where the **Dependency Inversion Principle (DIP)** becomes essential.

The principle states:

> **1. High-level modules should not depend on low-level modules. Both should depend on abstractions.**
>
> **2. Abstractions should not depend on details. Details should depend on abstractions.**

In simple terms, instead of making our high-level service depend directly on a specific concrete tool, we should make it depend on an **abstraction** (interface).

So instead of:

```text
BankTransactionService (High-level)
          │
          ↓
     SMSNotifier (Low-level)
```

we invert the dependency:

```text
                   Notifier (Abstraction)
                             ▲
              ┌──────────────┴──────────────┐
              │                             │
         SMSNotifier                  EmailNotifier
      (Low-level detail)            (Low-level detail)
              ▲
              │ depends on
    BankTransactionService (High-level)
```

Notice why it is called **Dependency Inversion**:

1. **Before**: The high-level module pointed **downward** directly at the low-level detail.
2. **After**: The dependency is **inverted**! Both the high-level service AND the low-level tools point toward the central abstraction (`Notifier`).

Now `BankTransactionService` does not care which concrete tool is being used. It only knows that whatever tool it receives follows the `Notifier` abstraction.

The dependency is provided from the outside (for example, passed through the constructor) instead of being created directly inside the service.

This technique is known as **Dependency Injection (DI)**.

Let's examine how this connects to the code we built in the previous chapter.

---

<h2 align="center">📍 Where We Left Off in Interface Segregation (ISP)</h2>

In the previous chapter (**Interface Segregation Principle**), we cleanly separated our banking capabilities:
- **`BankAccount`**: Base class handling common operations (`deposit`, `withdraw`, `calculate_interest`).
- **`Investable`**: Segregated interface for accounts supporting financial market investments (`invest`).
- **`SavingsAccount` & `CheckingAccount`**: Standard accounts inheriting from `BankAccount`.
- **`InvestmentAccount`**: Inheriting from `BankAccount` and implementing `Investable`.

Now, we need a high-level service to orchestrate customer transactions and alert customers.

Let's see what happens when we write that service **without** Dependency Inversion first.

---

<h2 align="center">💥 The Mistake: Direct Coupling (Violating DIP)</h2>

Suppose we create our concrete notification tool first:

```python
class SMSNotifier:
    """Low-level detail: Talks to an external SMS gateway."""

    def send(self, recipient: str, message: str):
        print(f"[SMS Gateway to {recipient}]: {message}")
```

Now, a developer creates the high-level banking service:

```python
class BankTransactionService:
    """High-level business logic module."""

    def __init__(self):
        # ❌ VIOLATION: Directly instantiating the concrete low-level class!
        self.notifier = SMSNotifier()

    def process_deposit(self, account: BankAccount, amount: float):
        account.deposit(amount)
        self.notifier.send(account.owner, f"Deposited ${amount:.2f}")

    def process_withdrawal(self, account: BankAccount, amount: float):
        account.withdraw(amount)
        self.notifier.send(account.owner, f"Withdrew ${amount:.2f}")

    def process_investment(self, account: Investable, amount: float, asset_name: str):
        account.invest(amount, asset_name)
        self.notifier.send(account.owner, f"Invested ${amount:.2f} in {asset_name}")
```

### Why is this code dangerous?

1. **Tight Coupling**:
   `BankTransactionService` cannot exist without `SMSNotifier`. They are glued together.
2. **Violates the Open/Closed Principle (OCP)**:
   When the bank introduces `EmailNotifier` or `PushNotificationService`, we are forced to **open and edit `BankTransactionService`**, modify its `__init__`, and risk breaking existing business logic.
3. **Impossible to Unit Test**:
   How do you test `process_deposit` in an automated test suite? Every test run would send real SMS messages via the network! You cannot easily mock or substitute the notifier because it is hardcoded inside `__init__`.

---

<h2 align="center">💡 The Solution: Inverting the Dependency (Applying DIP)</h2>

We solve this problem in two clean steps:

### Step 1: Create an Abstraction (`Notifier`)
We define a contract using Python's `ABC`:

```python
from abc import ABC, abstractmethod


class Notifier(ABC):
    """Abstraction that defines the notification contract."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass
```

Both low-level modules and high-level services will now agree on this contract.

### Step 2: Implement Low-Level Tools that Depend on the Abstraction

```python
class SMSNotifier(Notifier):
    def send(self, recipient: str, message: str) -> None:
        print(f"[SMS to {recipient}]: {message}")


class EmailNotifier(Notifier):
    def send(self, recipient: str, message: str) -> None:
        print(f"[Email to {recipient}@bank.com]: {message}")


class PushNotificationService(Notifier):
    def send(self, recipient: str, message: str) -> None:
        print(f"[Push Alert to {recipient}'s App]: {message}")
```

### Step 3: Inject the Abstraction into the High-Level Service (Dependency Injection)

Instead of creating the tool inside the service, **the service accepts any `Notifier` from the outside**:

```python
class BankTransactionService:
    """High-level module: depends ONLY on the Notifier abstraction."""

    def __init__(self, notifier: Notifier):
        # ✅ Injected dependency! No hardcoded classes.
        self.notifier = notifier

    def set_notifier(self, notifier: Notifier) -> None:
        """Allows swapping the delivery tool dynamically at runtime."""
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
        owner = getattr(account, "owner", "Customer")
        self.notifier.send(
            owner,
            f"Invested ${amount:.2f} in {asset_name}. Portfolio updated!",
        )
```

Look at what we achieved:
- `BankTransactionService` **never creates** any concrete notifier.
- It works with `SMSNotifier`, `EmailNotifier`, `PushNotificationService`, or any future tool (e.g. `WhatsAppNotifier`, `SlackNotifier`).
- We can swap notifiers at runtime with zero changes to business logic.
- We can pass a `MockNotifier` during testing to verify messages instantly without external network calls.

---

<h2 align="center">🛠️ Step-by-Step Code Changes</h2>

Let's see how our codebase is organized:

1. **`bank.py`**:
   - `BankAccount` & `Investable` (core domain contracts from ISP).
   - `Notifier(ABC)` (the DIP abstraction).
   - `SMSNotifier`, `EmailNotifier`, `PushNotificationService` (concrete low-level details).
   - `BankTransactionService` (high-level module with Dependency Injection).
2. **`account_types.py`**:
   - `SavingsAccount`, `CheckingAccount`, `InvestmentAccount` (domain models).
3. **`main.py`**:
   - Assembles the components, injects different notifiers, and demonstrates testability.

---

<h2 align="center">📦 The Complete Refactored Code</h2>

### 1. `bank.py`

```python
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
```

### 2. `account_types.py`

```python
from solid_principles.dependency_inversion.bank import (
    BankAccount,
    Investable,
)


class SavingsAccount(BankAccount):
    """A savings account earning 5% interest."""

    def calculate_interest(self) -> float:
        return self.balance * 0.05


class CheckingAccount(BankAccount):
    """A checking account earning 2% interest."""

    def calculate_interest(self) -> float:
        return self.balance * 0.02


class InvestmentAccount(BankAccount, Investable):
    """An investment account supporting investments and earning 8% return."""

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
```

### 3. `main.py`

```python
from solid_principles.dependency_inversion.bank import (
    BankTransactionService,
    SMSNotifier,
    EmailNotifier,
    PushNotificationService,
    Notifier,
)
from solid_principles.dependency_inversion.account_types import (
    SavingsAccount,
    CheckingAccount,
    InvestmentAccount,
)


class MockAuditLogger(Notifier):
    """A test double (mock) to verify transactions in automated tests."""

    def __init__(self):
        self.sent_messages = []

    def send(self, recipient: str, message: str) -> None:
        self.sent_messages.append((recipient, message))


def main():
    print("=== Setting Up Bank Accounts ===")
    alice = SavingsAccount("Alice", 1000.0)
    bob = CheckingAccount("Bob", 500.0)
    charlie = InvestmentAccount("Charlie", 5000.0)

    print(f"Alice's Savings balance:    ${alice.balance:.2f}")
    print(f"Bob's Checking balance:     ${bob.balance:.2f}")
    print(f"Charlie's Investment cash:  ${charlie.balance:.2f}")

    print("\n=== 1. Using SMS Notifier (Injected via Constructor) ===")
    sms_tool = SMSNotifier()
    bank_service = BankTransactionService(notifier=sms_tool)

    # Deposit with SMS alert
    bank_service.process_deposit(alice, 250.0)

    # Withdrawal with SMS alert
    bank_service.process_withdrawal(bob, 100.0)

    # Investment with SMS alert
    bank_service.process_investment(charlie, 1500.0, "Tech ETF")

    print(
        "\n=== 2. Swapping to Email Notifier (Zero Changes to BankTransactionService!) ==="
    )
    email_tool = EmailNotifier()
    bank_service.set_notifier(email_tool)

    bank_service.process_deposit(bob, 300.0)
    bank_service.process_investment(charlie, 1000.0, "Gold Fund")

    print("\n=== 3. Swapping to Push Notifications ===")
    push_tool = PushNotificationService()
    bank_service.set_notifier(push_tool)

    bank_service.process_withdrawal(alice, 50.0)

    print("\n=== 4. Testability via Mock Notifier ===")
    mock_tool = MockAuditLogger()
    test_service = BankTransactionService(notifier=mock_tool)

    test_service.process_deposit(alice, 100.0)
    print(f"Captured {len(mock_tool.sent_messages)} message in test log:")
    for recipient, msg in mock_tool.sent_messages:
        print(f"  -> Recorded for '{recipient}': {msg}")

    print(
        "\n[SUCCESS] High-level service depends on Notifier abstraction, not concrete tools!"
    )
    print(
        "[SUCCESS] We can plug in any notification tool without changing business logic!"
    )


if __name__ == "__main__":
    main()
```

---

<h2 align="center">▶ Running the Code & Output</h2>

Run the script from the root directory:

```bash
python -m solid_principles.dependency_inversion.main
```

Output:

```text
=== Setting Up Bank Accounts ===
Alice's Savings balance:    $1000.00
Bob's Checking balance:     $500.00
Charlie's Investment cash:  $5000.00

=== 1. Using SMS Notifier (Injected via Constructor) ===
[SMS to Alice]: Deposited $250.00. New Balance: $1250.00
[SMS to Bob]: Withdrew $100.00. Remaining Balance: $400.00
[SMS to Charlie]: Invested $1500.00 in Tech ETF. Portfolio updated!

=== 2. Swapping to Email Notifier (Zero Changes to BankTransactionService!) ===
[Email to Bob@bank.com]: Deposited $300.00. New Balance: $700.00
[Email to Charlie@bank.com]: Invested $1000.00 in Gold Fund. Portfolio updated!

=== 3. Swapping to Push Notifications ===
[Push Alert to Alice's App]: Withdrew $50.00. Remaining Balance: $1200.00

=== 4. Testability via Mock Notifier ===
Captured 1 message in test log:
  -> Recorded for 'Alice': Deposited $100.00. New Balance: $1300.00

[SUCCESS] High-level service depends on Notifier abstraction, not concrete tools!
[SUCCESS] We can plug in any notification tool without changing business logic!
```

---

<h2 align="center">⚖️ Before vs After</h2>

| Aspect | 🔴 Before (Violating DIP) | 🟢 After (Applying DIP) |
|:---|:---|:---|
| **Dependency Direction** | `BankTransactionService` depends directly on `SMSNotifier` (High-level depends on Low-level) | Both depend on the `Notifier` abstraction (Inverted dependencies) |
| **Instantiation** | Service creates its own dependencies internally (`self.notifier = SMSNotifier()`) | Dependencies are supplied from the outside via Dependency Injection (`__init__(notifier)`) |
| **Adding New Tools** | Adding Email or Push requires editing the service class (violating OCP) | New notifiers implement `Notifier` and can be plugged in without modifying the service |
| **Testability** | Hard to test without sending real SMS messages | Trivial to test by injecting a `MockNotifier` |
| **Coupling** | Tight coupling to third-party SDKs and delivery details | Loose coupling to stable abstractions |

---

<h2 align="center">🔍 DIP vs Dependency Injection (DI)</h2>

Developers often mix up **DIP** and **DI**:

- **Dependency Inversion Principle (DIP)** is the **architectural design principle**:
  *"High-level business logic should depend on abstractions, not concrete details."*
- **Dependency Injection (DI)** is the **implementation pattern/technique**:
  Instead of a class creating what it needs (`self.tool = Tool()`), dependencies are *"injected"* into the class from the outside (via constructor parameters, setter methods, or a DI container).

> **Dependency Injection is the tool we use to achieve the Dependency Inversion Principle.**

---

<h2 align="center">👍 3 Simple Rules to Spot a DIP Violation</h2>

1. **You see `new` or `ClassName()` inside high-level business classes**:
   If a high-level service directly instantiates a database connector, API client, or notification tool inside its methods or `__init__`, it is tightly coupled to that concrete class.
2. **Writing unit tests requires mocking network calls or monkey-patching**:
   If you cannot test your business logic in isolation without touching real databases or external services, your code is violating DIP.
3. **Changing a low-level library forces you to rewrite high-level rules**:
   If switching from SMS to Email or from SQLite to PostgreSQL causes you to modify your transaction logic, high-level code is depending on low-level details.

---

<h2 align="center">🎓 The Complete SOLID Journey: Summary</h2>

Across this repository, we evolved our banking system through all five SOLID principles:

| Principle | Core Question | What We Did in Our Bank |
|:---|:---|:---|
| **S — Single Responsibility** | *Does this class have only one reason to change?* | Separated `BankAccount`, `InterestCalculator`, and `AccountFormatter`. |
| **O — Open/Closed** | *Can we add new behavior without editing existing code?* | Made interest calculation polymorphic so new account types don't modify the calculator. |
| **L — Liskov Substitution** | *Can subclasses safely replace their base class?* | Ensured accounts that cannot withdraw (`FixedDepositAccount`) don't inherit and crash `withdraw()`. |
| **I — Interface Segregation** | *Are clients forced to implement methods they don't use?* | Separated `invest()` into `Investable` so standard savings accounts aren't burdened with dummy investment methods. |
| **D — Dependency Inversion** | *Do high-level and low-level modules depend on abstractions?* | Injected the `Notifier` abstraction into `BankTransactionService` so notification channels can be swapped without touching business logic. |

> **Software design is not about making code more complex; it is about keeping code adaptable and safe when requirements inevitably change.**
