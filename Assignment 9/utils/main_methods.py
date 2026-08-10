#moved some methods from the main program in here to make the main file easier to read and work with
import pathvalidate

# import pathvalidate

from models.DayEntity import *
from datetime import date
from models.CalorieEntity import *
from models.HealthEntry import *

from services import health_database
from services.data_csv_report import write_out_report
from utils.input_utils import *

import services.health_data as health_data

def gen_selection_list(list_elements, header1, header2 = ""):

    print("\n### " + header1 + " : ###\n")

    if header2 != "":
        print(header2 + "\n")

    choice_number = 1

    for element in list_elements:
        print(str(choice_number) + ". " + str(element))
        choice_number += 1

def get_date(input_message):

    got_value = False

    # get current date

    while not got_value:

        wk_date = get_valid_date(input(input_message))

        if wk_date is None:
            print("\n### Error - Date cannot be blank and must be in ""MM/DD/YYYY"" format ###")
        elif wk_date > date.today():
            print("\n### Error - Date cannot be a date in the future ###")
        else:
            got_value = True
            return wk_date

def add_meal():

    # get meal date

    meal_date = get_date("\nEnter meal date: ")

    #get meal item

    choice = 0
    meal_list = list(MealType)
    total_choices = len(meal_list) + 1

    while choice != total_choices:

        num_choices = 1
        meal_type = ""
        meal_description = ""
        calories: int = 0
        choice = 0
        print("### Choose meal: ###")

        for m in meal_list:
            print(str(num_choices) + ". " + str(m))
            num_choices += 1

        print(str(num_choices) + ". Exit")

        choice = get_int_range(input("Choose meal number: "), 1, total_choices)

        if choice is None:
            print("\n### Error - meal item entered must be between 1 and " + str(total_choices) + " ###")
        elif 1 <= choice <= (total_choices - 1):
            meal_type = str(meal_list[choice - 1])

            # print("meal_item = " + meal_item)

            while meal_description == "":
                meal_description =  input("Enter meal description: ").strip()

                if meal_description == "":
                    print("Entered meal description cannot be blank")

            got_value = False

            while not got_value:

                calories = get_int(input("Enter calories: "))

                if calories is not None and calories > 0:
                    got_value = True
                else:
                    print("\n### Error - calories entered must be greater than 0 and must be an integer ###")

            # add to db

            v = Meal(meal_description, meal_type, calories, 0)
            v.add_meal(meal_date)

            print("### Meal entry added\n")

        elif choice == total_choices:
            print("\nSystem Exiting...")
        else:
            print("\n### Error - meal item entered must be between 1 and 5 ###")


def add_workout():

    # get work out date

    workout_date = get_date("\nEnter workout date: ")

    #get work out detail and calories

    choice = 0
    workout_list = list(WorkoutType)
    total_choices = len(workout_list) + 1

    while choice != total_choices:

        num_choices = 1
        workout_type = ""
        workout_description = ""
        calories: int = 0
        choice = 0

        print("### Choose workout: ###")

        for w in workout_list:
            print(str(num_choices) + ". " + str(w))
            num_choices += 1

        print(str(num_choices) + ". Exit")

        choice = get_int_range(input("\nEnter workout number: "),  1, total_choices)

        if choice is None:
            print("\n### Error - workout number entered must be between 1 and " + str(total_choices) + " ###")
        elif 1 <= choice <= (total_choices - 1):

            workout_type = str(workout_list[choice - 1])

            while workout_description == "":
                workout_description = input("Enter workout description: ").strip()

                if workout_description == "":
                    print("Entered workout description cannot be blank")

            got_value = False

            while not got_value:

                calories = get_int(input("Enter calories: "))

                if calories is None or calories < 0:
                    print("\n### Error - calories entered must be greater than 0 and must be an integer ###")
                else:
                    got_value = True

            #add to db

            v: Workout = Workout(workout_description, workout_type, calories, 0)
            v.add_workout(workout_date)

            print("### Workout entry added\n")

