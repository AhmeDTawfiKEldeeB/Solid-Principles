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
