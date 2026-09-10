from solid_principles.single_responsibility.bank import InterestCalculator, AccountFormatter
from solid_principles.open_closed.account_types import (SavingsAccount,CheckingAccount,BusinessAccount,StudentAccount)

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
