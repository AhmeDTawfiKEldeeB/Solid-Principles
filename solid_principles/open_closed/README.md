<h1 align="center">🚪 Open/Closed Principle (OCP)</h1>

<h2 align="center">📖 Imagine That Our Banking System Is Growing</h2>

In the previous chapter, we started building a simple banking system.

We had a `BankAccount` class responsible for the basic operations of an
account, such as depositing and withdrawing money.

As we continued developing the system, we noticed that the account was
starting to have more than one responsibility.

For example, calculating interest was not really the responsibility of
`BankAccount`, so we moved that logic into a separate `InterestCalculator`.

We also had another requirement: converting the account data into JSON.

Instead of putting that functionality inside `BankAccount`, we created a
separate `AccountFormatter` class.

After applying the **Single Responsibility Principle**, our design looks
like this:

```text
BankAccount
│
├── deposit()
└── withdraw()

InterestCalculator
│
└── calculate_interest()

AccountFormatter
│
└── to_json()
```

So far, everything is working perfectly.

Our banking system is simple, and each class has a clear responsibility.

But now imagine that the bank is growing.

The bank wants to introduce different types of bank accounts.

For example, we may start with:

```text
BankAccount
│
├── SavingsAccount
└── CheckingAccount
```

And now a new requirement appears.

A `SavingsAccount` should have a different interest rate from a
`CheckingAccount`.

For example:

- **SavingsAccount**: 5% interest
- **CheckingAccount**: 2% interest

At first, this looks like a small change.

We already have an `InterestCalculator`, so we can simply modify it to check
which type of account we received and calculate the interest accordingly.

For example, we could write something like:

```text
if account is a SavingsAccount:
    calculate 5%

else if account is a CheckingAccount:
    calculate 2%
```

This approach works.

The program will run correctly, and the interest will be calculated.

But let's think about what will happen as the banking system continues to grow.

Tomorrow, the bank may introduce:

- `BusinessAccount`
- `StudentAccount`
- `PremiumAccount`
- `InvestmentAccount`
- ...

Now every time we introduce a new account type, we need to go back to the
existing `InterestCalculator` and modify it.

The class that was originally responsible for calculating interest is now
starting to know about every type of account in the system.

This is where we start to have a design problem.

The Open/Closed Principle tells us that a class or module should be:

> **Open for extension, but closed for modification.**

In simple terms, we should be able to add new behavior to our system without
having to continuously modify existing code that is already working.

Instead of changing `InterestCalculator` every time a new account type is
introduced, we want to design our system so that new account types can bring
their own interest calculation behavior.

So the goal is not to stop the system from changing.

The goal is to make it possible to extend the system without constantly
changing the existing implementation.

---

### 🗺️ The Journey from SRP to OCP

1. **Step 1 — Single Responsibility Principle (SRP)**:
   We separated distinct concerns into focused classes:
   - `BankAccount` handles core account operations.
   - `InterestCalculator` handles interest calculations.
   - `AccountFormatter` handles formatting account data.

2. **Step 2 — New Requirements Emerge**:
   The bank introduces specialized account types:
   - `SavingsAccount`
   - `CheckingAccount`
   - `BusinessAccount`

3. **Step 3 — The Design Problem (OCP Violation)**:
   `InterestCalculator` must be opened and modified for every new account type,
   accumulating endless conditional checks.

4. **Step 4 — Refactoring with OCP**:
   We refactor the architecture so new accounts extend the system without
   modifying any existing classes or modules.

Let's see what happens with our current design first.

We will start by adding different account types and modifying
`InterestCalculator` to handle them.

Then we will introduce another account type and see why this design becomes
a problem.

After that, we will refactor the design using the Open/Closed Principle.

---

<h2 align="center">💻 The First Implementation (Violating OCP)</h2>

We start with our `BankAccount` base class and two specialized account
types: `SavingsAccount` and `CheckingAccount`.

```python
class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount


class SavingsAccount(BankAccount):
    pass


class CheckingAccount(BankAccount):
    pass
```

Now, we create an `InterestCalculator` that checks the type of account
using conditional statements:

