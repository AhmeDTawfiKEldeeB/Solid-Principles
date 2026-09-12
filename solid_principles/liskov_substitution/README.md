<h1 align="center">🔄 Liskov Substitution Principle (LSP)</h1>

<h2 align="center">📖 Imagine That Our Banking System Is Growing Again</h2>

In the previous chapter, we continued building our banking system.

We already had a `BankAccount` class that handled the common behavior of a
bank account.

Then, the bank introduced different types of accounts.

We created classes such as:

```text
BankAccount
│
├── SavingsAccount
├── CheckingAccount
├── BusinessAccount
└── StudentAccount
```

Each account type can be used wherever a BankAccount is expected.

This is useful because our code does not need to know the exact type of the
account before working with it.

For example, if a function expects a BankAccount, we should be able to give
it a SavingsAccount or a CheckingAccount, and the program should continue
working correctly.

But now imagine that the bank introduces a new requirement.

Some operations that are common for certain types of bank accounts are not
necessarily supported by every account.

For example, the bank may introduce a new operation that every
BankAccount is expected to support.

At first, adding this operation to the base class seems completely fine.

The problem starts when we create a subclass that cannot actually behave
like a normal BankAccount.

Imagine that we create a new type of account that does not support this
operation.

What should the subclass do?

If we simply raise an exception or return an unexpected value, we have a
problem.

The code that works with BankAccount expects the normal behavior of the
base class.

But our subclass is no longer following that behavior.

This means that although the subclass is technically a BankAccount, it
cannot safely replace a BankAccount in every situation.

And this is exactly the problem that the Liskov Substitution Principle
helps us understand.

The principle states:

> **Any instance of a subclass should be substitutable for an instance of
> its base class.**

In simple terms:

If SavingsAccount is a subclass of BankAccount, then code that works
with a BankAccount should also be able to work with a SavingsAccount
without unexpected errors or different behavior that breaks the original
expectations.

```text
BankAccount
     │
     ├── SavingsAccount
     ├── CheckingAccount
     └── BusinessAccount

If code expects BankAccount
            ↓
A subclass should work
            ↓
Without breaking the expected behavior
```

So in this chapter, we are going to take our existing banking system and
introduce a new requirement.

We will first add the new behavior to BankAccount.

Then we will create different account types and see what happens when one
of the subclasses cannot properly support that behavior.

After seeing the problem, we will refactor the design so that every subclass
can safely be used wherever a BankAccount is expected.

Let's start with our current banking system.

---

<h2 align="center">📍 Where We Left Off in Open/Closed (OCP)</h2>

At the end of the previous chapter (**Open/Closed Principle**), our banking system had two main files:

### 1. `bank.py` (Baseline from OCP)
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
        """Calculate interest specific to this account type."""
        pass


class InterestCalculator:

    def calculate_interest(self, account: BankAccount):
        return account.calculate_interest()


class AccountFormatter:

    def to_json(self, account: BankAccount):
        return {
            "owner": account.owner,
            "balance": account.balance,
            "account_type": type(account).__name__,
        }
```

### 2. `account_types.py` (Baseline from OCP)
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

Notice what we had in OCP:
- `BankAccount` defined `deposit()` and `withdraw()`.
- Every account type (`Savings`, `Checking`, `Business`, `Student`) inherited both methods.
- Everything worked smoothly because **all four accounts supported withdrawing money**.

---

<h2 align="center">📈 New Requirement: Adding FixedDepositAccount</h2>

As the bank grows, it introduces a new investment product: **`FixedDepositAccount`** .

- It offers a high interest rate (**7%**).
- **The condition**: The money is locked for one year, so the customer **cannot withdraw money before maturity**.

Because a fixed deposit is logically a bank account, a developer naturally makes it inherit from `BankAccount`:

```python
class FixedDepositAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.07

    def withdraw(self, amount):
        # The money is locked, so we cannot withdraw!
        raise Exception("Withdrawals are not allowed on a Fixed Deposit Account!")
