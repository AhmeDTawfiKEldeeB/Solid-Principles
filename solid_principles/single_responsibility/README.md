# Single Responsibility Principle (SRP)

## What is the Single Responsibility Principle?

The **Single Responsibility Principle (SRP)** is the first principle of SOLID.

It states:

> **A class should have only one reason to change.**

In simple terms, a class should have one clear responsibility.

This does not mean that a class should contain only one method.
Instead, the functionality inside a class should belong to the same
responsibility.

The goal is to keep classes focused, easier to understand, and easier to
change when requirements evolve.

---

## Why Do We Need SRP?

A class can start small and still look perfectly fine.

The problem usually appears later.

As the application grows, new requirements are added. More functionality is
introduced, and developers may naturally add that functionality to an
existing class because it already seems related.

Over time, the class can become responsible for several different things.

Now, a change in one responsibility can affect code that belongs to another
responsibility.

This makes the class harder to maintain, harder to test, and more difficult
to understand.

SRP helps us prevent this by keeping responsibilities separated.

----------
So,Imagine that we are building a simple **banking system**.

The bank currently has many customers, and each customer has a
`BankAccount`.

At the beginning, the requirements are very simple.

We need a bank account that can:

- Store the account owner's name
- Store the current balance
- Deposit money
- Withdraw money

So we start with a simple `BankAccount` class.

```python
class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

```
and let's run it:
```python
from bank import BankAccount
def main():
    account = BankAccount("John Doe", 1000)
    print(f"Account Owner: {account.owner}")
    print(f"Initial Balance: ${account.balance}")

    account.deposit(500)
    print(f"Balance after deposit: ${account.balance}")

    account.withdraw(200)
    print(f"Balance after withdrawal: ${account.balance}")

if __name__ == "__main__":
    main()
```
The code works perfectly, there are no issues, and the output is perfect

- Account Owner: John Doe
- Initial Balance: $1000
- Balance after deposit: $1500
- Balance after withdrawal: $130

**The problem is that it'll start when we begin adding functions like this**
```python
class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def calculate_interest(self):
        return self.balance * 0.05

    def to_json(self):
        return {
            "owner": self.owner,
            "balance": self.balance,
        }
```
and That's the output:
- Account Owner: John Doe
- Initial Balance: $1000
- Balance after deposit: $1500
- Balance after withdrawal: $1300
- Interest: $65.0
- JSON: {'owner': 'John Doe', 'balance': 1300}

The program is working perfectly,no problems at all. So what's the problem now?



## So, What's the Problem?

The important thing to understand here is that the problem is **not** that
the program is producing incorrect results.

The program works perfectly.

The problem is the **responsibility of the `BankAccount` class**.

When we first created the class, its responsibility was simple:

```text
BankAccount
│
├── owner
├── balance
├── deposit()
└── withdraw()
```

Everything inside the class was directly related to managing the bank
account.

But as the requirements grew, we started adding more functionality:

```text
BankAccount
│
├── Account management
│   ├── deposit()
│   └── withdraw()
│
├── Interest calculation
│   └── calculate_interest()
│
└── Data formatting
    └── to_json()
```

Now the BankAccount class has more than one responsibility.

### The SRP Violation

Let's look at the two new methods we added.

#### `calculate_interest()`

```python
def calculate_interest(self):
    return self.balance * 0.05
```

This method is responsible for calculating interest.

If the bank changes the interest calculation rules, for example:

- The interest rate changes
- Different account types have different rates
- A more complicated formula is introduced

we would need to modify the BankAccount class.

#### `to_json()`

```python
def to_json(self):
    return {
        "owner": self.owner,
        "balance": self.balance,
    }
```

This method is responsible for formatting the account data.

If the way we represent the account changes, for example:

- We change the JSON structure
- We add or remove fields
- We introduce another output format

we would also need to modify the BankAccount class.

### Multiple Reasons to Change

This means that our BankAccount class now has several different reasons
to change.

For example:

```text
Interest calculation changes
          ↓
    BankAccount changes


JSON format changes
          ↓
    BankAccount changes


Account operations change
          ↓
    BankAccount changes
```

This is exactly what SRP tells us to avoid.

A class should have only one reason to change.

Our BankAccount class currently has multiple reasons to change.

Therefore, it violates the Single Responsibility Principle.

### Why Is This a Problem?

At the moment, the class is still small, so the problem may not seem serious.

But imagine that the banking system continues to grow.

More requirements will be added:

- Generate account statements
- Calculate transaction fees
- Export account information
- Send account notifications
- Calculate different types of interest

If we keep adding everything to BankAccount, the class will continue to grow.

Eventually, we could end up with something like:

```text
BankAccount
│
├── Account management
├── Interest calculation
├── Fee calculation
├── Statement generation
├── JSON formatting
├── Notification handling
└── ...
```

Now a class that was originally responsible for representing a bank account
has become responsible for completely different concerns.

This makes the code harder to maintain.

A change in one responsibility can also affect code related to another
responsibility, making the system more difficult to understand and test.

### The Better Approach

Instead of making BankAccount responsible for everything, we can separate
these responsibilities into different classes.

For example:

```text
BankAccount
│
├── Account management
│
InterestCalculator
│
└── Interest calculation

AccountFormatter
│
└── Data formatting
```

