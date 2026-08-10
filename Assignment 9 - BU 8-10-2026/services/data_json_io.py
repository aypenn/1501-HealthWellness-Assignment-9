import json
import threading
from pathlib import Path
import services.health_data as health_data
from models.DayEntity import *
from utils.input_utils import *

def read_json_file():

    print("\n### Reading JSON File ###")

    # get application root

    folder_path = Path(__file__).parent.resolve()

    threads_meals = []
    threads_workouts = []

    # read in JSON file

    with open(str(folder_path) + "\\health_data.json", "r") as file:

        # get raw data

        data = json.load(file)

        # process raw dats

        for item in data:

            # get date

            wk_date_str = item.get("date")
            wk_date = date.strptime(wk_date_str, "%m/%d/%Y")

            # if health_data.get_day(wk_date) is not None:
            # health_data.add_day(wk_date)

            # get meals

            for m in item.get("meals"):

                desc = m.get("description")
                calories = m.get("calories")
                meal_type = m.get("meal_type")

                # health_data.add_meal(wk_date, Meal(desc, meal_type, int(calories)))

                t = threading.Thread(target=health_database.add_meal, args=(wk_date, Meal(desc, meal_type, int(calories))))
                threads_meals.append(t)
                t.start()

            for t in threads_meals:
                t.join()

            # get workouts

            for w in item.get("workouts"):

                desc = w.get("description")
                calories = w.get("calories")
                workout_type = w.get("workout_type")

                # health_data.add_workout(wk_date, Workout(desc, workout_type, int(calories)))

                t = threading.Thread(target=health_database.add_workout, args=(wk_date, Workout(desc, workout_type, int(calories))))
                threads_meals.append(t)
                t.start()

            for t in threads_workouts:
                t.join()

def write_out_json():


    # write health_data to JSON file

    print("\n### Creating JSON File ###")

    # get root directory

    folder_path = str(Path(__file__).parent.resolve().parent) + "\\outputfiles"

    output_file = str(folder_path) + "\\health_data_out.json"

    # get start and stop dates

    min_date: date = health_database.meals_min_date()

    max_date: date = health_database.meals_max_date()

    workouts_min_date: date = health_database.workouts_min_date()

    workouts_max_date: date = health_database.workouts_max_date()

    if min_date > workouts_min_date:
        min_date = workouts_min_date

    if max_date < workouts_max_date:
        max_date = workouts_max_date
    


    # insert data

    json_data = []

    for d in daterange(min_date, max_date + timedelta(days=1)):

        # get element

        wk_date: date = d.strftime("%m/%d/%Y")

        element: DayEntity | None = health_data.get_day(d)

        if element is not None:

            # insert date

            wk_dict = {"date": wk_date}

            # insert meals

            vm = element.meals_to_dict()
            wk_dict["meals"] = vm

            # insert workouts

            vw = element.workouts_to_dict()
            wk_dict["workouts"] = vw

            # append data

            json_data.append(wk_dict)

    # create file

    with open(output_file, "w") as file:
        json.dump(json_data, file, indent=4)




