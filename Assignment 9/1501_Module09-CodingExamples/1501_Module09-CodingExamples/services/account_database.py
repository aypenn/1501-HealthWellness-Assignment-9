import sqlite3

#from models import Account
from models.AccountType import AccountType
from models.BankAccounts import CheckingAccount, SavingsAccount
from models.Owner import Owner
from models.Transaction import Transaction, TransactionType
from datetime import date, datetime

DATABASE_NAME = "BankAccountSystem.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    return conn

def add_checking_account(account : CheckingAccount) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # insert into account
        cursor.execute("INSERT INTO account VALUES(?, ?, ?)",
                       (account.account_num, account.balance, str(account.account_type)))
        # insert into checking
        cursor.execute("INSERT INTO checking_account VALUES (?, ?, ?, ?, ?)",
                       (account.account_num, account.monthly_fee, account.limit, account.no_fee_amount, account.apply_fee))

        add_owner_account(account.account_num, account.owners, conn)

        conn.commit()
        return True
    except Exception as ex:
        print(ex)
        conn.rollback()
        return False
    finally:
        conn.close()

def add_savings_account(account : SavingsAccount) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # insert into account
        cursor.execute("INSERT INTO account VALUES(?, ?, ?)",
                       (account.account_num, account.balance, str(account.account_type)))
        # insert into checking
        cursor.execute("INSERT INTO savings_account VALUES (?, ?, ?, ?)",
                       (account.account_num, account.minimum_balance, account.earned_interest, account.monthly_fee))

        add_owner_account(account.account_num, account.owners, conn)

        conn.commit()
        return True
    except Exception as ex:
        print(ex)
        conn.rollback()
        return False
    finally:
        conn.close()

def add_owner_account(acct_num : int, owners : list[Owner], conn : sqlite3.Connection):
    cursor = conn.cursor()
    for owner in owners:
        try:
            cursor.execute("INSERT INTO account_owners VALUES(?,?)", (acct_num, owner.id))
        except Exception as ex:
            print(ex)
            conn.rollback()

def modify_account_add_owner(acct_num : int, owner_id : str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO account_owners VALUES (?, ?)", (acct_num, owner_id))

        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()


def add_owner(owner : Owner) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # insert owner
        cursor.execute("INSERT INTO owner VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                       (owner.id, owner.first_name, owner.last_name, owner.address, owner.city,
                        owner.state, owner.zipcode, owner.date_of_birth))

        conn.commit()
        return True
    except Exception as ex:
        print(ex)
        conn.rollback()
        return False
    finally:
        conn.close()

def add_transaction(acct_num : int, transaction : Transaction) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO account_transaction (type, date_time, description, mod_amount, account_number) VALUES (?, ?, ?, ?, ?)",
            (str(transaction.type), transaction.date_time, transaction.description, transaction.mod_amount, acct_num))

        conn.commit()
        return True
    except Exception as ex:
        print(ex)
        conn.rollback()
        return False
    finally:
        conn.close()

def get_owners_via_name(name : str) -> list[Owner]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM owner WHERE first_name LIKE ? OR last_name LIKE ?", (f"%{name}%", f"%{name}%"))
    owners = cursor.fetchall()

    owner_list = []
    for o in owners:
        owner_list.append(Owner(o[0], o[1], o[2], o[3], o[4], o[5], o[6], parse_date(o[7])))  # date:

    return owner_list

