from models import Account
# this bank account system has us add, view, and remove accounts as needed.
# other functionality include withdraw/deposit money as well

#import services.account_data as ad
from models.Transaction import TransactionType
from utils.input_utils import *
import random
from models.BankAccounts import CheckingAccount, SavingsAccount
from models.Owner import Owner
from models.AccountType import AccountType
from datetime import datetime, timedelta
from services.data_csv_io import *
from services.data_xml_io import *
from services.data_json_io import *
import services.account_database as db

def prompt_date(prompt):
    while True:
        value = get_valid_date(input(prompt))
        if value is not None:
            return value
        print("Error, date entered not valid.")

def add_owner():
    print("* Add Owner *")
    id = input("Enter owner ID: ")
    first_name = input("Enter account owner first name: ")
    last_name = input("Enter account owner last name: ")
    address = input("Enter owner address: ")
    city = input("Enter owner city: ")
    state = input("Enter owner state: ")
    zipcode = input("Enter owner zipcode: ")
    dob = prompt_date("Enter in owner date of birth(MM-DD-YYYY): ")

    new_owner = Owner(id, first_name, last_name, address, city, state, zipcode, dob)
    #ad.add_owner(new_owner) # add to the set

    if db.owner_exists(id, first_name, last_name, dob):
        print("Owner already exists.")
        return
    # owner doesn't exist so add
    db.add_owner(new_owner)

def search_for_owner(name : str):
    #owner_list = ad.search_owner_name(name)
    owner_list = db.get_owners_via_name(name)
    if len(owner_list) == 0:
        print("No owners found with that name.")
        print()
        return None

    print("\n* Owners found: ")
    for i in range(len(owner_list)):
        print(f"{i+1}. {owner_list[i].full_name}")
    print(f"{len(owner_list)+1}. No owner, exit.")

    choice = prompt_int_range("Select owner: ", 1, len(owner_list)+1)

    if choice == len(owner_list)+1:
        print()
        return None # no owner found in list that matches search.

    return owner_list[choice-1] # off by one



def add_account():
    print("* Add Account *")
    for index, account_type in enumerate(AccountType, start=1): # print off my options of the enum
        print(f"{index}. {account_type.value}")

    choice = prompt_int_range("Choose Account Type: ", 1, len(AccountType))

    choice_enum = list(AccountType)[choice-1]

    account_num = random.randint(10000000,99999999)

    #can't have duplicate account numbers, get a new number

    #while ad.account_exists(account_num):
    while db.account_exists_via_id(account_num):
        #print("Account number already used.")
        account_num = random.randint(10000000,99999999)

    print("Account Number:", account_num)

    # owner stuff here - search
    name = input("Enter name to search: ")
    owner = search_for_owner(name) # do a search
    while owner is None:
        name = input("Enter name to search(Q to quit): ")
        if name.lower() == "q":
            return # go back to the main to add owner to then back adding account
        owner = search_for_owner(name)


    balance = prompt_float("Enter account starting balance: ")

    new_account = None # making this to use in the if statements

    if choice_enum == AccountType.CHECKING:
        limit = prompt_float("Enter account withdraw limit: ")
        monthly_fee = prompt_float("Enter account monthly fee: ")
        new_account = CheckingAccount(account_num, [owner], balance, limit, monthly_fee)
        db.add_checking_account(new_account)
    elif choice_enum == AccountType.SAVINGS:
        minimum_balance = prompt_float("Enter account minimum balance: ")
        earned_interest = prompt_float("Enter account earned interest rate: ")
        new_account = SavingsAccount(account_num, [owner], balance, minimum_balance, earned_interest)
        db.add_savings_account(new_account)

    #add new account transaction only if really adding in - not reading from file.
    # this inserts the transaction into the table
    new_account.add_transaction(Transaction(TransactionType.OTHER, datetime.now(), "Account Created", balance))

    # add to the dictionary
    #ad.add_account(new_account)


