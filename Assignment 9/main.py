'''
    INFO 1501 - Python I
    Welcome to the Health and Wellness System
    You will be working on this throughout the course and adding to it

    Please read instructions for each assignment clearly and don't go beyond the functionality
    required as we will be adding more each week.

    Make sure to merge branches and create new branches for each week's assignment.
'''
from operator import index, truediv

from utils.main_methods import *
from services.data_xml_io import *
from services.data_json_io import *
from services.data_csv_report import *


import services.health_data as health_data

# global dictionaries for meal and workout
# keys are date - in string format - for now

from models.EntryType import *

def main():

    app_path = Path(__file__).parent.resolve()

    # add_test_data()

    # TODO: You need to make this system file loop for the menu until they exit.
    # print menu - We will be adding to these as we go throughout the course


    main_choice_list = ["Add Meal", "Add Workout", "Search Date", "Modify Meal", "Delete Meal",
                        "Modify Workout", "Delete Workout", "Filter By Date", "Load In From XML",
                        "Exit"]

    main_choice_list_len = len(main_choice_list)

    choice = 0

    while choice != main_choice_list_len:

        gen_selection_list(main_choice_list, "Health and Wellness App")

        # get input

        choice = get_int_range(input("\nChoose Operation: "), 1, main_choice_list_len)

        if choice is None or choice > main_choice_list_len:
            print("\n### Error - Value Entered Must be Between 1 and " + str(main_choice_list_len) + " ###")
        else:

            match choice:
                case 1:
                    add_meal()
                case 2:
                    add_workout()
                case 3:
                    search_date()
                case 4:
                    # update_calorie_element("Meal")
                    update_meal()
                case 5:
                    delete_element("Meal")
                case 6:
                    # update_calorie_element("Workout")
                    update_workout()
                case 7:
                    delete_element("Workout")
                case 8:
                    filter_by_date()
                case 9:
                    read_xml_file()
                case 10:
                    print("\nSystem Exiting...")

            # test code - leave in
            # print()
            # print("\n\n")
            # for d in health_data.entry_dates:
            #     if len(d.__meal) > 0:
            #         for m in d.__meal:
            #             print(str(d.__meal))

            # print(health_data.entry_dates)


if __name__ == "__main__":
    main()