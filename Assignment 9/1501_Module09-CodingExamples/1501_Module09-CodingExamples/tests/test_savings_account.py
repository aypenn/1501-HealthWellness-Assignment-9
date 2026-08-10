from unittest import TestCase
from models.BankAccounts import SavingsAccount
from models.Owner import Owner
from datetime import date

class TestSavingsAccount(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.owner = Owner("John", "Smith", "123 Happy St", "Omaha", "NE", "68107", date(1989, 9, 18))

    def setUp(self):
        self.bank_account = SavingsAccount(5555, self.owner, 500)

    def test_apply_monthly_fee(self):
        self.bank_account.balance = 200
        amount = self.bank_account.balance - self.bank_account.monthly_fee
        self.bank_account.apply_monthly_fee()
        self.assertEqual(self.bank_account.balance, amount)

    def test_apply_earned_interest(self):
        self.bank_account.apply_earned_interest()
        self.assertAlmostEqual(self.bank_account.balance, 502.5, places=4)