def view_account():
    month_map = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
                 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

    account_num = prompt_int_range("Enter account number to view: ", 10000000,99999999)
    # if account found print out information

    #current = ad.search_account(account_num)
    current = db.get_account_via_number(account_num)
    if not current:
        print("Account not found.")
        return

    choice = 0
    while choice != 4:
        print("Account Info:")
        print(current)

        print("1. View Transaction by Year")
        print("2. View Transaction by a Month")
        print("3. View Transaction by a Range")
        print("4. Exit to main menu")

        choice = prompt_int_range("Select option: ", 1, 4)
        filter_list = [] # list to use and print out
        print()
        if choice == 1:
            year = prompt_int("Enter year to filter: ")
            #filter_list = ad.filter_account_transactions_by_year(account_num, year)

            # can do it this way with separate functions
            #filter_list = db.get_transactions_on_account_via_year(account_num, year)

            # OR this way with one function for all to build the date here and send over
            start_date = str(year) + "-01-01"
            end_date = str(year+1) + "-01-01"
            filter_list = db.get_transactions_on_account_via_range(account_num, start_date, end_date)
            print(f"* Transaction in {year}")
        elif choice == 2:
            year = prompt_int("Enter year of month to filter: ")
            month = prompt_int_range("Enter month to filter(1-12): ", 1, 12)
            #filter_list = ad.filter_account_transactions_by_month(account_num, month, year)

            #Again using specfic function
            #filter_list = db.get_transactions_on_account_via_month(account_num, year, month)

            # OR build the date here and call the same function for all
            start_date = f"{year}-{month:02}-01"
            if month >= 12:
                month = 0
                year += 1
            end_date = f"{year}-{month + 1:02}-01"
            filter_list = db.get_transactions_on_account_via_range(account_num, start_date, end_date)
            print(f"* Transaction in {month_map[month]} month")
        elif choice == 3:
            start_date = prompt_date("Enter start date: ")
            end_date = prompt_date("Enter end date: ")
            while end_date < start_date:
                print("* Error, start date must come before end date.")
                start_date = prompt_date("Enter start date: ")
                end_date = prompt_date("Enter end date: ")
            #filter_list = ad.filter_account_transaction_by_range(account_num, start_date, end_date)
            # no modification here other than adding 1 to the day
            end_date = end_date + timedelta(days=1)
            filter_list = db.get_transactions_on_account_via_range(account_num, str(start_date), str(end_date))
            print(f"* Transaction between {start_date} and {end_date}")


        if len(filter_list) == 0:
            print("Sorry, no transaction during this date range.")
        for transaction in filter_list:
            print(transaction)

        net_transaction_amount = sum([t.mod_amount for t in filter_list])
        print(f"\n* Transaction Net Amount *\n${net_transaction_amount:.2f}")





def deposit_money():
    account_num = prompt_int_range("Enter account number to view: ", 10000000,99999999)
    #if ad.account_exists(account_num):

    current = db.get_account_via_number(account_num)

    if not current:
        print("Account not found.")
        return

    deposit = prompt_float("Enter deposit amount: ")
    desc = input("Enter deposit description: ")

    if current.credit(deposit, desc) and db.update_account_balance(account_num, deposit):
        print("*Account deposited")
        print("New Balance: ", current.balance)
    else:
        print("Error, can't deposit money.")


def withdraw_money():
    account_num = prompt_int_range("Enter account number to view: ", 10000000,99999999)
    #if ad.account_exists(account_num):

    current = db.get_account_via_number(account_num)

    if not current:
        print("Account not found.")
        return

    withdraw = prompt_float("Enter withdraw amount: ")
    desc = input("Enter withdraw description: ")

    if current.debit(withdraw, desc) and db.update_account_balance(account_num, -withdraw):
        print("*Account withdrawn")
        print("New Balance: ", current.balance)
    else:
        print("Account balance too small, can't do negative values, or over spending limit.")

def modify_owner():
    print("* Modify Owner *")
    name = input("Enter name to search: ")
    owner = search_for_owner(name) # do a search
    while owner is None:
        name = input("Enter name to search(Q to quit): ")
        if name.lower() == "q":
            return # go back to the main to add owner to then back adding account
        owner = search_for_owner(name)
    print()
    choice = 0
    while choice != 7:
        print("* Owner Information")
        print(owner)
        print("\n1. Change first name")
        print("2. Change last name")
        print("3. Change street address")
        print("4. Change city")
        print("5. Change state")
        print("6. Change zipcode")
        print("7. Exit Owner Modification")
        choice = prompt_int_range("Modify: ", 1, 7)
        print()
        if choice == 1:
            new_name = input("Enter new first name: ")
            owner.first_name = new_name
        elif choice == 2:
            new_name = input("Enter new last name: ")
            owner.last_name = new_name
        elif choice == 3:
            new_address = input("Enter new street address: ")
            owner.street_address = new_address
        elif choice == 4:
            new_city = input("Enter new city: ")
            owner.city = new_city
        elif choice == 5:
            new_state = input("Enter new state: ")
            owner.state = new_state
        elif choice == 6:
            new_zip = input("Enter new zip code: ")
            owner.zipcode = new_zip
        elif choice == 7:
            db.update_owner(owner)  # actually update on the database
        print()


def modify_account():
    print("* Modify Account *")

    account_num = prompt_int_range("Enter account number to view: ", 10000000, 99999999)
    # if account found print out information
    #current = ad.search_account(account_num)
    current = db.get_account_via_number(account_num)

    if not current:
        print("No account found.")
        return
    choice = 0
    while choice != 4:
        print(current)
        print("\n1. Add Owner")
        print("2. Remove Owner")
        print("3. Delete Transactions")
        print("4. Close Account")
        print("5. Exit Modify Account")
        choice = prompt_int_range("Modify: ", 1, 5)

        if choice == 1:
            add_owner_to_account(current)
        elif choice == 2:
            remove_owner_from_account(current)
        elif choice == 3:
            delete_transaction(current)
        elif choice == 4:
            if db.update_account_active(current.account_num, False):
                print("* Account closed")
            else:
                print("* Error closing account.")


