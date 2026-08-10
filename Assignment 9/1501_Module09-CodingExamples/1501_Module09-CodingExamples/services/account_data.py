from models.BankAccounts import CheckingAccount, SavingsAccount
from models.AccountType import AccountType
from models.Owner import Owner
from datetime import date
import random

accounts = {}
owners = set()

def filter_account_transactions_by_year(account_num, year):
    current = search_account(account_num)
    return [t for t in current.transactions if t.date_time.year == year]

def filter_account_transactions_by_month(account_num, month, year):
    current = search_account(account_num)
    return [t for t in current.transactions if t.date_time.month == month and t.date_time.year == year]

def filter_account_transaction_by_range(account_num, start_date, end_date):
    current = search_account(account_num)
    return [t for t in current.transactions if start_date <= t.date_time.date() <= end_date]

def filter_accounts(account_type : AccountType):
    return [account for account in accounts.values() if account.account_type == account_type]

def get_all_checking_accounts():
    return [account for account in accounts.values() if account.account_type == AccountType.CHECKING]

def get_all_savings_accounts():
    return [account for account in accounts.values() if account.account_type == AccountType.SAVINGS]

def add_owner(owner : Owner):
    owners.add(owner)

def search_owner_name(name : str) -> list[Owner]:
    search = []
    for owner in owners:
        if name.lower() in owner.full_name.lower():
            search.append(owner)
    return search

def search_owner_id(owner_id : str) -> Owner | None:
    for owner in owners:
        if owner.id == owner_id:
            return owner
    return None # no owners found

def account_exists(account_num : int) -> bool:
    return account_num in accounts

def add_account(account : CheckingAccount | SavingsAccount):
    accounts[account.account_num] = account

def search_account(account_num : int) -> CheckingAccount | SavingsAccount:
    return accounts.get(account_num) # returns "None" by default if not there

def deposit_account(account_num : int, amount : float, trans_desc : str) -> bool:
    if account_exists(account_num):
        return accounts.get(account_num).credit(amount, trans_desc)
    return False

def withdraw_account(account_num : int, amount : float, trans_desc : str) -> bool:
    if account_exists(account_num):
        return accounts.get(account_num).debit(amount, trans_desc)
    return False

def apply_monthly_fees():
    for a in accounts.values():
        a.apply_monthly_fee()

# reset monthly charge to True for applying
def reset_monthly_fee_check():
    for a in accounts.values():
        if a.account_type == AccountType.CHECKING:
            a.apply_fee = True

def load_test_data():
    """
    Loads sample owners, accounts, and transactions for testing/demo purposes.
    """

    # -------------------------
    # Create Owners
    # -------------------------
    ''' owner_list = [
            Owner("AJ123", "Alice", "Johnson", "123 Maple St", "Omaha", "NE", "68102", date(1985, 4, 12)),
            Owner("BS123", "Bob", "Smith", "456 Oak Ave", "Omaha", "NE", "68106", date(1990, 7, 23)),
            Owner("CD123","Carol", "Davis", "789 Pine Rd", "Bellevue", "NE", "68005", date(1978, 1, 9)),
            Owner("DM123", "David", "Miller", "321 Birch Ln", "Papillion", "NE", "68046", date(1982, 11, 30)),
            Owner("EW123", "Eva", "Wilson", "654 Cedar Ct", "La Vista", "NE", "68128", date(1995, 6, 18)),
        ]
    
        for owner in owner_list:
            add_owner(owner)
        '''
    # -------------------------
    # Create 20 Accounts
    # -------------------------
    owner_list = list(owners)
    for _ in range(20):

        # match main.py random account number logic
        account_num = random.randint(10000000, 99999999)
        while account_exists(account_num):
            account_num = random.randint(10000000, 99999999)

        primary_owner = random.choice(owner_list)
        starting_balance = random.uniform(800, 3000)

        if random.choice([True, False]):
            account = CheckingAccount(
                account_num,
                primary_owner,
                starting_balance,
                limit=500,
                monthly_fee=5
            )
        else:
            account = SavingsAccount(
                account_num,
                primary_owner,
                starting_balance,
                minimum_balance=300,
                earned_interest=0.01
            )

        # Optional second owner
        if random.choice([True, False]):
            second_owner = random.choice(owner_list)
            if second_owner != primary_owner:
                account.add_owner(second_owner)

        add_account(account)
        print(account_num)

        # -------------------------
        # Transactions (safe values)
        # -------------------------
        for i in range(random.randint(2, 3)):
            account.credit(
                random.uniform(100, 500),
                f"Test Deposit {i + 1}"
            )

        for i in range(random.randint(2, 3)):
            debit_amount = random.uniform(50, 250)
            if debit_amount < account.balance:
                account.debit(
                    debit_amount,
                    f"Test Withdrawal {i + 1}"
                )