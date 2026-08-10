import os
import sqlite3
from services.data_csv_io import read_in_owners
from services.data_xml_io import read_in_transactions
from services.data_json_io import read_in_accounts

DATABASE_NAME = "../BankAccountSystem.db"

CREATE_ACCOUNT = """CREATE TABLE IF NOT EXISTS account (
	account_number INTEGER NOT NULL PRIMARY KEY UNIQUE,
	balance REAL NOT NULL,
	type TEXT NOT NULL
);"""

CREATE_CHECKING = """CREATE TABLE IF NOT EXISTS checking_account (
	account_number INTEGER NOT NULL PRIMARY KEY UNIQUE,
	monthly_fee REAL NOT NULL,
	spending_limit REAL NOT NULL,
	no_fee_amount REAL NOT NULL,
	apply_fee INTEGER NOT NULL,
	FOREIGN KEY (account_number) REFERENCES account(account_number)
);"""

CREATE_SAVINGS = """CREATE TABLE IF NOT EXISTS savings_account (
	account_number INTEGER NOT NULL PRIMARY KEY UNIQUE,
	minimum_balance REAL NOT NULL,
	earned_interest REAL NOT NULL,
	monthly_fee REAL NOT NULL,
	FOREIGN KEY (account_number) REFERENCES account(account_number)
);"""

CREATE_TRANSACTIONS = """CREATE TABLE IF NOT EXISTS account_transaction (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	type TEXT NOT NULL,
	date_time TEXT NOT NULL,
	description TEXT NOT NULL,
	mod_amount REAL NOT NULL,
	account_number INTEGER NOT NULL,
	FOREIGN KEY (account_number) REFERENCES account(account_number)
);"""

CREATE_OWNER = """CREATE TABLE IF NOT EXISTS owner (
	owner_id TEXT NOT NULL PRIMARY KEY UNIQUE,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	street_address TEXT NOT NULL,
	city TEXT NOT NULL,
	state TEXT NOT NULL,
	zipcode TEXT NOT NULL,
	DOB TEXT NOT NULL
);"""

CREATE_ACCOUNT_OWNER_BRIDGE = """CREATE TABLE IF NOT EXISTS account_owners (
	account_number INTEGER NOT NULL,
	owner_id TEXT NOT NULL,
	PRIMARY KEY (account_number, owner_id),
	FOREIGN KEY (account_number) REFERENCES account(account_number),
	FOREIGN KEY (owner_id) REFERENCES owner(owner_id)
);"""

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_table(table_sql : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(table_sql) # run the table command

    conn.commit()
    conn.close()

def drop_table(table_name : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

    conn.commit()
    conn.close()

def read_owners():
    print("** Read in Owners from CSV **")

    filename = "../" + input("Enter CSV file to load: ")

    if os.path.exists(filename):
        read_in_owners(filename) #just get the file name at the root of the project with ../
        print("Owners added in.")
    else:
        print("Error, file not found, no owners loaded.")

def read_accounts():
    print("** Read in Accounts from JSON **")

    filename = "../" + input("Enter JSON file to load: ")

    if os.path.exists(filename):
        read_in_accounts(filename) #just get the file name at the root of the project with ../
        print("Accounts added in.")
    else:
        print("Error, file not found, no accounts loaded.")

def read_transactions():
    print("** Read in Transactions from XML **")

    filename = "../" + input("Enter XML file to load: ")

    if os.path.exists(filename):
        read_in_transactions(filename) #just get the file name at the root of the project with ../
        print("Transactions added in.")
    else:
        print("Error, file not found, no transactions loaded.")

def main():
    choice = 0
    while choice != 11:
        print("*** Database Utility ***")
        print("1. Add Account Table")
        print("2. Add Checking Table")
        print("3. Add Savings Table")
        print("4. Add Transaction Table")
        print("5. Add Owner Table")
        print("6. Add Account Owner Bridge Table")
        print("7. Drop a Table")
        print("8. Insert Account Data from JSON")
        print("9. Insert Owner Data from CSV")
        print("10. Insert Transaction Data from XML")
        print("11. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            create_table(CREATE_ACCOUNT)
        elif choice == 2:
            create_table(CREATE_CHECKING)
        elif choice == 3:
            create_table(CREATE_SAVINGS)
        elif choice == 4:
            create_table(CREATE_TRANSACTIONS)
        elif choice == 5:
            create_table(CREATE_OWNER)
        elif choice == 6:
            create_table(CREATE_ACCOUNT_OWNER_BRIDGE)
        elif choice == 7:
            table = input("Enter table name to drop: ")
            drop_table(table)
        elif choice == 8:
            read_accounts()
        elif choice == 9:
            read_owners()
        elif choice == 10:
            read_transactions()
        elif choice == 11:
            print("Exiting...")
        else:
            print("Invalid operation...")

if __name__ == "__main__":
    main()