def filter_by_date_range(start_date: date, stop_date: date):

    # select entries by date range
    v = ""

    net_calories = 0

    # check each date in range

    for d in daterange(start_date, stop_date):

        # element: DayEntity | None = health_database.get_day(d)

        element: DayEntity | None = DayEntity.get_day(d)

        if element is not None:

            if v != "":
                v += "\n"
            v += element.__str__()

            # keep running total of net calories

            net_calories += element.net_calories()

    #  if entries made, add net calories for range

    if v != "" and (stop_date - start_date).days > 1:

        v += "\nNet calories for range: " + str(net_calories)

    return v


def search_date():

    # get search date

    search_day = get_date("\nEnter search date: ")

    # v: DayEntity | None = DayEntity.get_day(search_day)

    v = filter_by_date_range(search_day, search_day + timedelta(days=1))

    if v != "":

        print(v)

    else:

        print("\nNo entries for this search date\n")

def update_element(element_type: str, element: object):

    if element_type == "Meal":
        # health_database.update_meal(element)
        print("in if - element = " + str(element))
        element.update_meal()
    else:
        health_database.update_workout(element)


def update_calorie_element(element_type):

    # get entity date and dayentity

    entry_date = get_date("\nEnter " + element_type + " Date: ")

    element_list = []
    element_type_list = []

    if element_type == "Meal":

        element_list = health_database.get_meals(entry_date)
        element_type_list = list(MealType)

    else:

        element_list = health_database.get_workouts(entry_date)
        element_type_list = list(WorkoutType)

    cal_choice: int | None = None

     # check for null

    if len(element_list) == 0:
        print("\nNo " + element_type + " Entered for ", entry_date.strftime("%m/%d/%Y"), "\n")

    else:

        #  select type of update

        mod_selection = ["Modify Item Description", "Modify Calories", "Modify " + element_type + " Type",
                         "Exit Current " + element_type + " Modification"]

        # element_list = []
        # element_type_list = []
        #
        # if element_type == "Meal":
        #
        #     element_list = health_database.get_meals(entry_date)
        #     element_type_list = list(MealType)
        #
        # else:
        #
        #     element_list = health_database.get_workouts(entry_date)
        #     element_type_list = list(WorkoutType)

        mod_done = False

        while not mod_done:

            max_cal_item_choice_number = len(element_list) + 1

            # print ("max_mod_item_choice_number = " +str(max_mod_item_choice_number))

            gen_selection_list(element_list, "Choose " + element_type + " to Update")
            print(str(max_cal_item_choice_number) + ". Exit")

            element_choice = get_int_range(input("\nEnter Number to Update: "), 1,  max_cal_item_choice_number)

            #process choice

            # bad selection

            if element_choice is None or element_choice >  max_cal_item_choice_number or element_choice < 1:

                print("\n### Error - Number Entered Must be Between 1 And " + str(max_cal_item_choice_number) + " ###")

            elif 1 <= element_choice <  max_cal_item_choice_number:

                update_done = False

                while not update_done:

                    if element_type == "Meal":
                        wk_element: Meal = element_list[element_choice - 1]
                    else:
                        wk_element: Workout = element_list[element_choice - 1]

                    # wk_element: HealthEntry = element_list[element_choice - 1]

                    max_mod_item_choice_number = len(mod_selection)

                    gen_selection_list(mod_selection, "Choose Modification", str(wk_element))

                    mod_choice = get_int_range(input("\nEnter Modification Choice: "), 1, max_mod_item_choice_number)

                    if mod_choice is None or mod_choice > max_mod_item_choice_number or mod_choice < 1:

                        print("\n### Error - Modify Number Entered Must be Between 1 and " + str(max_mod_item_choice_number) + " ###")

                    elif mod_choice == 1:

                        # process Modify Item Description

                        element_description = ""

                        while element_description == "":

                            element_description = input("\nEnter " + element_type + " Description: ")

                            if element_description == "":
                                print("Entered meal description cannot be blank")
                            else:
                                # wk_element.description_set(element_description)
                                wk_element.update_meal_description(element_description)
                                print("wk_element = ", str(wk_element))
                                # update_element(element_type, wk_element)


                        # update_element(element_type, wk_element)

                    elif mod_choice == 2:

                        # process Modify Calories

                        calories: int | None = None

                        while calories is None:

                            calories = get_int(input("\nEnter calories: "))
                            if calories is None:
                                print("\nEntered calories must be an integer")
                            else:
                                wk_element.calories_set(calories)
                                # update_element(element_type, wk_element)

                        update_element(element_type, wk_element)

                    elif mod_choice == 3:

                        # process type

                        element_type_done = False

                        while not  element_type_done:

                            max_type_choices = len(element_type_list) + 1

                            gen_selection_list(element_type_list, "Choose " + element_type + " Type")
                            print(str(max_type_choices ) + ". Exit\n")

                            type_choice = get_int_range(input("Choose " + element_type + " Type: "), 1, max_type_choices)

                            # print("type_choice = " + type_choice)

                            if type_choice is None:

                                print("Entered " + element_type + " Type Cannot be Blank")

                            elif type_choice < 1 or type_choice > max_type_choices:

                                print(element_type + " Type Must be Between 1 And " + str(max_type_choices))

                            elif type_choice < max_type_choices:
                                element_type_choice = element_type_list[type_choice - 1]
                                wk_element.entry_type_set(str(element_type_choice))
                                element_type_done = True

                            else:
                                element_type_done = True
                                update_done = True

                        update_element(element_type, wk_element)

                    else:

                        # exit
                        update_done = True


            else:
                mod_done = True


