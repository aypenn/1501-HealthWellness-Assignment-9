
from unittest import TestCase
from models.Account import BankAccount
from models.AccountType import AccountType
from models.Owner import Owner
from datetime import date

class TestBankAccount(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.owner = Owner("John", "Smith", "123 Happy St", "Omaha", "NE", "68107", date(1989, 9, 18))

    def setUp(self):
        self.bank_account = BankAccount(5555, self.owner, 500.0, AccountType.CHECKING)

    def test_initial_balance(self):
        self.assertEqual(self.bank_account.balance, 500.0)

    def test_negative_balance_sets_to_zero(self):
        self.bank_account.balance = -200
        self.assertEqual(self.bank_account.balance, 0)

    def test_credit_balance(self):
        self.bank_account.credit(250)
        self.assertEqual(self.bank_account.balance, 750.0)

    def test_negative_credit_balance(self):
        self.bank_account.credit(-250)
        self.assertEqual(self.bank_account.balance, 500.0)

    def test_debit_balance(self):
        self.bank_account.debit(250)
        self.assertEqual(self.bank_account.balance, 250.0)

    def test_negative_debit_balance(self):
        self.bank_account.debit(-250)
        self.assertEqual(self.bank_account.balance, 500.0)

    def test_debit_above_balance(self):
        self.bank_account.debit(1000)
        self.assertEqual(self.bank_account.balance, 500.0)

    def test_not_eq_accounts(self):
        ba2 = BankAccount(5544, self.owner, 500.0, AccountType.CHECKING)
        self.assertNotEqual(ba2, self.bank_account)

    def test_eq_accounts(self):
        ba2 = BankAccount(5555, self.owner, 200, AccountType.SAVINGS)
        self.assertEqual(ba2, self.bank_account)

    def test_str_includes_account_type_and_balance(self):
        text = str(self.bank_account)
        self.assertIn("Checking", text)
        self.assertIn("Balance", text)