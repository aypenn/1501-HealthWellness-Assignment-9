import threading
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

import services.health_data as health_data
from models.DayEntity import *
from services import health_database
from utils.input_utils import *

def read_xml_file():
    xml_file = str(Path(__file__).parent) + "\\Meals_Workouts.xml"

    # print("xml_file = ", xml_file)

    # tree = ET.parse(r"C:\Data Files\Source\Repos\MCC\INFO 1501\Assignment 7\HealthWellness\services\Meals_Workouts.xml")
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # import meal data

    threads_meals = []
    threads_workouts = []

    for meal in root.findall("meal"):

        wk_date_str = meal.get("date")
        wk_date:date = datetime.strptime(wk_date_str, "%m/%d/%Y")

        desc = meal.find("description").text
        calories = meal.find("calories").text
        meal_type = meal.find("meal_type").text

        t = threading.Thread(target=health_database.add_meal, args=(wk_date, Meal(desc, meal_type, int(calories))))
        threads_meals.append(t)
        t.start()

    for t in threads_meals:
        t.join()


    for workout in root.findall("workout"):

        wk_date_str = workout.get("date")
        wk_date:date = datetime.strptime(wk_date_str, "%m/%d/%Y")

        desc = workout.find("description").text
        calories = workout.find("calories").text
        workout_type = workout.find("workout_type").text

        t = threading.Thread(target=health_database.add_workout, args=(wk_date, Workout(desc, workout_type, int(calories))))
        threads_meals.append(t)
        t.start()

    for t in threads_workouts:
            t.join()

        # # add date entity if nat already added
        #
        # if health_data.get_day(wk_date) is not None:
        #     health_data.add_day(wk_date)


        # # add workout data to health_data
        # health_data.add_workout(date(wk_date.year, wk_date.month, wk_date.day), Workout(desc, workout_type, int(calories)))

        # result = health_database.add_workout(wk_date, Workout(desc, workout_type, int(calories)))
