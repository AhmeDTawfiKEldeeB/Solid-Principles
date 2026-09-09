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