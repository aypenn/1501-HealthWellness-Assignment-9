import json
import os

from models.AccountType import AccountType
from models.BankAccounts import CheckingAccount, SavingsAccount
from services.account_data import accounts, add_account, search_owner_id
import services.account_database as db

def write_out_accounts():
    json_data = [account.to_dict() for account in accounts.values()]

    with open('accounts.json', 'w') as file:
        json.dump(json_data, file, indent=4)


def read_in_accounts(filename):
    if not os.path.exists(filename):
        return # break out of this function, no file will create on exit

    with open(filename) as file:
        data = json.load(file)

    for item in data:
        new_account = None

        # get all the data, turn into a bank account
        account_num = item.get("account_num", 0)
        owner_list = item.get("owners", [])
        owners = []
        for o_id in owner_list:
            #owners.append(search_owner_id(o_id))
            owners.append(db.get_owner_via_id(o_id))

        a_type = AccountType(item.get("account_type"))
        balance = item.get("balance", 0.0)
        monthly_fee = item.get("monthly_fee", 5.0)
        if a_type == AccountType.CHECKING:
            no_fee_amount = item.get("no_fee_amount", 300)
            limit = item.get("limit", 300)
            apply_fee = item.get("apply_fee", True)
            new_account = CheckingAccount(account_num, owners, balance, limit, monthly_fee, no_fee_amount, apply_fee)
            db.add_checking_account(new_account) # going to the database table
        else:
            minimum_balance = item.get("minimum_balance", 300)
            earned_interest = item.get("earned_interest", 0.005)
            new_account = SavingsAccount(account_num, owners, balance, minimum_balance, monthly_fee, earned_interest)
            db.add_savings_account(new_account) # going to the database table.

        #add_account(new_account) # add into the system
