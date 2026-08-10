import csv

from services import health_database
from services.health_database import workouts_min_date
from utils.input_utils import *
from pathlib import Path
from datetime import date, timedelta, datetime
import services.health_data as health_data

def write_out_report(output_file: str = "", start_date: date = None, end_date: date = None):

    # set start and stop dates

    min_date:date = date.today()
    max_date:date = date.today()

    if start_date is not None:
        min_date = start_date
    else:
        min_date = health_database.meals_min_date()
        workouts_min_date: date = health_database.workouts_min_date()
        if workouts_min_date <  min_date:
            min_date = workouts_min_date

    if end_date is not None:
        max_date = end_date + timedelta(days=1)
    else:
        max_date = health_database.meals_max_date()  + timedelta(days=1)
        workouts_max_date: date = health_database.workouts_max_date()
        if workouts_max_date > max_date:
            max_date = workouts_max_date  + timedelta(days=1)


    # create output path and file

    output_file_path = str(Path(__file__).parent.resolve().parent) + "\\outputfiles"

    if output_file != "":
        output_file_path = output_file_path + "\\" + output_file
    else:
        output_file_path = output_file_path + "\\health_data_out.csv"

    # field name headers

    fieldnames = ["Date", "Meal Calories", "Workout Calories", "Net Calories"]

    #  process data

    with open(output_file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

         # get data from database

        for d in daterange(min_date, max_date):
            calories = health_database.get_day(d)
            if calories is not None:

                mc: int = calories[0]
                if mc is None:
                    mc = 0

                wc: int = calories[1]
                if wc is None:
                    wc = 0

                if mc != 0 or wc != 0:
                    netc: int = mc - wc
                    data = {"Date" : d.strftime("%m/%d/%y"), "Meal Calories": str(mc), "Workout Calories": str(wc), "Net Calories": str(mc - wc)}
                    writer.writerow(data)