def account_exists_via_id(o_id : int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT account_number FROM account WHERE account_number = ? AND is_active = 1", (o_id,))

    if cursor.fetchone() is None:
        return False

    return True

def get_owners_via_account_number(account_num : int) -> list[Owner]:
    conn = get_connection()
    cursor = conn.cursor()
    owner_list = []

    cursor.execute("SELECT owner_id FROM account_owners WHERE account_number = ?", (account_num,))

    owner_ids = cursor.fetchall()

    for o_id in owner_ids:
        owner_list.append(get_owner_via_id(o_id[0]))

    return owner_list

def get_owner_via_id(o_id : str) -> Owner | None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM owner WHERE owner_id = ?", (o_id,))
    o = cursor.fetchone()

    return Owner(o[0], o[1], o[2], o[3], o[4], o[5], o[6], parse_date(o[7]))  # date:


def get_account_via_number(account_num : int) -> CheckingAccount | SavingsAccount | None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM account WHERE account_number = ? AND is_active = 1", (account_num,))

    base_account = cursor.fetchone()
    # 0 - id, 1 - balance, 2 - type

    if base_account is None:
        return None

    owners = get_owners_via_account_number(base_account[0])

    if base_account[2] == "Checking":
        # query the checking account and get the data there
        cursor.execute("SELECT * FROM checking_account WHERE account_number = ?", (base_account[0],))
        checking = cursor.fetchone()

        # get the owners as a list

        return CheckingAccount(base_account[0], owners, float(base_account[1]), checking[2], checking[1],
                               checking[3], bool(checking[4]))
    elif base_account[2] == "Savings":
        # query the savings table and get data
        cursor.execute("SELECT * FROM savings_account WHERE account_number = ?", (base_account[0],))
        savings = cursor.fetchone()

        return SavingsAccount(base_account[0], owners, float(base_account[1]), savings[1], savings[3], savings[2])

def get_closed_account_via_number(account_num : int) -> CheckingAccount | SavingsAccount | None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM account WHERE account_number = ? AND is_active = 0", (account_num,))

    base_account = cursor.fetchone()
    # 0 - id, 1 - balance, 2 - type

    if base_account is None:
        return None

    owners = get_owners_via_account_number(base_account[0])

    if base_account[2] == "Checking":
        # query the checking account and get the data there
        cursor.execute("SELECT * FROM checking_account WHERE account_number = ?", (base_account[0],))
        checking = cursor.fetchone()

        # get the owners as a list

        return CheckingAccount(base_account[0], owners, float(base_account[1]), checking[2], checking[1],
                               checking[3], bool(checking[4]))
    elif base_account[2] == "Savings":
        # query the savings table and get data
        cursor.execute("SELECT * FROM savings_account WHERE account_number = ?", (base_account[0],))
        savings = cursor.fetchone()

        return SavingsAccount(base_account[0], owners, float(base_account[1]), savings[1], savings[3], savings[2])


def get_account_number_list() -> list[int]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT account_number FROM account WHERE is_active = 1")

    return [num[0] for num in cursor.fetchall()]

def get_accounts_via_type(acct_type : AccountType) -> list[CheckingAccount] | list[SavingsAccount]:
    conn = get_connection()
    cursor = conn.cursor()

    account_list = []

    cursor.execute("SELECT * FROM account WHERE type = ? AND is_active = 1", (str(acct_type),))
    base_accounts = cursor.fetchall()

    for acct in base_accounts:
        if acct_type == AccountType.CHECKING:
            cursor.execute("SELECT * FROM checking_account WHERE account_number = ?", (acct[0],))
            checking = cursor.fetchone()
            owners = get_owners_via_account_number(acct[0])
            checking_account = CheckingAccount(acct[0], owners, float(acct[1]), checking[2], checking[1], checking[3], bool(checking[4]))
            account_list.append(checking_account)
        else:
            cursor.execute("SELECT * FROM savings_account WHERE account_number = ?", (acct[0],))
            savings = cursor.fetchone()
            owners = get_owners_via_account_number(acct[0])
            savings_account = SavingsAccount(acct[0], owners, float(acct[1]), savings[1], savings[3], savings[2])
            account_list.append(savings_account)

    return account_list

def owner_exists(owner_id : str, first_name : str, last_name : str, dob : date) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT owner_id FROM owner WHERE owner_id = ? AND first_name = ? AND last_name = ? AND DOB = ?",
                   (owner_id, first_name, last_name, dob))

    if cursor.fetchone() is None:
        return False

    return True

