import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

from models.Transaction import Transaction, TransactionType
from services.account_data import accounts, search_account
from datetime import datetime
import services.account_database as db

def read_in_transactions(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    for transaction in root.findall('transaction'):
        account_num = int(transaction.get('account_num'))

        t_type = TransactionType(transaction.find('type').text)
        str_date = transaction.find('date_time').text
        date_time = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f")
        description = transaction.find('description').text
        amount = float(transaction.find('mod_amount').text)

        new_transaction = Transaction(t_type, date_time, description, amount)

        #current_account = search_account(account_num)
        current_account = db.get_account_via_number(account_num)

        # print(new_transaction) # to test

        if current_account:
            current_account.add_transaction(new_transaction)



def write_out_transactions():
    root = ET.Element('all_transactions')

    for account in accounts.values():
        # get transactions and loop through those, create subelements for those

        for t in account.transactions:
            transaction = ET.SubElement(root, 'transaction')
            transaction.set("account_num", str(account.account_num))

            t_type = ET.SubElement(transaction, 'type')
            t_type.text = str(t.type)

            date_time = ET.SubElement(transaction, 'date_time')
            date_time.text = str(t.date_time)

            desc = ET.SubElement(transaction, 'description')
            desc.text = t.description

            amount = ET.SubElement(transaction, 'mod_amount')
            amount.text = str(t.mod_amount)

    # basic xml to string
    xml_data = ET.tostring(root)

    # turn it 'pretty'
    pretty_xml = parseString(xml_data).toprettyxml()
    #print(pretty_xml)
    #pretty_xml = "\n".join(line for line in pretty_xml.splitlines() if line.strip()) # get rid of extra new lines

    #write it out
    with open("All_Transactions.xml", "w") as file:
        file.write(pretty_xml)
