import csv
from services.account_data import *
from models.Owner import Owner
from utils.input_utils import get_valid_date
import services.account_database as db

def write_out_owners():
    # get list of dictionary of owners
    #owners_dict = []
    #for owner in owners:
    #    owners_dict.append(owner.to_dict())

    owners_dict = [owner.to_dict() for owner in owners]

    # open file
    with open("owners.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=owners_dict[0].keys())
        writer.writeheader() # headers

        # loop through and write out dictionary info
        for owner in owners_dict:
            writer.writerow(owner)

def read_in_owners(filename):
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader: # loop through and create an owner
            new_owner = Owner(row['id'], row['first_name'], row['last_name'], row['street_address'],
                              row['city'], row['state'], row['zipcode'], get_valid_date(row['dob'])) # use our valid date getter we already have
            #add_owner(new_owner) # add new owner on the account_data file
            db.add_owner(new_owner)