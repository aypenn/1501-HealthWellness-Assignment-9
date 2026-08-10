from datetime import date
from datetime import datetime

from models.CalorieEntity import *
from models.HealthEntry import HealthEntry
from services import health_database
# from services.health_data import get_day


class DayEntity:

    def __init__(self, entry_date: date) -> None:
        self.__entry_date = entry_date
        self.__meal = []
        self.__workout = []

    # def __new__(cls, entry_date: date):
    #
    #     instance = super().__new__(cls)
    #     instance.entry_date = entry_date
    #     return instance

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

    def meal_list(self) -> list[Meal]:
        return self.__meal

    def meals_to_dict(self) -> dict:

        v = []
        for meal in self.__meal:
            md = meal.to_dict()
            v.append(md)

        return v

    def add_workout(self, workout: Workout):
        self.__workout.append(workout)

    @property
    def get_entry_date(self):
        return self.__entry_date

    # @property
    # def entry_date_str(self):
    #     return self.__entry_date.strftime("%Y-%m-%d")

    @property
    def workout_calories(self):
        val = 0
        if len(self.__workout) > 0:
            for workout in self.__workout:
                val += "\t" + workout.calories
        return val

    # def workout_calories_int(self) -> int:


    @property
    def workout_to_string(self):
        val = ""
        if len(self.__workout) > 0:
            for workout in self.__workout:
                if val != "":
                    val += ",\n"
                val += str(workout)
        return val

    def workouts_to_dict(self) -> dict:

        v = []
        for workout in self.__workout:
            wd = workout.to_dict()
            v.append(wd)

        return v

    def update_workout(self, workout: Workout) -> bool:
        return health_database.update_meal(workout)

    # def __eq__(self, other):
    #     return self.__entry_date == other.entry_date and self.__meal == other.meal and self.__workout == other.workout

    def __eq__(self, other):
        print("in __eq__(self, other):")
        if not isinstance(other, DayEntity):
            print("in 1")
            return False
        elif self.__entry_date != other.__entry_date:
            print("in 2")
            return False
        elif self.meal_list() != other.meal_list():
            print("in 3")
            return False
        elif self.workout_list() != other.workout_list():
            print("in 4")
            return False
        else:
            print("in 5")
            return True

        # and self.__workout == other.workout)

    def net_calories(self) -> int:

        net_calories = 0

        if len(self.__meal) > 0:
            for meal in self.__meal:
                net_calories += meal.calories()

        if len(self.__workout) > 0:
            for workout in self.__workout:
                net_calories -= workout.calories()

        return net_calories

    def __str__(self) -> str:

        val = "Entry Date: " + self.__entry_date.strftime("%Y-%m-%d") + "\n"

        val += "\tMeals:\n"
        net_calories:int = 0
        if len(self.__meal) > 0:
            for meal in self.__meal:
                val += "\t\t" + str(meal) + "\n"
                net_calories += meal.calories()
                # net_calories = net_calories + meal.calories
        else:
            val += "\t\tNo meals entered\n"

        val += "\tWorkouts:\n"
        if len(self.__workout) > 0:
            for workout in self.__workout:
                val += "\t\t" +str(workout) + "\n"
                net_calories -= workout.calories()
                # net_calories = net_calories - workout.calories
        else:
            val += "\t\tNo workouts entered\n"

        if net_calories != 0:
            val += "\tNet Calories: " + str(net_calories) + "\n"

        return val

    def workout_list(self) -> list[Workout]:
        return self.__workout

    def to_report(self) -> {} | None:

        meals_calories = 0
        workouts_calories = 0

        if len(self.__meal) > 0:
            for meal in self.__meal:
                meals_calories += meal.calories()

        if len(self.__workout) > 0:
            for workout in self.__workout:
                workouts_calories += workout.calories()

        net_calories = meals_calories - workouts_calories

        return {"Date" : self.__entry_date.strftime("%m/%d/%y"), "Meal Calories": str(meals_calories), "Workout Calories": str(workouts_calories), "Net Calories": str(net_calories)}

    def get_day(entry_date: date | None) -> DayEntity | None:

        meals = health_database.get_meals(entry_date)

        workouts = health_database.get_workouts(entry_date)

        if len(meals) != 0 or len(workouts) != 0:

            v = DayEntity(entry_date)
            for meal in meals:
                v.__meal.append(Meal(meal[0], meal[1], meal[2], meal[3]))
            for workout in workouts:
                v.__workout.append(Workout(workout[0], workout[1], workout[2], workout[3]))

            return v

        else:

             return None



