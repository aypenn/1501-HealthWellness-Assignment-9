from unittest import TestCase
from models.BankAccounts import CheckingAccount
from models.Owner import Owner
from datetime import date

class TestCheckingAccount(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.owner = Owner("John", "Smith", "123 Happy St", "Omaha", "NE", "68107", date(1989, 9, 18))

    def setUp(self):
        self.bank_account = CheckingAccount(5555, self.owner, 500)

    def test_apply_monthly_fee(self):
        amount = self.bank_account.balance - self.bank_account.monthly_fee
        self.bank_account.apply_monthly_fee()
        self.assertEqual(amount, self.bank_account.balance)

    def test_negative_set_limit(self):
        self.bank_account.limit = -10
        self.assertEqual(self.bank_account.limit, 300)

    def test_debit_over_limit(self):
        self.assertFalse(self.bank_account.debit(500))

    def test_debit_under_limit(self):
        self.assertTrue(self.bank_account.debit(100))

    def test_no_fee_applied_with_eligible_credit(self):
        self.assertTrue(self.bank_account.apply_fee)
        self.bank_account.credit(500)
        self.assertFalse(self.bank_account.apply_fee)