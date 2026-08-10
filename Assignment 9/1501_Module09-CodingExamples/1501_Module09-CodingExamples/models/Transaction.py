from enum import Enum
from datetime import datetime

class TransactionType(Enum):
    DEBIT = "Debit"
    CREDIT = "Credit"
    OTHER = "Other"

    def __str__(self):
        return self.value

class Transaction:
    def __init__(self, t_id : int, transaction_type : TransactionType, date_time : datetime, description : str, mod_amount : float):
        self.__id = t_id
        self.__type = transaction_type
        self.__date_time = date_time
        self.__description = description
        self.__mod_amount = mod_amount

    @property
    def id(self):
        return self.__id

    @property
    def type(self):
        return self.__type
    @property
    def date_time(self):
        return self.__date_time
    @property
    def description(self):
        return self.__description
    @property
    def mod_amount(self):
        return self.__mod_amount

    def __str__(self):
        mod = ""
        if self.mod_amount >= 0:
            mod = "+"
        return f"Type: {self.type}\nDate: {self.date_time}\nDescription: {self.description}\nAmount: {mod}{self.mod_amount}"