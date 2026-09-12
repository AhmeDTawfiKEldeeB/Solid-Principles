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