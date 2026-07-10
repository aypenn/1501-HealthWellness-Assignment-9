from datetime import date
from models.DayEntity import *
from models.CalorieEntity import *

entry_dates = {}

mealTracker = {} # each value is the calorie count for the meal
workoutTracker = {} # each entry is the calorie count burned from the workout

def add_day(entry_date: date | None)  -> DayEntity | None:

    if entry_date is None:
        return None
    elif entry_date not in entry_dates:
        v: DayEntity = DayEntity(entry_date)
        entry_dates[entry_date] = v
        return entry_dates[entry_date]
    else:
        return entry_dates[entry_date]

def get_day(entry_date: date | None) -> DayEntity | None:

        if entry_date is None:
            return None
        elif entry_date not in entry_dates:
            return None
        else:
            return entry_dates[entry_date]


def add_meal(meal_date: date | None, meal:Meal) -> bool:

    v: DayEntity | None = add_day(meal_date)

    if v is None:
        return False
    else:
        v.add_meal(meal)
        return True


def add_workout(workout_date: date | None, workout:Workout) -> bool:

    v: DayEntity | None = add_day(workout_date)

    if v is None:
        return False
    else:

        v.add_workout(workout)
        return True
        v.add_workout(workout)
        return True
