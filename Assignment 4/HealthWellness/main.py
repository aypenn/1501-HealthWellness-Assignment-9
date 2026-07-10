'''
    INFO 1501 - Python I
    Welcome to the Health and Wellness System
    You will be working on this throughout the course and adding to it

    Please read instructions for each assignment clearly and don't go beyond the functionality
    required as we will be adding more each week.

    Make sure to merge branches and create new branches for each week's assignment.
'''
from operator import index

from models import DayEntity
from datetime import datetime
# This is the UI for the Health and Wellness system

from utils.input_utils import *
from models.CalorieEntity import *
from models.DayEntity import *

import services.health_data as health_data

# global dictionaries for meal and workout
# keys are date - in string format - for now

from models.EntryType import *

def get_date(input_message):

    got_value = False

    #get current date

    while not got_value:

        wk_date = get_valid_date(input(input_message))

        if wk_date is None:
            print("\n### Error - Date cannot be blank and must be in ""MM/DD/YYYY"" format ###")
        elif wk_date > date.today():
            print("\n### Error - Date cannot be a date in the future ###")
        else:
            got_value = True
            return wk_date


# TODO: Create functions to add meal, add workout and search via date in the dictionary.

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

            v = Meal(meal_description, meal_type, calories)
            if not health_data.add_meal(meal_date, v):
                print("\n### Error - Meal not added because a meal has already been added for the date "+ meal_date.strftime("%m/%d/%Y") + " ###\n")
            print("### Meal entry added\n")

        elif choice == total_choices:
            print("\nSystem Exiting...")
        else:
            print("\n### Error - meal item entered must be between 1 and 5 ###")


    # while meal_item.upper() != "Q":
    #
    #     meal_item = input("\nEnter meal item(enter 'Q' to quit): ")
    #
    #
    #
    #     #check for blank entry
    #
    #     if meal_item.strip() == "":
    #         print("\n### Error - Meal item cannot be blank ###")
    #
    #     elif meal_item.upper() != "Q":
    #
    #         got_value = False
    #
    #         while not got_value:
    #
    #             calories = get_int(input("Enter calories: "))
    #
    #             if calories is not None and calories > 0:
    #                 got_value = True
    #             else:
    #                 print("\n### Error - calories entered must be greater than 0 and must be an integer ###")
    #
    #         # add to db
    #
    #         v = Meal(meal_item, int(calories))
    #         if not health_data.add_meal(meal_date, v):
    #             print("\n### Error - Meal not added because a meal has already been added for the date "+ meal_date.strftime("%m/%d/%Y") + " ###\n")
    #         print("### Meal entry added\n")
    #         meal_item = "q"

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

            v: Workout = Workout(workout_description, workout_type, calories)

            if not health_data.add_workout(workout_date, v):
                print("\n### Error - Workout not added because a workout has already been added for the date " + workout_date.strftime("%m/%d/%Y") + " ###\n")
            else:
                print("### Workout entry added\n")

# def add_workout():
#
#     # get work out date
#
#     workout_date = get_date("\nEnter workout date: ")
#
#     workout_item = ""
#     workout_calories = 0
#
#     #get work out detail and calories
#
#     details = ""
#     calories = 0
#
#     while details.strip() == "":
#
#         details = input("\nEnter workout details: ")
#
#         if details.strip() == "":
#
#             print("\n### Error - Workout details cannot be blank ###")
#
#         else:
#
#             got_value = False
#
#             while not got_value:
#
#                 calories = get_int(input("Enter calories: "))
#
#                 print("calories = " + str(calories))
#                 # if calories is not None and calories > 0:
#
#
#                 if calories is None or calories < 0:
#                     print("\n### Error - calories entered must be greater than 0 and must be an integer ###")
#                 else:
#                     got_value = True
#
#                 #add to db
#
#             v: Workout = Workout(details, int(calories))
#
#             if not health_data.add_workout(workout_date, v):
#                 print("\n### Error - Workout not added because a workout has already been added for the date " + workout_date.strftime("%m/%d/%Y") + " ###\n")
#             else:
#                 print("### Workout entry added\n")

def search_date():

    # get search date

    search_day = get_date("\nEnter search date: ")

    #print("Search Date = ", search_day)

    v: DayEntity | None = health_data.get_day(search_day)

    if v is not None:

        print(str(v))

    else:

        print("\nNo entries for this search date\n")


def main():

    # TODO: You need to make this system file loop for the menu until they exit.
    # print menu - We will be adding to these as we go throughout the course

    choice = 0

    while choice != 4:
        print("### Health and Wellness App ###")
        print("1. Add Meal")
        print("2. Add Workout")
        print("3. Search Date")
        print("4. Exit")

        # get input

        choice = get_int_range(input("Choose operation: "), 1, 4)

        # TODO: You need to validate the choice operation input is between 1-4 using a while loop NOT just having else on the if/elif below.

        # call other functions based on input - You need to do this
        # TODO: You need to create other functions outside of main and call them here for each operation.

        if choice is None:
            print("\n### Error - Value entered must be between 1 and 4 ###")
        elif choice == 1:
            # pass
            add_meal()
        elif choice == 2:
            add_workout()
        elif choice == 3:
            search_date()
        elif choice == 4:
            print("\nSystem Exiting...")

            # test code - leave in
            # print()
            # print("\n\n")
            # for d in health_data.entry_dates:
            #     if len(d.__meal) > 0:
            #         for m in d.__meal:
            #             print(str(d.__meal))

            # print(health_data.entry_dates)


        else:
            print("\n### Error - Value entered must be between 1 and 4 ###")

if __name__ == "__main__":
    main()