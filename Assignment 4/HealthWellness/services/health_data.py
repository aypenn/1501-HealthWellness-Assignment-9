from datetime import date

mealTracker = {} # each value is the calorie count for the meal
workoutTracker = {} # each entry is the calorie count burned from the workout

def add_meal(meal_date: date | None, meal:dict) -> bool:

    if meal_date is None:
        return False
    elif meal_date in mealTracker:
        return False
    mealTracker[meal_date] = meal
    return True

def get_meal(meal_date: date | None) -> dict | None:

    if meal_date is None or meal_date not in mealTracker:
        return None
    else:
        item = mealTracker[meal_date]["item"]
        calories = mealTracker[meal_date]["calories"]
        return {"item": item, "calories": calories}


def add_workout(workout_date: date | None, workout:dict) -> bool:
    if workout_date is None:
        return False
    elif workout_date in workoutTracker:
        return False
    workoutTracker[workout_date] = workout
    return True


def get_workout(workout_date: date | None) -> dict | None:
    if workout_date is None or workout_date not in workoutTracker:
        return None
    else:
        details = workoutTracker[workout_date]["details"]
        calories = workoutTracker[workout_date]["calories"]
        return {"details": details, "calories": calories}
