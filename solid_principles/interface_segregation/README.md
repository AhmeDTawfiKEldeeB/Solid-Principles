<h1 align="center">🧩 Interface Segregation Principle (ISP)</h1>

<h2 align="center">📖 Imagine That Our Banking System Is Growing Again</h2>

In the previous chapters, we continued building our banking system and added
different types of bank accounts.

Our system now supports different account types, and each type can have
different capabilities.

For example, accounts such as `SavingsAccount` and `CheckingAccount` support
withdrawing and depositing money, and calculating interest.

As the banking system grows, the bank decides to introduce a new feature: **investing in financial markets** (such as stocks, ETFs, and mutual funds).

To support this feature, the bank wants to introduce an `InvestmentAccount`.

A developer looks at the existing system and thinks:

> *"Let's simply add the new `invest()` method directly to the base `BankAccount` class. That way, all account types can inherit it!"*

At first, this seems like a convenient idea.

Our `BankAccount` now looks like this:

```text
BankAccount
│
├── deposit()
├── withdraw()
├── calculate_interest()
└── invest()
```

And every account type inherits from it:

```text
BankAccount
│
├── deposit()
├── withdraw()
├── calculate_interest()
└── invest()
       │
       ├── SavingsAccount
       ├── CheckingAccount
       └── InvestmentAccount
```

But think about this:

Does a **`SavingsAccount`** support buying stocks or investing in financial markets? **No.**

Does a **`CheckingAccount`** support trading assets? **No.**

Only an **`InvestmentAccount`** needs the `invest()` operation.

By putting `invest()` into the base `BankAccount` class, **every account type is now forced to depend on a method that it does not actually need or support.**

The problem is not that `invest()` exists.

The problem is that classes are forced to implement or depend on functionality that is completely irrelevant to them.

This is where the **Interface Segregation Principle** becomes useful.

The principle states:

> **Clients should not be forced to depend on methods they do not use.**

In simple terms, instead of creating one large interface that contains everything, we should break it into smaller and more specific interfaces.

Each class should only depend on the functionality that it actually needs.

So instead of having one large interface:

```text
BankAccount
│
├── deposit()
├── withdraw()
├── calculate_interest()
└── invest()
```

we separate the investment capability into its own interface:

```text
BankAccount (Base Class)
├── deposit()
├── withdraw()
└── calculate_interest()

Investable (Interface)
└── invest()
```

Now each account type only implements what makes sense for it:

```text
SavingsAccount
└── BankAccount

CheckingAccount
└── BankAccount

InvestmentAccount
├── BankAccount
└── Investable
```

This keeps our classes clean, focused, and free of useless baggage.

Let's see what happens when we put `invest()` into the base `BankAccount` first.

---

<h2 align="center">📍 Where We Left Off in Liskov Substitution (LSP)</h2>

At the end of the previous chapter (**Liskov Substitution Principle**), our banking system had:
- A `BankAccount` base class handling core operations (`deposit()`, `calculate_interest()`).
- Accounts handling standard operations (`SavingsAccount`, `CheckingAccount`).
- Everything was working smoothly.

Now, let's look at the mistake of adding `invest()` to that base class.

---

<h2 align="center">💥 The Mistake: The "Fat Interface" (Violating ISP)</h2>

Suppose a developer modifies the base `BankAccount` class by adding `invest()` as an abstract method:

```python
from abc import ABC, abstractmethod


class BankAccount(ABC):

    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float):
        self.balance += amount

    def withdraw(self, amount: float):
        self.balance -= amount

    @abstractmethod
    def calculate_interest(self) -> float:
        pass

    # ❌ New operation added to the base class:
    @abstractmethod
    def invest(self, amount: float, asset_name: str):
        """Invest money into a financial asset."""
        pass
```

Because `invest()` is an `@abstractmethod` in the base class, **every single subclass is forced to implement it**.

Look at what happens when we write `SavingsAccount`:

```python
class SavingsAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.05

    # ❌ SavingsAccount does NOT invest, but Python FORCES us to implement it!
    def invest(self, amount: float, asset_name: str):
        raise NotImplementedError("Savings accounts do not support investments!")
```