```python
class InterestCalculator:

    def calculate_interest(self, account):
        if isinstance(account, SavingsAccount):
            return account.balance * 0.05
        elif isinstance(account, CheckingAccount):
            return account.balance * 0.02
        else:
            raise ValueError(f"Unknown account type: {type(account).__name__}")
```

Let's run it:

```python
savings = SavingsAccount("Alice", 1000)
checking = CheckingAccount("Bob", 1000)

calculator = InterestCalculator()

print(f"Savings Account ({savings.owner}) Balance: ${savings.balance}")
print(f"Savings Interest: ${calculator.calculate_interest(savings)}")

print(f"Checking Account ({checking.owner}) Balance: ${checking.balance}")
print(f"Checking Interest: ${calculator.calculate_interest(checking)}")
```

The code works as expected and produces:

```text
Savings Account (Alice) Balance: $1000
Savings Interest: $50.0
Checking Account (Bob) Balance: $1000
Checking Interest: $20.0
```

Both accounts calculate interest properly: Alice earns 5% ($50.0) and Bob
earns 2% ($20.0).

---

<h2 align="center">📈 New Requirement: Adding BusinessAccount</h2>

As the bank expands, corporate clients join and the bank introduces a
`BusinessAccount` with a 3% interest rate.

To support this new account type, we define the class:

```python
class BusinessAccount(BankAccount):
    pass
```

Now, how do we calculate interest for a `BusinessAccount`?

Because `InterestCalculator` relies on type checking, we are **forced to open
and modify the existing `InterestCalculator` class**:

```python
class InterestCalculator:

    def calculate_interest(self, account):
        if isinstance(account, SavingsAccount):
            return account.balance * 0.05
        elif isinstance(account, CheckingAccount):
            return account.balance * 0.02
        elif isinstance(account, BusinessAccount):  # MODIFIED EXISTING CODE
            return account.balance * 0.03
        else:
            raise ValueError(f"Unknown account type: {type(account).__name__}")
```

Let's test it:

```python
business = BusinessAccount("Charlie", 10000)
print(f"Business Interest: ${calculator.calculate_interest(business)}")
```

Output:

```text
Business Interest: $300.0
```

The calculation works. But notice what just happened: **to add a new feature,
we had to modify existing, working code.**

---

<h2 align="center">⚠️ So, What's the Problem?</h2>

The problem is **not** that the code produces incorrect calculations.

The calculations are mathematically accurate.

The problem is **how our system handles change**.

When we first built `InterestCalculator`, it was tested and working. But as
soon as a new account type appeared, we were forced to go back and modify
its internal logic:

```text
InterestCalculator (Tightly Coupled)
├── SavingsAccount  (5% logic)
├── CheckingAccount (2% logic)
└── BusinessAccount (3% logic)
```

`InterestCalculator` is tightly coupled to every single account type. It
must know what types exist and how to calculate interest for each one.

<h3 align="">🚨 The OCP Violation</h3>

Here is what happens every time requirements evolve:

1. A new account type is introduced.
2. We must open `InterestCalculator` (existing tested code).
3. We add a new `elif isinstance(...)` condition.
4. We must recompile and retest all existing accounts.
5. We introduce the risk of breaking existing behavior.

This violates both sides of the principle:

- **Not Closed for Modification**:
  Every time the bank creates an account type, `InterestCalculator` must be
  modified. A class should be closed to modifications once implemented and
  tested.

- **Not Open for Extension**:
  We cannot introduce a new account type by simply writing a new class. We
  always have to edit existing code.

<h3 align="c"> Why Is This Dangerous in Practice?</h3>

As the bank continues to grow, more account types will be added:

- `StudentAccount` (1% interest)
- `MoneyMarketAccount` (4.5% interest)
- `FixedDepositAccount` (7% interest)
- `RetirementAccount` (6% interest)

If we keep using this approach:

- **Endless Conditionals**: `InterestCalculator` turns into a massive chain of
  `if/elif/elif/...` spanning dozens or hundreds of lines.
- **Regression Bugs**: Modifying `InterestCalculator` risks accidentally
  breaking the calculations for existing account types that were already
  working fine.