```

At first glance, this seems completely reasonable: if someone tries to withdraw from a fixed deposit, the account rejects the withdrawal.

Now, let's see what happens when client code uses this new account.

---

<h2 align="center">💥 The Crash: Breaking the Contract</h2>

Imagine our banking application has a function to process customer withdrawals:

```python
def make_withdrawal(account: BankAccount, amount: float):
    print(f"Withdrawing ${amount} from {account.owner}'s account...")
    account.withdraw(amount)
    print(f"Success! Remaining balance: ${account.balance}\n")
```

The function expects a `BankAccount` parameter.

Now, let's run it on our accounts:

```python
savings = SavingsAccount("Alice", 1000)
checking = CheckingAccount("Bob", 1000)
fixed = FixedDepositAccount("Charlie", 5000)

make_withdrawal(savings, 200)   # Alice withdraws $200 -> Works!
make_withdrawal(checking, 200)  # Bob withdraws $200   -> Works!
make_withdrawal(fixed, 200)     # Charlie withdraws $200 -> ???
```

Look at what happens in the terminal:

```text
Withdrawing $200 from Alice's account...
Success! Remaining balance: $800

Withdrawing $200 from Bob's account...
Success! Remaining balance: $800

Withdrawing $200 from Charlie's account...
Traceback (most recent call last):
  ...
Exception: Withdrawals are not allowed on a Fixed Deposit Account!
```

💥 **The entire program crashes!**

---

<h2 align="center">⚠️ So, What's the Problem?</h2>

Let's analyze why this crash happened:

1. The function `make_withdrawal` trusted the base class contract: `account: BankAccount`.
2. The `BankAccount` class promised: *"Any bank account has a `withdraw()` method that you can safely call."*
3. When we passed `SavingsAccount` or `CheckingAccount`, they honored that promise.
4. **When we passed `FixedDepositAccount`, it broke that promise and threw an exception.**

Even though `FixedDepositAccount` is technically a subclass of `BankAccount`, **it cannot safely replace a BankAccount**.

```text
Function expects: BankAccount
                        │
          Can the subclass replace it?
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
    SavingsAccount           FixedDepositAccount
     (Works: ✅)                 (Crashes: ❌)
```

And this is the core rule of the **Liskov Substitution Principle (LSP)**:

> **Subclasses must be substitutable for their base class without breaking the program or throwing unexpected errors.**

### 🚨 Common Bad Workarounds

When developers encounter this problem, they often try two bad "fixes":

1. **Silently Doing Nothing (`pass`)**:
   ```python
   class FixedDepositAccount(BankAccount):
       def withdraw(self, amount):
           pass  # Do nothing so it doesn't crash!
   ```
   *Why this is bad*: The caller thinks the money was withdrawn, but the balance never changed! This leads to silent accounting bugs and financial corruption.

2. **Checking the Type with `if isinstance(...)`**:
   ```python
   def make_withdrawal(account: BankAccount, amount: float):
       if isinstance(account, FixedDepositAccount):
           print("Cannot withdraw from this account!")
           return
       account.withdraw(amount)
   ```
   *Why this is bad*: Whenever you have to write `if isinstance(...)` to prevent calling a method on a subclass, **your inheritance design is broken**. Tomorrow, if the bank adds another non-withdrawable account, you will have to modify every withdrawal function in your codebase, violating OCP!

---

<h2 align="center">💡 The Solution: How We Refactor Step by Step</h2>

Let's ask the fundamental question:

> **Why did we put `withdraw()` inside `BankAccount` in the first place?**

We put it there because we assumed **every** bank account can withdraw money.
That assumption was wrong!

In our bank:
- Can **every** account accept deposits? **Yes.**
- Does **every** account have an owner and balance? **Yes.**
- Does **every** account calculate interest? **Yes.**
- Can **every** account withdraw money? **No!**

Therefore: **`withdraw()` does not belong in the base `BankAccount` class!**

### The Refactored Hierarchy

We separate account capabilities into two honest levels:

1. **`BankAccount`**: Contains only the operations shared by **all** accounts:
   - `deposit()`
   - `calculate_interest()`
2. **`WithdrawableAccount(BankAccount)`**: A specialized subclass that introduces:
   - `withdraw()`

```text
              BankAccount
     (owner, balance, deposit)
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
WithdrawableAccount    FixedDepositAccount
 (adds withdraw)          (no withdraw)
      │