And `CheckingAccount` is forced to do the exact same thing:

```python
class CheckingAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.02

    # ❌ CheckingAccount does NOT invest either!
    def invest(self, amount: float, asset_name: str):
        raise NotImplementedError("Checking accounts do not support investments!")
```

Only `InvestmentAccount` actually uses the method:

```python
class InvestmentAccount(BankAccount):

    def __init__(self, owner: str, balance: float):
        super().__init__(owner, balance)
        self.portfolio = {}

    def calculate_interest(self):
        return self.balance * 0.08

    def invest(self, amount: float, asset_name: str):
        self.balance -= amount
        self.portfolio[asset_name] = self.portfolio.get(asset_name, 0.0) + amount
        print(f"Invested ${amount} in {asset_name}")
```

---

<h2 align="center">💥 The Crash: What Happens to the Clients?</h2>

Now imagine our bank has an investment service used by the investment department:

```python
class InvestmentService:

    @staticmethod
    def process_investment(account: BankAccount, amount: float, asset_name: str):
        print(f"Processing investment for {account.owner}...")
        account.invest(amount, asset_name)
```

Notice that `InvestmentService` takes a `BankAccount` parameter.

Because `SavingsAccount` inherits from `BankAccount`, someone passes a `SavingsAccount` into this function:

```python
alice_savings = SavingsAccount("Alice", 1000.0)
charlie_invest = InvestmentAccount("Charlie", 5000.0)

# Charlie's investment -> Works!
InvestmentService.process_investment(charlie_invest, 2000.0, "S&P 500 ETF")

# Alice's savings -> What happens?
InvestmentService.process_investment(alice_savings, 500.0, "Apple Stock")
```

Look at what happens in the terminal:

```text
Processing investment for Charlie...
Invested $2000.0 in S&P 500 ETF

Processing investment for Alice...
Traceback (most recent call last):
  ...
NotImplementedError: Savings accounts do not support investments!
```

💥 **The entire program crashes!**

---

<h2 align="center">⚠️ So, What's the Problem?</h2>

Let's break down why this design is flawed:

1. **Polluted Subclasses (Dummy Implementations)**:
   `SavingsAccount` and `CheckingAccount` are polluted with methods they cannot use. Developers are forced to write `raise NotImplementedError` or empty `pass` methods just to make the code compile.

2. **False Promises**:
   `BankAccount` promised: *"Every bank account has an `invest()` method that you can safely call."*
   Client code trusted that promise, called the method, and crashed at runtime.

3. **High Coupling & Unnecessary Changes**:
   Imagine tomorrow the bank changes the signature of `invest()` to require a transaction fee:
   ```python
   def invest(self, amount: float, asset_name: str, fee: float):
   ```
   Because `invest()` is inside `BankAccount`, you must now modify `SavingsAccount` and `CheckingAccount` too!
   **Why should a class change when a feature it never uses changes?**

```text
                   ┌──────────────────────────────────────────────┐
                   │                 BankAccount                  │
                   │      deposit()  withdraw()  invest()         │
                   └──────────────────────┬───────────────────────┘
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  ▼                       ▼                       ▼
            SavingsAccount         CheckingAccount        InvestmentAccount
        (Forced dummy invest)   (Forced dummy invest)     (Real invest: ✅)
```

This violates the **Interface Segregation Principle**:
> **Clients should not be forced to depend on methods they do not use.**

---

<h2 align="center">💡 The Solution: Segregate the Interface</h2>

The solution is straightforward:

> **Don't put `invest()` into `BankAccount`!**

Instead:
1. Keep `BankAccount` focused only on operations common to **all** accounts: `deposit()`, `withdraw()`, and `calculate_interest()`.
2. Create a separate, dedicated interface: **`Investable`** with the `invest()` method.

```text
      BankAccount (Base Class)
      ├── deposit()
      ├── withdraw()
      └── calculate_interest()
             ▲
             │
      ┌──────┴─────────────────────────┐
      │                                │
SavingsAccount                  InvestmentAccount
(BankAccount)             (BankAccount + Investable)
                                       ▲
                                       │ implements
                                  Investable (Interface)
                                  └── invest()
```

