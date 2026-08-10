
from models.Account import BankAccount
from models.AccountType import AccountType
from models.Transaction import *
from datetime import datetime


class CheckingAccount(BankAccount):
    LIMIT_DEFAULT = 300
    MONTHLY_FEE_DEFAULT = 5
    NO_FEE_AMOUNT_DEFAULT = 300
    def __init__(self, account_num, owners, balance, limit=LIMIT_DEFAULT, monthly_fee=MONTHLY_FEE_DEFAULT, no_fee_amount=NO_FEE_AMOUNT_DEFAULT, apply_fee=True):
        super().__init__(account_num, owners, balance, AccountType.CHECKING)
        self.monthly_fee = monthly_fee
        self.limit = limit
        self.__no_fee_amount = no_fee_amount
        self.__apply_fee = apply_fee

    @property
    def monthly_fee(self):
        return self.__monthly_fee
    @monthly_fee.setter
    def monthly_fee(self, monthly_fee):
        if monthly_fee > 0:
            self.__monthly_fee = monthly_fee
        else:
            self.__monthly_fee = self.MONTHLY_FEE_DEFAULT

    @property
    def no_fee_amount(self):
        return self.__no_fee_amount
    @no_fee_amount.setter
    def no_fee_amount(self, no_fee_amount):
        if no_fee_amount > 0:
            self.__no_fee_amount = no_fee_amount
        else:
            self.__no_fee_amount = self.NO_FEE_AMOUNT_DEFAULT

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, limit):
        if limit > 0:
            self.__limit = limit
        else:
            self.__limit = self.LIMIT_DEFAULT

    @property
    def apply_fee(self):
        return self.__apply_fee

    def apply_monthly_fee(self):
        if self.__apply_fee:
            self._balance -= self.__monthly_fee # no matter what, take out the fee
            import services.account_database as db
            db.update_account_balance(self.account_num, -self.__apply_fee)
            super().add_transaction(Transaction(TransactionType.DEBIT, datetime.now(), "Monthly Fee", -self.__monthly_fee))

    def debit(self, amount: float, trans_desc : str):
        if amount < self.__limit:
            return super().debit(amount, trans_desc)
        return False

    def credit(self, amount: float, trans_desc : str):
        if amount >= self.__no_fee_amount:
            self.__apply_fee = False
        return super().credit(amount, trans_desc)

    def reset_apply_fee(self):
        self.__apply_fee = True

    def update_fee_on_db(self):
        import services.account_database as db
        db.update_checking_apply_fee(self.account_num, self.__apply_fee)

    def to_dict(self):
        owner_list = [o.id for o in self._owners]
        return {"account_num": self._account_num, "owners" : owner_list, "account_type" : str(self._account_type),
                "balance" : self._balance, "monthly_fee" : self.__monthly_fee, "no_fee_amount" : self.__no_fee_amount,
                "limit" : self.__limit, "apply_fee" : self.__apply_fee}

    def __str__(self):
        return super().__str__() + f"\nLimit: ${self.__limit:.2f}\nMonthly Fee: ${self.__monthly_fee:.2f}"


class SavingsAccount(BankAccount):
    MINIMUM_DEFAULT = 300
    EARNED_INTEREST_DEFAULT = .005
    MONTHLY_FEE_DEFAULT = 5
    def __init__(self, account_num, owners, balance, minimum_balance=MINIMUM_DEFAULT, monthly_fee=MONTHLY_FEE_DEFAULT, earned_interest=EARNED_INTEREST_DEFAULT):
        super().__init__(account_num, owners, balance, AccountType.SAVINGS)
        self.__minimum_balance = minimum_balance
        self.__earned_interest = earned_interest
        self.__monthly_fee = monthly_fee

    @property
    def minimum_balance(self):
        return self.__minimum_balance

    @minimum_balance.setter
    def minimum_balance(self, minimum_balance):
        if minimum_balance > 0:
            self.__minimum_balance = minimum_balance
        else:
            self.__minimum_balance = self.MINIMUM_DEFAULT

    @property
    def monthly_fee(self):
        return self.__monthly_fee

    @monthly_fee.setter
    def monthly_fee(self, monthly_fee):
        if monthly_fee > 0:
            self.__monthly_fee = monthly_fee
        else:
            self.__monthly_fee = self.MONTHLY_FEE_DEFAULT

    @property
    def earned_interest(self):
        return self.__earned_interest

    @earned_interest.setter
    def earned_interest(self, earned_interest):
        if earned_interest > 0:
            self.__earned_interest = earned_interest
        else:
            self.__earned_interest = self.EARNED_INTEREST_DEFAULT

    def apply_monthly_fee(self):
        if self._balance < self.__minimum_balance:
            self._balance -= self.__monthly_fee
            import services.account_database as db
            db.update_account_balance(self.account_num, -self.__monthly_fee)
            super().add_transaction(Transaction(TransactionType.DEBIT, datetime.now(), "Monthly Fee", -self.__monthly_fee))

    def apply_earned_interest(self):
        self.credit(self.earned_interest*self.balance, "Monthly Earned Interest")

    def to_dict(self):
        owner_list = [o.id for o in self._owners]
        return {"account_num": self._account_num, "owners" : owner_list, "account_type" : str(self._account_type),
                "balance" : self._balance, "monthly_fee" : self.__monthly_fee, "minimum_balance" : self.__minimum_balance,
                "earned_interest" : self.__earned_interest}

    def __str__(self):
        return super().__str__() + f"\nMinimum Balance: ${self.__minimum_balance:.2f}\nInterest Rate: {self.__earned_interest*100:.2f}%"