def add_owner_to_account(current):
    print("* Add owner")
    name = input("Enter name to search: ")
    owner = search_for_owner(name)  # do a search
    while owner is None:
        name = input("Enter name to search(Q to quit): ")
        if name.lower() == "q":
            return  # go back to the main to add owner to then back adding account
        owner = search_for_owner(name)
    print()

    if current.add_owner(owner) and db.modify_account_add_owner(current.account_num, owner.id):
        print("* Owner added to account")
    else:
        print("* Error, owner already on account.")

def remove_owner_from_account(current):
    print("* Remove owner")
    # list out owners?
    counter = 0 # print list of owners to remove
    for o in current.owners:
        counter += 1
        print(f"{counter}. {o}")

    # have them choose which one to delete
    delete_index = prompt_int_range("Select owner to remove: ", 1, counter)

    # remove from account and from db
    del_owner = current.remove_owner(delete_index-1) # off by one for deleting

    if del_owner is not None and db.delete_owner_from_account(current.account_num, del_owner.id):
        print("* Owner removed from account")
    else:
        print("* Error, owner not on account.")

def delete_transaction(current):
    print("* Delete transaction")
    # loop through print transactions
    transaction_list = db.get_transactions_on_account(current.account_num)

    if len(transaction_list) > 0:
        count = 0
        for t in transaction_list:
            count += 1
            print(f"{count}. {t}")

        # input for transaction to delete
        delete_index = prompt_int_range("Select transaction to delete: ", 1, count)

        # perform the delete
        if db.delete_transaction_by_id(transaction_list[delete_index-1].id):
            print("* Transaction deleted")
        else:
            print("* Error, transaction not deleted.")
    else:
        print("* No transactions on account.")

def filter_accounts():
    print("* Filter Accounts *")
    for index, account_type in enumerate(AccountType, start=1): # print off my options of the enum
        print(f"{index}. {account_type.value}")

    choice = prompt_int_range("Choose Account Type: ", 1, len(AccountType))

    choice_enum = list(AccountType)[choice-1]

    # accounts = ad.filter_accounts(choice_enum)
    accounts = db.get_accounts_via_type(choice_enum)
    for account in accounts:
        print(account)

def monthly_fee_to_accounts():
    print("* Apply Monthly Fee *")

    account_nums = db.get_account_number_list()

    for an in account_nums:
        account = db.get_account_via_number(an)
        account.apply_monthly_fee()

def reactivate_account():
    print("* Reactivate Account *")

    account_num = prompt_int_range("Enter account number to view: ", 10000000, 99999999)

    current = db.get_closed_account_via_number(account_num)

    if not current:
        print("No account found.")
        return

    print(current)
    if db.update_account_active(current.account_num, True):
        print("* Account re-activated")
    else:
        print("* Error re-activating account.")

def main():
    #read_in_owners("owners.csv")
    #read_in_accounts("accounts.json")
    #read_in_transactions("All_Transactions.xml")
    #ad.load_test_data() # loads test data until module 7-8

    MENU_EXIT = 11

    choice = 0
    while choice != MENU_EXIT:
        print("** Banking System **")
        print("1. Add Account")
        print("2. View Account")
        print("3. Modify Account")
        print("4. Filter Accounts")
        print("5. Deposit Money")
        print("6. Withdraw Money")
        print("7. Apply Monthly Fee")
        print("8. Add Owner")
        print("9. Modify Owner")
        print("10. Re-open Account")
        print(str(MENU_EXIT) + ". Exit")

        choice = prompt_int_range("Operation: ", 1, MENU_EXIT)

        print() # spacing
        if choice == 1:
            add_account()
        elif choice == 2:
            view_account()
        elif choice == 3:
            modify_account()
        elif choice == 4:
            filter_accounts()
        elif choice == 5:
            deposit_money()
        elif choice == 6:
            withdraw_money()
        elif choice == 7:
            monthly_fee_to_accounts()
        elif choice == 8:
            add_owner()
        elif choice == 9:
            modify_owner()
        elif choice == 10:
            reactivate_account()
        else: # exit option
            #write_out_owners()
            #write_out_transactions()
            #write_out_accounts()
            print("System exiting...")
        print() # space out the UI


# helper functions
def prompt_int(prompt) -> int:
    while True:
        str_value = input(prompt)
        value = get_int(str_value)
        if value is not None:
            return value
        print("Error, invalid input.")

def prompt_int_range(prompt, low, high) -> int:
    while True:
        str_value = input(prompt)
        value = get_int_range(str_value, low, high)
        if value is not None:
            return value
        print("Error, invalid input, out of range.")

def prompt_float(prompt) -> float:
    while True:
        str_value = input(prompt)
        value = get_float(str_value)
        if value is not None:
            return value
        print("Error, invalid input.")


if __name__ == "__main__":
    main()
