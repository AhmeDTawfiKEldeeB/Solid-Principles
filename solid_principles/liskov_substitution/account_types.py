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
   