def update_meal():

    # get entity date and dayentity

    entry_date = get_date("\nEnter Meal Date: ")

    element_list = health_database.get_meals(entry_date)
    element_type_list = list(MealType)


     # check for null

    if len(element_list) == 0:

        print("\nNo Meal Entered for ", entry_date.strftime("%m/%d/%Y"), "\n")

    else:

        #  select type of update

        mod_selection = ["Modify Item Description", "Modify Calories", "Modify Meal Type",
                         "Exit Current Meal Modification"]

        mod_done = False

        while not mod_done:

            max_cal_item_choice_number = len(element_list) + 1

            # print ("max_mod_item_choice_number = " +str(max_mod_item_choice_number))

            gen_selection_list(element_list, "Choose Meal to Update")
            print(str(max_cal_item_choice_number) + ". Exit")

            element_choice = get_int_range(input("\nEnter Number to Update: "), 1,  max_cal_item_choice_number)

            #process choice

            # bad selection

            if element_choice is None or element_choice >  max_cal_item_choice_number or element_choice < 1:

                print("\n### Error - Number Entered Must be Between 1 And " + str(max_cal_item_choice_number) + " ###")

            elif 1 <= element_choice <  max_cal_item_choice_number:

                update_done = False

                while not update_done:

                    wk_element = list(element_list[element_choice - 1])

                    max_mod_item_choice_number = len(mod_selection)

                    gen_selection_list(mod_selection, "Choose Modification", str(wk_element))

                    mod_choice = get_int_range(input("\nEnter Modification Choice: "), 1, max_mod_item_choice_number)

                    if mod_choice is None or mod_choice > max_mod_item_choice_number or mod_choice < 1:

                        print("\n### Error - Modify Number Entered Must be Between 1 and " + str(max_mod_item_choice_number) + " ###")

                    elif mod_choice == 1:

                        # process Modify Item Description

                        element_description = ""

                        while element_description == "":

                            element_description = input("\nEnter Meal Description: ")

                            if element_description == "":
                                print("Entered meal description cannot be blank")
                            else:
                                wk_element[0] = element_description
                                element_list[element_choice - 1] = wk_element
                                health_database.update_meal(wk_element[3], wk_element[0], wk_element[2], wk_element[1])

                    elif mod_choice == 2:

                        # process Modify Calories

                        calories: int | None = None

                        while calories is None:

                            calories = get_int(input("\nEnter calories: "))
                            if calories is None:
                                print("\nEntered calories must be an integer")
                            else:
                                wk_element[2] = calories
                                element_list[element_choice - 1] = wk_element
                                health_database.update_meal(wk_element[3], wk_element[0], wk_element[2], wk_element[1])

                        # update_element(element_type, wk_element)

                    elif mod_choice == 3:

                        # process type

                        element_type_done = False

                        while not  element_type_done:

                            max_type_choices = len(element_type_list) + 1

                            gen_selection_list(element_type_list, "Choose Meal Type")
                            print(str(max_type_choices ) + ". Exit\n")

                            type_choice = get_int_range(input("Choose Meal Type: "), 1, max_type_choices)

                            # print("type_choice = " + type_choice)

                            if type_choice is None:

                                print("Entered Meal Type Cannot be Blank")

                            elif type_choice < 1 or type_choice > max_type_choices:

                                print("Meal Type Must be Between 1 And " + str(max_type_choices))

                            elif type_choice < max_type_choices:
                                element_type_choice = element_type_list[type_choice - 1]
                                wk_element[1] = element_type_choice
                                element_list[element_choice - 1] = wk_element
                                health_database.update_meal(wk_element[3], wk_element[0], wk_element[2], wk_element[1])
                                element_type_done = True

                            else:
                                element_type_done = True
                                update_done = True

                        # health_database.update_meal(wk_element[3], wk_element[0], wk_element[2], wk_element[1])

                    else:

                        # exit
                        update_done = True


            else:
                mod_done = True

