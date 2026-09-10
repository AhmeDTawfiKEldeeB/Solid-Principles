
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