├── SavingsAccount
├── CheckingAccount
├── BusinessAccount
└── StudentAccount
```

Now look at how clean this is:
- If a function needs to deposit money or calculate interest, it accepts **`BankAccount`**.
  Both normal accounts and `FixedDepositAccount` will work safely!
- If a function needs to perform withdrawals, it accepts **`WithdrawableAccount`**.
  Only accounts that actually support withdrawals can be passed!

---

<h2 align="center">🛠️ Step-by-Step Code Changes</h2>

### Step 1: Clean `bank.py`
1. Remove `withdraw()` from `BankAccount`.
2. Create the `WithdrawableAccount(BankAccount)` class:
```python
class WithdrawableAccount(BankAccount):
    """A base class for accounts that support withdrawals."""

    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception("Insufficient funds.")
        if amount <= 0:
            raise Exception("Withdrawal amount must be positive.")
        self.balance -= amount
```
3. Add a helper service `BankServices` that specifies honest parameter types:
```python
class BankServices:

    @staticmethod
    def process_deposit(account: BankAccount, amount: float):
        """Any BankAccount can accept a deposit!"""
        account.deposit(amount)

    @staticmethod
    def process_withdrawal(account: WithdrawableAccount, amount: float):
        """Only WithdrawableAccount can be withdrawn from!"""
        account.withdraw(amount)
```

### Step 2: Update `account_types.py`
- Accounts that support withdrawals inherit from `WithdrawableAccount`.
- `FixedDepositAccount` inherits directly from `BankAccount` (it does not have `withdraw()`):
```python
from solid_principles.liskov_substitution.bank import (
    BankAccount,
    WithdrawableAccount,
)


class SavingsAccount(WithdrawableAccount):

    def calculate_interest(self):
        return self.balance * 0.05


class CheckingAccount(WithdrawableAccount):

    def calculate_interest(self):
        return self.balance * 0.02


class BusinessAccount(WithdrawableAccount):

    def calculate_interest(self):
        return self.balance * 0.03


class StudentAccount(WithdrawableAccount):

    def calculate_interest(self):
        return self.balance * 0.01


class FixedDepositAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.07
```

---

<h2 align="center">📦 The Complete Refactored Code</h2>

### 1. `bank.py`

```python
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
        if amount <= 0:
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
    def process_deposit(account: BankAccount, amount: float):
        account.deposit(amount)

    @staticmethod
    def process_withdrawal(account: WithdrawableAccount, amount: float):
        account.withdraw(amount)
```

### 2. `account_types.py`

```python
from solid_principles.liskov_substitution.bank import BankAccount
from solid_principles.liskov_substitution.bank import WithdrawableAccount


class SavingsAccount(WithdrawableAccount):

    def calculate_interest(self):
        return self.balance * 0.05


class CheckingAccount(WithdrawableAccount):

    def calculate_interest(self):
        return self.balance * 0.02


class BusinessAccount(WithdrawableAccount):

    def calculate_interest(self):
        return self.balance * 0.03


class StudentAccount(WithdrawableAccount):

    def calculate_interest(self):
        return self.balance * 0.01


class FixedDepositAccount(BankAccount):

    def calculate_interest(self):
        return self.balance * 0.07
```

### 3. `main.py`

```python
from solid_principles.liskov_substitution.bank import BankServices
from solid_principles.liskov_substitution.account_types import (
    SavingsAccount,
    CheckingAccount,
    BusinessAccount,
    StudentAccount,
    FixedDepositAccount,
)