def update_workout():

    # get entity date and dayentity

    entry_date = get_date("\nEnter workout Date: ")

    element_list = health_database.get_workouts(entry_date)
    element_type_list = list(WorkoutType)


     # check for null

    if len(element_list) == 0:

        print("\nNo Workout Entered for ", entry_date.strftime("%m/%d/%Y"), "\n")

    else:

        #  select type of update

        mod_selection = ["Modify Item Description", "Modify Calories", "Modify Workout Type",
                         "Exit Current Workout Modification"]

        mod_done = False

        while not mod_done:

            max_cal_item_choice_number = len(element_list) + 1

            # print ("max_mod_item_choice_number = " +str(max_mod_item_choice_number))

            gen_selection_list(element_list, "Choose Workout to Update")
            print(str(max_cal_item_choice_number) + ". Exit")

            element_choice = get_int_range(input("\nEnter Number to Update: "), 1,  max_cal_item_choice_number)

            #process choice

            # bad selection

            if element_choice is None or element_choice >  max_cal_item_choice_number or element_choice < 1:

                print("\n### Error - Number Entered Must be Between 1 And " + str(max_cal_item_choice_number) + " ###")

            elif 1 <= element_choice <  max_cal_item_choice_number:

                update_done = False

                while not update_done:

                    wk_element = list(element_list[element_choice - 1])

                    max_mod_item_choice_number = len(mod_selection)

                    gen_selection_list(mod_selection, "Choose Modification", str(wk_element))

                    mod_choice = get_int_range(input("\nEnter Modification Choice: "), 1, max_mod_item_choice_number)

                    if mod_choice is None or mod_choice > max_mod_item_choice_number or mod_choice < 1:

                        print("\n### Error - Modify Number Entered Must be Between 1 and " + str(max_mod_item_choice_number) + " ###")

                    elif mod_choice == 1:

                        # process Modify Item Description

                        element_description = ""

                        while element_description == "":

                            element_description = input("\nEnter Workout Description: ")

                            if element_description == "":
                                print("Entered workout description cannot be blank")
                            else:
                                wk_element[0] = element_description
                                element_list[element_choice - 1] = wk_element
                                health_database.update_workout(wk_element[3], wk_element[0], wk_element[2], wk_element[1])

                    elif mod_choice == 2:

                        # process Modify Calories

                        calories: int | None = None

                        while calories is None:

                            calories = get_int(input("\nEnter calories: "))
                            if calories is None:
                                print("\nEntered calories must be an integer")
                            else:
                                wk_element[2] = calories
                                element_list[element_choice - 1] = wk_element
                                health_database.update_workout(wk_element[3], wk_element[0], wk_element[2], wk_element[1])

                        # update_element(element_type, wk_element)

                    elif mod_choice == 3:

                        # process type

                        element_type_done = False

                        while not  element_type_done:

                            max_type_choices = len(element_type_list) + 1

                            gen_selection_list(element_type_list, "Choose Workout Type")
                            print(str(max_type_choices ) + ". Exit\n")

                            type_choice = get_int_range(input("Choose Workout Type: "), 1, max_type_choices)

                            # print("type_choice = " + type_choice)

                            if type_choice is None:

                                print("Entered Workout Type Cannot be Blank")

                            elif type_choice < 1 or type_choice > max_type_choices:

                                print("Workout Type Must be Between 1 And " + str(max_type_choices))

                            elif type_choice < max_type_choices:
                                element_type_choice = element_type_list[type_choice - 1]
                                wk_element[1] = element_type_choice
                                element_list[element_choice - 1] = wk_element
                                health_database.update_workout(wk_element[3], wk_element[0], wk_element[2], wk_element[1])
                                element_type_done = True

                            else:
                                element_type_done = True
                                update_done = True

                    else:

                        # exit
                        update_done = True

            else:
                mod_done = True



