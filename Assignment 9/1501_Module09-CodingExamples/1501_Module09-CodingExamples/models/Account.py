from datetime import date
from models.Owner import Owner
from models.AccountType import AccountType
from models.Transaction import *
from datetime import datetime

class BankAccount:
    routing_number = 100010076
    bank_name = "Bank of MCC"

    def __init__(self, account_num : int, owners : list[Owner], balance : float, account_type : AccountType):
        self._account_num = account_num
        self._owners = owners
        #self._owners.append(owner)
        self._transactions = []
        #self._transactions.append(Transaction(TransactionType.OTHER, datetime.now(), "Account Created", balance))
        self.balance = balance # calling the setter here
        self._account_type = account_type

    @property
    def account_type(self) -> AccountType:
        return self._account_type
    @account_type.setter
    def account_type(self, account_type : AccountType):
        self._account_type = account_type

    @property
    def account_num(self) -> int:
        return self._account_num

    @property
    def owners(self) -> list:
        return self._owners

    def get_one_owner(self, index) -> Owner:
        return self._owners[index]

    def add_owner(self, owner : Owner) -> bool:
        if owner not in self._owners:
            self._owners.append(owner)
            return True
        return False

    def remove_owner(self, index):
        if 0 <= index < len(self._owners):
            return self._owners.pop(index)
        return None

    @property
    def transactions(self):
        return self._transactions

    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, balance : float):
        if balance > 0:
            self._balance = balance
        else:
            self._balance = 0

    def debit(self, amount : float, trans_desc : str): # taking out money
        if amount < self._balance and amount > 0:
            self._balance -= amount
            self.add_transaction(Transaction(TransactionType.DEBIT, datetime.now(), trans_desc, -amount))
            return True
        return False

    def credit(self, amount : float, trans_desc : str):  # adding money
        if amount > 0:
            self._balance += amount
            self.add_transaction(Transaction(TransactionType.CREDIT, datetime.now(), trans_desc, amount))
            return True
        return False

    def add_transaction(self, new_transaction : Transaction):
        self._transactions.append(new_transaction)
        import services.account_database as db
        db.add_transaction(self.account_num, new_transaction)  # adds it into the database

    def delete_transaction(self, index: int):
        delete = self._transactions.pop(index)
        import services.account_database as db
        return db.delete_transaction_by_id(delete.id)

    def str_owners(self):
        value = ""
        for owner in self._owners:
            value += str(owner) + "\n"
        return value

    def apply_monthly_fee(self):
        raise NotImplementedError("need apply_monthly_fee")

    def __str__(self):
        return f"Type: {self._account_type.value}\nAccount Number: {self._account_num}\nOwners:\n{self.str_owners()}\nBalance: ${self._balance:.2f}"

    def __eq__(self, other):
        try:
            return self._account_num == other.account_num
        except Exception:
            return False

