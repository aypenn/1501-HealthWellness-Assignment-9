from enum import Enum

class AccountType(Enum):
    CHECKING = "Checking"
    SAVINGS = "Savings"

    def __str__(self):
        return self.value