Look at how clean this becomes:
- `SavingsAccount` only inherits from `BankAccount`. It doesn't know or care about `invest()`.
- `CheckingAccount` only inherits from `BankAccount`.
- `InvestmentAccount` inherits from `BankAccount` **and** implements `Investable`.
- `InvestmentService` accepts **`Investable`**, NOT `BankAccount`.

Now:
- You **cannot** accidentally pass a `SavingsAccount` to `InvestmentService`.
- No account has dummy methods or `raise NotImplementedError`.
- Changes to `invest()` only affect `Investable` and `InvestmentAccount`.

---

<h2 align="center">🛠️ Step-by-Step Code Changes</h2>

### Step 1: Keep `BankAccount` Clean and Create `Investable` in `bank.py`

```python
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


class Investable(ABC):
    """Segregated interface specifically for investment operations."""

    @abstractmethod
    def invest(self, amount: float, asset_name: str) -> None:
        """Invest a specified amount into an asset."""
        pass
```

### Step 2: Update Client Services in `bank.py`

- `BankServices` (deposits and withdrawals) accepts any `BankAccount`.
- `InvestmentService` accepts **only** `Investable`:

```python
class BankServices:
    """General banking operations for all accounts."""

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
```

### Step 3: Implement Account Types in `account_types.py`

- `SavingsAccount` and `CheckingAccount` inherit only from `BankAccount`.
- `InvestmentAccount` inherits from `BankAccount` and implements `Investable`:

```python
from solid_principles.interface_segregation.bank import (
    BankAccount,
    Investable,
)


class SavingsAccount(BankAccount):

    def calculate_interest(self) -> float:
        return self.balance * 0.05


class CheckingAccount(BankAccount):

    def calculate_interest(self) -> float:
        return self.balance * 0.02


class InvestmentAccount(BankAccount, Investable):

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

---

<h2 align="center">📦 The Complete Refactored Code</h2>

### 1. `bank.py`

```python
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
```

### 2. `account_types.py`

```python
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
```

### 3. `main.py`

```python
from solid_principles.interface_segregation.bank import (
    BankServices,
    InvestmentService,
    Investable,
)
from solid_principles.interface_segregation.account_types import (
    SavingsAccount,
    CheckingAccount,
    InvestmentAccount,
)


def main():
    print("=== Setting Up Bank Accounts ===")
    alice = SavingsAccount("Alice", 1000.0)
    bob = CheckingAccount("Bob", 500.0)
    charlie = InvestmentAccount("Charlie", 5000.0)

    print(f"Alice's Savings balance:    ${alice.balance:.2f}")
    print(f"Bob's Checking balance:     ${bob.balance:.2f}")
    print(f"Charlie's Investment cash:  ${charlie.balance:.2f}")

    print("\n=== 1. Standard Banking Operations (Deposit & Withdraw) ===")
    BankServices.process_deposit(alice, 200.0)
    print(f"Deposited $200 to Alice. New balance: ${alice.balance:.2f}")

    BankServices.process_withdrawal(bob, 100.0)
    print(f"Withdrew $100 from Bob. New balance: ${bob.balance:.2f}")

    BankServices.process_deposit(charlie, 1000.0)
    print(f"Deposited $1000 to Charlie. New cash balance: ${charlie.balance:.2f}")

    print("\n=== 2. Investment Service (Only for Investable Accounts) ===")
    print("Charlie investing $2500 in 'S&P 500 ETF'...")
    InvestmentService.process_investment(charlie, 2500.0, "S&P 500 ETF")
    print(f"Charlie's remaining cash balance: ${charlie.balance:.2f}")
    print(f"Charlie's investment portfolio:    {charlie.portfolio}")

    print("\n=== 3. Interface Segregation Guarantees ===")
    print(f"- Is SavingsAccount Investable?    {isinstance(alice, Investable)} [False]")
    print(f"- Is CheckingAccount Investable?   {isinstance(bob, Investable)} [False]")
    print(f"- Is InvestmentAccount Investable? {isinstance(charlie, Investable)} [True]")

    print(
        "\n[SUCCESS] SavingsAccount and CheckingAccount are not forced to implement invest()!"
    )
    print(
        "[SUCCESS] InvestmentService depends strictly on Investable, keeping interfaces clean!"
    )


