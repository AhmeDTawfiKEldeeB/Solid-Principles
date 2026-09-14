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

    print("\n=== 2. Swapping to Email Notifier (Zero Changes to BankTransactionService!) ===")
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

    print("\n[SUCCESS] High-level service depends on Notifier abstraction, not concrete tools!")
    print("[SUCCESS] We can plug in any notification tool without changing business logic!")


if __name__ == "__main__":
    main()