- **Merge Conflicts**: Multiple developers adding different account types will
  all edit the same file and method at the same time.
- **Tight Coupling**: `InterestCalculator` must import and know the exact details
  of every account class in the system.

---

<h2 align="center">💡 The Better Approach</h2>

Instead of having `InterestCalculator` inspect account types with conditionals,
we can use **Polymorphism** and an **Abstract Contract**.

The Open/Closed Principle suggests that:

> **New behavior should be added by writing new code, not by modifying existing code.**

We invert the design:

1. `BankAccount` defines an abstract method `calculate_interest()`.
2. Each account type implements its own interest calculation rules.
3. `InterestCalculator` simply calls `account.calculate_interest()` without
   caring which concrete type it is dealing with.
4. We separate the base system from concrete types:
   - `bank.py`: Contains the core `BankAccount` contract, `InterestCalculator`,
     and `AccountFormatter`.
   - `accounts_type.py`: Contains concrete account implementations.

```text
InterestCalculator
└── Calls calculate_interest() on BankAccount contract
    ├── SavingsAccount   (calculates 5%)
    ├── CheckingAccount  (calculates 2%)
    └── BusinessAccount  (calculates 3%)
```

Now look at what happens when a new requirement arrives (e.g., `StudentAccount`):

```text
BankAccount Contract
└── StudentAccount (New extension: calculates 1%)
```

Does `InterestCalculator` change? **No! Not a single line.**
Does `bank.py` change? **No! It remains completely untouched.**

The system has been **extended** without **modifying** existing code.

---

<h2 align="">🛠️ Refactoring the Design</h2>

Let's refactor our design step by step using OCP and clean file separation.

<h3 align=""> Step 1 — Define the Abstract Contract in <code>bank.py</code></h3>

We use Python's `abc` module to define `BankAccount` as an abstract base
class. Any account type must implement `calculate_interest()`:

```python
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
        """Each account type defines its own interest calculation."""
        pass
```

<h3 align=""> Step 2 — Make InterestCalculator Closed for Modification in <code>bank.py</code></h3>

Look at `InterestCalculator`:

```python
class InterestCalculator:

    def calculate_interest(self, account: BankAccount):
        return account.calculate_interest()
```

Notice how clean and minimal `InterestCalculator` is:

- No `isinstance()` checks.
- No `if/elif/else` ladders.
- No imports of concrete account classes.
- It depends entirely on the abstract `BankAccount` contract.
- It is now **closed for modification**.

<h3 align=""> Step 3 — Separate Account Implementations into <code>accounts_type.py</code></h3>

Instead of crowding all accounts into `bank.py`, we place concrete account
types in `accounts_type.py`:

```python
from bank import BankAccount


class SavingsAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.05


class CheckingAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.02


class BusinessAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.03
```

<h3 align=""> Step 4 — Proving OCP: Adding a New Account Type</h3>

Now the bank introduces a fourth account type: `StudentAccount` (1% interest).

To add this feature, all we do is create a **new class** in `accounts_type.py`:

```python
class StudentAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.01
```

Look at what we did NOT have to touch:

- `BankAccount` did not change.
- `SavingsAccount` did not change.
- `CheckingAccount` did not change.
- `BusinessAccount` did not change.
- `bank.py` did not change.
- **`InterestCalculator` did not change!**

The new account works immediately with the existing `InterestCalculator`.
This is the Open/Closed Principle in action!

---

<h2 align="center">📦 The Complete Refactored Code</h2>

### 1. `bank.py` (Core Abstractions & Calculator)

```python
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
```

### 2. `accounts_type.py` (Concrete Account Extensions)

```python
from solid_principles.open_closed.bank import BankAccount


class SavingsAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.05


class CheckingAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.02


class BusinessAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.03


class StudentAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.01
```

---

<h3 align="center">🚀 Running the Main Function (`main.py`)</h3>

In `main.py`, we import our services from `bank` and our account types from
`accounts_type`:

```python
from bank import InterestCalculator, AccountFormatter

from solid_principles.open_closed.accounts_type import (SavingsAccount,CheckingAccount,BusinessAccount,StudentAccount)


def main():
    calculator = InterestCalculator()
    formatter = AccountFormatter()

    accounts = [
        SavingsAccount("Alice", 1000),
        CheckingAccount("Bob", 1000),
        BusinessAccount("Charlie", 10000),
        StudentAccount("David", 500),
    ]

    for account in accounts:
        interest = calculator.calculate_interest(account)
        account_type = type(account).__name__
        print(f"{account.owner} ({account_type}):")
        print(f"  Balance: ${account.balance}")
        print(f"  Interest: ${interest}")
        print(f"  JSON: {formatter.to_json(account)}\n")


if __name__ == "__main__":
    main()
```

<h3 align="">▶ Output</h3>

Running `python main.py` produces:

```text
Alice (SavingsAccount):
  Balance: $1000
  Interest: $50.0
  JSON: {'owner': 'Alice', 'balance': 1000, 'account_type': 'SavingsAccount'}

Bob (CheckingAccount):
  Balance: $1000
  Interest: $20.0
  JSON: {'owner': 'Bob', 'balance': 1000, 'account_type': 'CheckingAccount'}

Charlie (BusinessAccount):
  Balance: $10000
  Interest: $300.0
  JSON: {'owner': 'Charlie', 'balance': 10000, 'account_type': 'BusinessAccount'}

David (StudentAccount):
  Balance: $500
  Interest: $5.0
  JSON: {'owner': 'David', 'balance': 500, 'account_type': 'StudentAccount'}
```

---

<h2 align="center">⚖️ Before vs After</h2>

### 🔴 Before (Violating OCP)

- **Modification Required**: Adding an account type requires modifying `InterestCalculator`.
- **Type Checking**: Uses `isinstance()` checks and conditional ladders.
- **Risk**: Touching existing code risks breaking accounts that already work.
- **Coupling**: High coupling between calculator and concrete account types.

### 🟢 After (Applying OCP)

- **Pure Extension**: Adding an account type only requires adding a new class in `accounts_type.py`.
- **Polymorphic Contract**: The calculator relies on `calculate_interest()` on the abstract `BankAccount`.
- **Safety**: `bank.py` and `InterestCalculator` stay closed and 100% stable.
- **Coupling**: Loose coupling through abstraction.

---

<h2 align="">🌟 Why Is This Better?</h2>

1. **Stability**:
   Code that already works and is running in production stays unchanged. You
   eliminate the risk of breaking existing features when adding new ones.

2. **Maintainability & Separation of Concerns**:
   `bank.py` contains core business abstractions, while `accounts_type.py`
   contains individual account rules. Each file has a clear responsibility.

3. **Team Scalability**:
   Multiple developers can create different account types in parallel without
   ever modifying the same file or causing git merge conflicts.

4. **Testability**:
   You only need to write unit tests for the new account class. You don't need
   to re-verify all other account calculations in `InterestCalculator`.

---

<h2 align="">👍 Thumb Rules</h2>

Practical rules to identify OCP opportunities:

- **Look for type checking**: If you see `isinstance()`, `type()`, or
  `account_type == "..."` in an `if/elif/else` chain, OCP is likely violated.
- **Ask yourself before editing**: "To add this new feature, am I writing
  *new* code or am I modifying *existing* code?"
- **Use Polymorphism**: Let subclasses implement specific behavior rather than
  a central class inspecting types.
- **Rely on Abstractions**: High-level modules should interact with interfaces
  or abstract classes, not concrete implementations.

---

<h2 align="center">📝 Summary</h2>

The **Open/Closed Principle (OCP)** is all about building software that can
grow gracefully.

- **Open for extension**: The system can easily adopt new features and behaviors.
- **Closed for modification**: Existing, tested code does not need to change to
  accommodate new features.

In our banking system:
- **Old Way**: `InterestCalculator` was modified for every new account type.
- **New Way**: `InterestCalculator` and `bank.py` stay closed; new account types extend `BankAccount` in `accounts_type.py`.

> **A class or module should be open for extension, but closed for modification.**