def delete_element(element_type):

    # get element date

    element_date = get_date("\nEnter " + element_type + " Date: ")

    # print("element_date = ", element_date.strftime("%m/%d/%Y"))

    # element: DayEntity | None = DayEntity.get_day(element_date)

    element_list = []
    element_type_list = []

    if element_type == "Meal":

        element_list = health_database.get_meals(element_date)
        element_type_list = list(MealType)

    else:

        element_list = health_database.get_workouts(element_date)
        element_type_list = list(WorkoutType)

    choice: int | None = None


    #  check for no entry on date

    if len(element_list) == 0:

        print("\nNo " + element_type + " Entered for ", element_date.strftime("%m/%d/%Y"), "/n")

    else:

        # get list of entries

        done = False

        while not done:

            #  choose entry

            print("\n### Choose " + element_type + " To Delete: ###\n")

            choice_number = 1

            for el in element_list:

                print(str(choice_number) + ". " + str(el))
                choice_number += 1

            print(str(choice_number) + ". Exit")

            choice = get_int_range(input("\nEnter " + element_type + " to Delete Number: "), 1, choice_number)

            # check for bad selection

            if choice is None or choice > choice_number or choice < 1:

                print("\n### Error - " + element_type + " Number Entered Must be Between 1 and " + str(choice_number) + " ###")

            #  delete selection

            elif 1 <= choice < choice_number:


                id = element_list[choice - 1][3]

                if element_type == "Meal":
                    health_database.delete_meal(id)

                else:
                    health_database.delete_workout(id)

                del element_list[choice - 1]
                if len(element_list) == 0:
                    done = True

            else:

                done = True