Now each class has a clear responsibility and a clear reason to change.

The BankAccount will focus on the account itself, while other classes will
handle functionality that does not belong to its core responsibility.

### Before Refactoring

Our current design looks like this:

```text
                  BankAccount
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 Account Management   Interest      Formatting
                      Calculation
```

The next step is to refactor this design using SRP.

We will move the responsibilities that do not belong to
BankAccount into separate classes and then run the program again to make
sure the behavior remains the same.



## Refactoring the Design

Now that we understand the problem, we can refactor the design.

The goal is not to change how the program works.

The goal is to change **how the responsibilities are organized**.

Our `BankAccount` should focus only on managing the bank account itself.

The responsibilities for calculating interest and formatting account data
should be moved into separate classes.

So instead of having everything inside `BankAccount`, we will separate the
responsibilities:

```text
BankAccount
│
├── Account management
│   ├── deposit()
│   └── withdraw()
│
InterestCalculator
│
└── Interest calculation
│
AccountFormatter
│
└── Data formatting
```

### Step 1 — Keep BankAccount Focused

The BankAccount class is now responsible only for managing the account.

```python
class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount
```

The BankAccount no longer knows how to calculate interest or format its
data.

Its responsibility is simply managing the account.

### Step 2 — Move Interest Calculation

We create a separate InterestCalculator class.

```python
class InterestCalculator:

    def calculate_interest(self, account):
        return account.balance * 0.05
```

Now, the interest calculation has its own responsibility.

If the bank changes the way interest is calculated, we can modify
InterestCalculator without changing BankAccount.

### Step 3 — Move Data Formatting

We also create a separate AccountFormatter class.

```python
class AccountFormatter:

    def to_json(self, account):
        return {
            "owner": account.owner,
            "balance": account.balance,
        }
```

Now, formatting the account data is no longer the responsibility of
BankAccount.

If the format changes, we can modify AccountFormatter without changing
the account management logic.

### The Refactored Design

Our complete implementation is now:

```python
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
```

### Updating the Main Function

The main function now uses the appropriate class for each responsibility.

```python
from bank import BankAccount, InterestCalculator, AccountFormatter


def main():

    account = BankAccount("John Doe", 1000)

    print(f"Account Owner: {account.owner}")
    print(f"Initial Balance: ${account.balance}")

    account.deposit(500)
    print(f"Balance after deposit: ${account.balance}")

    account.withdraw(200)
    print(f"Balance after withdrawal: ${account.balance}")

    interest_calculator = InterestCalculator()
    interest = interest_calculator.calculate_interest(account)

    print(f"Interest: ${interest}")

    formatter = AccountFormatter()
    account_json = formatter.to_json(account)

    print(f"JSON: {account_json}")


if __name__ == "__main__":
    main()
```

### ▶️ Running the Refactored Program

After the refactoring, the behavior of the program remains the same.

The program produces:

```text
Account Owner: John Doe
Initial Balance: $1000
Balance after deposit: $1500
Balance after withdrawal: $1300
Interest: $65.0
JSON: {'owner': 'John Doe', 'balance': 1300}
```

The important point here is that we changed the design, not the
behavior of the program.

The program still produces the same results, but the responsibilities are
now separated.

### Before vs After

#### Before

The BankAccount class was responsible for several different things:

```text
BankAccount
│
├── Account management
├── Interest calculation
└── Data formatting
```

This gave the class multiple reasons to change.

#### After

The responsibilities are now separated:

```text
BankAccount
│
├── Account management
│
InterestCalculator
│
└── Interest calculation
│
AccountFormatter
│
└── Data formatting
```

Now each class has a clear responsibility.

If account management changes, we modify BankAccount.

If the interest calculation changes, we modify InterestCalculator.

If the output format changes, we modify AccountFormatter.

### Why Is This Better?

The refactored design makes the code easier to maintain.

Each class is focused on one responsibility, so changes are more isolated.

For example, imagine that the bank changes the interest rate from 5% to
7%.

We only need to change:

```python
class InterestCalculator:

    def calculate_interest(self, account):
        return account.balance * 0.07
```

We do not need to modify BankAccount.

The same applies to formatting.

If the JSON structure changes, we modify AccountFormatter without touching
the account management logic.

This separation makes the system easier to understand, maintain, and test.

### Thumb Rules

Some practical rules can help identify SRP violations:

- A class should have one clear responsibility.
- Methods inside a class should belong to the same responsibility.
- A class should have only one reason to change.
- If a method performs a responsibility that could belong to another class,
consider separating it.
- Avoid putting unrelated functionality into an existing class just because
it is convenient.
- Keep classes focused rather than creating large classes that handle many
different concerns.

These are useful guidelines rather than strict rules. They should be applied
with context rather than mechanically.

### Summary

The Single Responsibility Principle does not mean that every class should
be extremely small or contain only one method.

The main idea is to keep responsibilities focused.

In our example, BankAccount originally handled:

- Account management
- Interest calculation
- Data formatting

This gave the class multiple reasons to change.

After applying SRP, we separated those responsibilities:

```text
BankAccount
    → Account management

InterestCalculator
    → Interest calculation

AccountFormatter
    → Data formatting
```

The program still works exactly as before, but the design is now easier to
maintain and change.

> **A class should have only one reason to change.**
