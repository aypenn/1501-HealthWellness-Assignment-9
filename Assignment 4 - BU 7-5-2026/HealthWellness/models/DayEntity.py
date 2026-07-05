from datetime import date

from models.CalorieEntity import *

class DayEntity:

    def __init__(self, entry_date: date):
        self.__entry_date = date
        self.__meal = []
        self.__workout = []


    def add_meal(self, meal: Meal):
        self.__meal.append(meal)

    @property
    def meal_calories(self):
        val = 0
        if len(self.__meal) > 0:
            for meal in self.__meal:
                val += meal.calories
        return val

    @property
    def meals_to_string(self):
        val = ""
        if len(self.__meal) > 0:
            for meal in self.__meal:
                if val != "":
                    val += ",\n"
                val += "\t" + str(meal)
        return val

    def add_workout(self, workout: Workout):
        self.__workout.append(workout)

    @property
    def workout_calories(self):
        val = 0
        if len(self.__workout) > 0:
            for workout in self.__workout:
                val += "\t" + workout.calories
        return val

    @property
    def workout_to_string(self):
        val = ""
        if len(self.__workout) > 0:
            for workout in self.__workout:
                if val != "":
                    val += ",\n"
                val += str(workout)
        return val


    def __eq__(self, other):
        return self.__entry_date == other.entry_date and self.__meal == other.meal and self.__workout == other.workout


    def __str__(self) -> str:
        val = "Meals:\n"
        net_calories = 0
        if len(self.__meal) > 0:
            for meal in self.__meal:
                print ("meal = ", meal)
                val += "\t" + str(meal) + "\n"
                net_calories += meal.calories()
        else:
            val += "\tNo meals entered\n"

        val += "Workouts:\n"
        if len(self.__workout) > 0:
            for workout in self.__workout:
                val += "\t" +str(workout) + "\n"
                net_calories -= workout.calories()
        else:
            val += "\tNo workouts entered\n"

        if net_calories != 0:
            val += "Net Calories: " + str(net_calories) + "\n"

        return val