if __name__ == "__main__":
    main()
```

---

<h2 align="center">▶ Running the Code & Output</h2>

Run the script from the root directory:

```bash
python -m solid_principles.interface_segregation.main
```

Output:

```text
=== Setting Up Bank Accounts ===
Alice's Savings balance:    $1000.00
Bob's Checking balance:     $500.00
Charlie's Investment cash:  $5000.00

=== 1. Standard Banking Operations (Deposit & Withdraw) ===
Deposited $200 to Alice. New balance: $1200.00
Withdrew $100 from Bob. New balance: $400.00
Deposited $1000 to Charlie. New cash balance: $6000.00

=== 2. Investment Service (Only for Investable Accounts) ===
Charlie investing $2500 in 'S&P 500 ETF'...
Charlie's remaining cash balance: $3500.00
Charlie's investment portfolio:    {'S&P 500 ETF': 2500.0}

=== 3. Interface Segregation Guarantees ===
- Is SavingsAccount Investable?    False [False]
- Is CheckingAccount Investable?   False [False]
- Is InvestmentAccount Investable? True [True]

[SUCCESS] SavingsAccount and CheckingAccount are not forced to implement invest()!
[SUCCESS] InvestmentService depends strictly on Investable, keeping interfaces clean!
```

---

<h2 align="center">⚖️ Before vs After</h2>

| Aspect | 🔴 Before (Fat Interface) | 🟢 After (Interface Segregation) |
|:---|:---|:---|
| **Base Class Design** | `BankAccount` contains `deposit()`, `withdraw()`, and `invest()` | `BankAccount` contains only common operations; `Investable` is a separate interface |
| **Subclass Responsibility** | `SavingsAccount` and `CheckingAccount` forced to implement dummy `invest()` methods raising errors | Subclasses only implement operations they actually support |
| **Client Safety** | `InvestmentService` accepts `BankAccount`, risking runtime crashes if given a regular account | `InvestmentService` accepts `Investable`, preventing invalid accounts at type-check time |
| **Impact of Change** | Modifying `invest()` forces changes to all accounts in the system | Modifying `invest()` only affects `Investable` and `InvestmentAccount` |

---

<h2 align="center">🔗 Relationship Between LSP and ISP</h2>

Notice how **LSP** and **ISP** complement each other:

- **ISP** asks: *"Is the interface small and focused, or are we forcing classes to carry methods they don't need?"*
- **LSP** asks: *"Can every subclass safely replace its base class without breaking expectations?"*

When you violate **ISP** by putting `invest()` inside `BankAccount`, you force `SavingsAccount` to implement it with `raise NotImplementedError`.
The moment someone calls `invest()` on that `SavingsAccount`, **you violate LSP as well!**

> **Applying ISP prevents the dummy methods that lead to LSP violations.**

---

<h2 align="center">👍 3 Simple Rules to Spot an ISP Violation</h2>

1. **A subclass raises `NotImplementedError` or does nothing (`pass`)**:
   If a class implements a method just to say *"I can't do this"*, that method does not belong in the base interface.
2. **A client only uses a small fraction of the interface**:
   If a service receives a large class but only calls one specific method, that service should depend on a smaller, dedicated interface.
3. **Changes to a feature force unrelated classes to update**:
   If changing how investments work forces you to touch `SavingsAccount`, your interfaces are not properly segregated.

---

<h2 align="center">📝 Summary</h2>

The **Interface Segregation Principle (ISP)** ensures that:

> **Clients should not be forced to depend on methods they do not use.**

In our banking system:
- **Old Way**: Putting `invest()` into `BankAccount` forced every account to implement investment logic it didn't support.
- **New Way**: We created a separate `Investable` interface. Only `InvestmentAccount` implements it, and `InvestmentService` depends only on `Investable`.

> **Keep your interfaces small, focused, and honest.**