def main():
    service = BankServices()

    # 1. All accounts (including Fixed Deposit) can accept deposits without issues:
    all_accounts = [
        SavingsAccount("Alice", 1000),
        CheckingAccount("Bob", 1000),
        BusinessAccount("Charlie", 10000),
        StudentAccount("David", 500),
        FixedDepositAccount("Emma", 20000),
    ]

    print("=== Testing Deposits for All Accounts ===")
    for acc in all_accounts:
        service.process_deposit(acc, 100)
        print(
            f"Deposited $100 to {acc.owner} ({type(acc).__name__}) - Balance: ${acc.balance}"
        )

    print("\n=== Testing Withdrawals for Withdrawable Accounts Only ===")
    # 2. Only withdrawable accounts are passed to process_withdrawal:
    withdrawable_accounts = [
        all_accounts[0],  # Alice (SavingsAccount)
        all_accounts[1],  # Bob (CheckingAccount)
        all_accounts[2],  # Charlie (BusinessAccount)
        all_accounts[3],  # David (StudentAccount)
    ]

    for acc in withdrawable_accounts:
        service.process_withdrawal(acc, 200)
        print(f"Withdrew $200 from {acc.owner} - New Balance: ${acc.balance}")


if __name__ == "__main__":
    main()
```

<h3 align="">▶ Running the Code & Output</h3>

Run the script from the root directory:

```bash
python -m solid_principles.liskov_substitution.main
```

Output:

```text
=== Testing Deposits for All Accounts ===
Deposited $100 to Alice (SavingsAccount) - Balance: $1100
Deposited $100 to Bob (CheckingAccount) - Balance: $1100
Deposited $100 to Charlie (BusinessAccount) - Balance: $10100
Deposited $100 to David (StudentAccount) - Balance: $600
Deposited $100 to Emma (FixedDepositAccount) - Balance: $20100

=== Testing Withdrawals for Withdrawable Accounts Only ===
Withdrew $200 from Alice - New Balance: $900
Withdrew $200 from Bob - New Balance: $900
Withdrew $200 from Charlie - New Balance: $9900
Withdrew $200 from David - New Balance: $400
```

---

<h2 align="center">⚖️ Before vs After</h2>

### 🔴 Before (Violating LSP)

- `BankAccount` forced a `withdraw()` method onto every subclass.
- `FixedDepositAccount` could not support withdrawals and threw an error.
- Any client function expecting `BankAccount` would crash when given `FixedDepositAccount`.
- Developers were tempted to add `if isinstance(...)` checks, breaking polymorphism and OCP.

### 🟢 After (Applying LSP)

- `BankAccount` only includes operations that **every** bank account can honor.
- Only accounts that truly support withdrawals inherit from `WithdrawableAccount`.
- Every subclass can safely substitute for its parent without crashes or surprises.
- Zero `if isinstance(...)` checks needed!

---

<h2 align="">👍 3 Simple Rules to Spot an LSP Violation</h2>

1. **A subclass throws "Not Supported" or "Cannot do this"**:
   If a subclass overrides a method just to raise an error because it doesn't
   support that action, that method does not belong in the base class!

2. **A subclass has an empty method (`pass`)**:
   If a subclass overrides a parent method with `pass` because it does nothing,
   it is breaking the contract promised by the parent.

3. **You find yourself writing `if isinstance(...)`**:
   If you have to check the concrete type of an object before calling a method,
   your subclasses are not truly substitutable.

---

<h2 align="center">📝 Summary</h2>

The **Liskov Substitution Principle (LSP)** ensures honest inheritance:

> **A subclass should be able to do everything its parent promised, without surprises or crashes.**

In our banking system:
- **Old Way**: `FixedDepositAccount` inherited `withdraw()` and crashed when called.
- **New Way**: `BankAccount` holds universal behaviors; `WithdrawableAccount` introduces withdrawals. Every subclass safely replaces its parent!

> **If a subclass cannot behave like its parent class, it shouldn't inherit from it.**
