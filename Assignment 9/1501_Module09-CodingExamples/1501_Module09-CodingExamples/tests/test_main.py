import main
from unittest import TestCase
from unittest.mock import patch
from models.Owner import Owner
from datetime import date
from models.BankAccounts import CheckingAccount, SavingsAccount
import services.account_data as ad

class TestMainSystem(TestCase):
    def setUp(self):
        ad.accounts.clear()


    @patch("main.random.randint", return_value=5555)
    @patch("main.prompt_float", side_effect=[1000, 300, 10])
    @patch("main.input", side_effect=["John", "Smith", "123 Happy St", "Omaha", "NE", "681007", "09-18-1989"])
    @patch("main.prompt_int_range", return_value=1)
    def test_add_account_creates_checking(self, m_int_range, m_input, m_float, m_rand):
        main.add_account()

        # do our tests
        self.assertIn(5555, ad.accounts)
        acct = ad.accounts[5555]

        self.assertEqual(acct.account_num, 5555)
        self.assertEqual(acct.balance, 1000)
        self.assertEqual(acct.limit, 300)
        self.assertEqual(acct.monthly_fee, 10)
        self.assertEqual(acct.owners[0].first_name, "John")
        self.assertEqual(acct.owners[0].last_name, "Smith")

    @patch("builtins.print")
    @patch("main.prompt_float", return_value=200)
    @patch("main.prompt_int_range", return_value=123456)
    def test_deposit_money(self, m_int_range, m_prompt_float, m_print):
        owner = Owner("John", "Smith", "123 Happy St", "Omaha", "NE", "681007", date(1989, 9, 18))
        acct = CheckingAccount(123456, owner, 500, 300, 10)
        ad.add_account(acct)

        main.deposit_money()

        self.assertEqual(ad.accounts[123456].balance, 700)
        m_print.assert_any_call("*Account deposited")

    @patch("builtins.print")
    @patch("main.prompt_float", return_value=100)
    @patch("main.prompt_int_range", return_value=123456)
    def test_withdraw_money(self, m_int_range, m_prompt_float, m_print):
        owner = Owner("John", "Smith", "123 Happy St", "Omaha", "NE", "681007", date(1989, 9, 18))
        acct = CheckingAccount(123456, owner, 500, 300, 10)
        ad.add_account(acct)

        main.withdraw_money()

        self.assertEqual(ad.accounts[123456].balance, 400)
        m_print.assert_any_call("*Account withdrawn")