def filter_by_date():

    #  get current year

    current_year = date.today().year

    start_date: date = None
    stop_date: date = None

    date_option_list = ["Filter by Year", "Filter by Month(in our current year " + str(current_year) + ")", "Filter by Date Range", "Exit"]

    date_option_list_len_max = len(date_option_list)

    date_filter_done = False

    date_option_choice = 0

    while not date_filter_done:

        # enter date range

        gen_selection_list(date_option_list, "Filter by Date")

        date_option_choice = get_int_range(input("\nChoose Operation: "), 1, date_option_list_len_max)

        if date_option_choice is None or date_option_choice > date_option_list_len_max or date_option_choice < 1:

            print("\n### Error - The Filter by Date Number Entered Must be Between 1 and " + str(date_option_choice) + " ###")

        # filter by year

        elif date_option_choice == 1:

            year_filter_done = False

            while not year_filter_done:

                # current_year = date.today().year

                choice_year = get_int_range(input("\nChoose Operation(Must be Between 2000 and " + str(current_year) + "): "), 2000, current_year)

                print("\nYear Chosen: " + str(choice_year) + "\n")

                if choice_year is None or choice_year < 2000 or choice_year > current_year:
                    print("\n### Error - Year Entered Must be Between 2000 and " + str(current_year) + " ###")

                else:

                    start_date = date(choice_year, 1, 1)
                    stop_date_excluded = date(choice_year + 1, 1, 1)
                    stop_date = stop_date_excluded + timedelta(days=-1)

                    v = filter_by_date_range(start_date, stop_date_excluded)

                    if v != "":
                        print(v)
                    else:
                        print("There are no entries for the year " + str(choice_year) + ".")

                    year_filter_done = True

        # filter by month for current year

        elif date_option_choice == 2:

            month_option_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "Exit"]

            month_filter_done = False

            while not month_filter_done:
                gen_selection_list(month_option_list, "Filter by Month")

                choice_month = get_int_range(input("\nChoose Month: "), 1, 13)

                if choice_month is None or choice_month < 1 or choice_month > 13:
                    print("\n### Error - Value Entered Must be Between 1 and 13 ###")

                else:

                    if choice_month < 13:

                        choice_month_str = month_option_list[choice_month - 1]

                        print("\nMonth Chosen: " + choice_month_str + "\n")

                        start_date = date(current_year, choice_month, 1)
                        stop_year = current_year
                        stop_month = choice_month + 1
                        if choice_month == 12:
                            stop_year += 1
                            stop_month = 1
                        stop_date_excluded = date(stop_year, stop_month, 1)
                        stop_date = stop_date_excluded + timedelta(days=-1)

                        v = filter_by_date_range(start_date, stop_date_excluded)

                        if v != "":
                            print(v)
                        else:
                            print("There are no entries for the month " + choice_month_str + ", " + str(current_year) + ".")

                    else:

                        month_filter_done = True

        # filter by date range

        elif date_option_choice == 3:

            print("\n## Filter by Date Range ##")

            valid_range = False

            while not valid_range:

                start_date = get_date("\nEnter start date: ")

                stop_date = get_date("\nEnter stop date: ")

                if(start_date > stop_date):
                    print("Error, start date must come before end date.")
                else:
                    stop_date_excluded = stop_date + timedelta(days=1)

                    v = filter_by_date_range(start_date, stop_date_excluded)

                    if v != "":
                        print("\n" + v)
                    else:
                        print("\nThere are no entries for the date range " + start_date.__str__() + " to " + stop_date.__str__() + ".")

                    valid_range = True

        else:

            date_filter_done = True

        if start_date is not None and stop_date is not None and 0 <= date_option_choice < date_option_list_len_max:

            print("\n### Save Report ###")
            print("\n1. Save to CSV")
            print("\n2. Exit")

            create_file_choice = get_int_range(input("\nChoose Operation: "), 1, 2)

            if create_file_choice == 1:

                file_choice_done = False

                while not file_choice_done:

                    filename = input("\nEnter file name(include .csv extension): ")

                    if filename is None:
                        print("\nFilename can not be blank")
                    elif ' ' in filename:
                        print("\nFilename can not contain spaces")
                    elif not pathvalidate.is_valid_filename(filename):
                        print("\nFilename contains illegal characters")
                    elif not filename.endswith(".csv"):
                        print("\nFilename does not end with .csv")
                    else:
                        write_out_report(filename, start_date, stop_date)
                        file_choice_done = True


##### test data ######


def add_test_data():
    # test data

    test_date: date = date(2026, 5, 1)
    health_database.add_day(test_date)
    health_database.add_meal(test_date, Meal("cereal", "Breakfast", 300, 0))
    health_database.add_meal(test_date, Meal("sandwich", "Lunch", 500, 0))
    health_database.add_meal(test_date, Meal("stew", "Dinner", 500, 0))
    health_database.add_workout(test_date, Workout("run", "Cardio", 400, 0))
    health_database.add_workout(test_date, Workout("weight lifting", "Strength", 400, 0))

    test_date = date(2026, 5, 2)
    health_database.add_day(test_date)
    health_database.add_meal(test_date, Meal("eggs", "Breakfast", 300, 0))
    health_database.add_meal(test_date, Meal("soup", "Lunch", 300, 0))
    health_database.add_meal(test_date, Meal("steak", "Dinner", 500, 0))
    health_database.add_workout(test_date, Workout("run", "Cardio", 400, 0))

    test_date = date(2026, 5, 4)
    health_database.add_day(test_date)
    health_database.add_meal(test_date, Meal("bacon and eggs", "Breakfast", 500, 0))
    health_database.add_meal(test_date, Meal("soup and sandwich", "Lunch", 400, 0))
    health_database.add_meal(test_date, Meal("steak", "Dinner", 500, 0))
    health_database.add_workout(test_date, Workout("hike", "Cardio", 300, 0))

    test_date = date(2026, 5, 5)
    health_database.add_day(test_date)
    health_database.add_meal(test_date, Meal("bacon and eggs", "Breakfast", 500, 0))
    health_database.add_meal(test_date, Meal("soup and sandwich", "Lunch", 400, 0))
    health_database.add_meal(test_date, Meal("steak", "Dinner", 500, 0))
    health_database.add_workout(test_date, Workout("hike", "Cardio", 300, 0))
    health_database.add_workout(test_date, Workout("weight lifting", "Strength", 400, 0))