def get_transactions_on_account(account_num : int) -> list[Transaction]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM account_transaction WHERE account_number=? ORDER BY date_time", (account_num,))

    transactions = cursor.fetchall()

    transaction_list = []

    for t in transactions:
        transaction_list.append(Transaction(t[0], TransactionType(t[1]), parse_date_time(t[2]), t[3], float(t[4])))

    return transaction_list

def get_transactions_on_account_via_year(account_num : int, year : int) -> list[Transaction]:
    conn = get_connection()
    cursor = conn.cursor()

    start_date = str(year) + "-01-01"
    end_date = str(year) + "-12-31"

    cursor.execute("SELECT * FROM account_transaction WHERE account_number=? AND (date_time >= ? AND date_time <=?) ORDER BY date_time",
                   (account_num, start_date, end_date))

    transactions = cursor.fetchall()

    transaction_list = []

    for t in transactions:
        transaction_list.append(Transaction(t[0], TransactionType(t[1]), parse_date_time(t[2]), t[3], float(t[4])))

    return transaction_list


def get_transactions_on_account_via_month(account_num : int, year : int, month : int) -> list[Transaction]:
    conn = get_connection()
    cursor = conn.cursor()

    start_date = f"{year}-{month:02}-01"
    if month >= 12:
        month = 0
        year += 1
    end_date = f"{year}-{month+1:02}-01"

    cursor.execute("SELECT * FROM account_transaction WHERE account_number=? AND (date_time >= ? AND date_time < ?) ORDER BY date_time",
                   (account_num, start_date, end_date))

    transactions = cursor.fetchall()

    transaction_list = []

    for t in transactions:
        transaction_list.append(Transaction(t[0], TransactionType(t[1]), parse_date_time(t[2]), t[3], float(t[4])))

    return transaction_list

def get_transactions_on_account_via_range(account_num : int, start_date : str, end_date : str) -> list[Transaction]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM account_transaction WHERE account_number=? AND (date_time >= ? AND date_time < ?) ORDER BY date_time",
                   (account_num, start_date, end_date))

    transactions = cursor.fetchall()

    transaction_list = []

    for t in transactions:
        transaction_list.append(Transaction(t[0], TransactionType(t[1]), parse_date_time(t[2]), t[3], float(t[4])))

    return transaction_list

def update_owner(owner : Owner) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""UPDATE owner SET first_name = ?, last_name = ?, street_address = ?, city = ?, state = ?, 
                       zipcode = ? WHERE owner_id = ?""",
                       (owner.first_name, owner.last_name, owner.street_address, owner.city,
                                                                            owner.state, owner.zipcode, owner.id))
        conn.commit()
        return cursor.rowcount == 1
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()

def update_account_balance(account_num : int, amount : float) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE account SET balance = balance + ? WHERE account_number = ? AND is_active = 1",
                                                                            (amount, account_num))

        conn.commit()
        return cursor.rowcount == 1
    except Exception as ex:
        conn.rollback()
        print(ex)
        return False
    finally:
        conn.close()

def update_checking_apply_fee(account_num : int, apply_fee : bool) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE account SET apply_fee = ? WHERE account_number = ? AND is_active = 1",(int(apply_fee), account_num))
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()

def update_account_active(account_num : int, active : bool) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE account SET is_active = ? WHERE account_number = ?", (int(active), account_num))
        conn.commit()
        return cursor.rowcount == 1
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_transaction_by_id(transaction_id : int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM account_transaction WHERE id = ?", (transaction_id,))
        conn.commit()
        return cursor.rowcount == 1
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_owner_from_account(account_num : int, owner_id : str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM account_owners WHERE account_number = ? AND owner_id = ?", (account_num, owner_id,))
        conn.commit()
        return cursor.rowcount == 1
    except Exception as ex:
        print(ex)
        conn.rollback()
        return False
    finally:
        conn.close()

def parse_date_time(date_time_text : str) -> datetime:
    return datetime.strptime(date_time_text, '%Y-%m-%d %H:%M:%S.%f')

def parse_date(date_text : str) -> date:
    return datetime.strptime(date_text, '%Y-%m-%d').date()