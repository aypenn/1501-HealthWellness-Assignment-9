# from datetime import date
# from models.DayEntity import *
# from models.CalorieEntity import *
#
# entry_dates = {}
#
# mealTracker = {} # each value is the calorie count for the meal
# workoutTracker = {} # each entry is the calorie count burned from the workout
#
# def add_day(entry_date: date | None)  -> DayEntity | None:
#
#     if entry_date is None:
#         return None
#     elif entry_date not in entry_dates:
#         v: DayEntity = DayEntity(entry_date)
#         entry_dates[entry_date] = v
#         return entry_dates[entry_date]
#     else:
#         return entry_dates[entry_date]
#
# def min_date() -> date | None:
#     if len(entry_dates) == 0:
#         return None
#     else:
#         min_date: date = min(entry_dates, key=entry_dates.get("entry_date"))
#         return min_date
#
# def max_date() -> date | None:
#     if len(entry_dates) == 0:
#         return None
#     else:
#         max_date: date = max(entry_dates, key=entry_dates.get("entry_date"))
#         return max_date
#
# def get_day(entry_date: date | None) -> DayEntity | None:
#
#         if entry_date is None:
#             return None
#         elif entry_date not in entry_dates:
#             return None
#         else:
#             return entry_dates[entry_date]
#
#
# def add_meal(meal_date: date | None, meal:Meal) -> bool:
#
#     # print("In add_meal meal_date = " + str(meal_date))
#     # print("In add_meal meal = " +  str(meal))
#
#     # v: DayEntity | None = add_day(meal_date)
#
#     v: DayEntity | None = add_day(meal_date)
#
#     if v is None:
#         return False
#     else:
#         v.add_meal(meal)
#         return True
#
#
# def add_workout(workout_date: date | None, workout:Workout) -> bool:
#
#     # print("In add_workout workout_date = " + str(workout_date))
#     # print("In add_workout workout = " +  str(workout))
#
#     v: DayEntity | None = add_day(workout_date)
#
#     if v is None:
#         return False
#     else:
#
#         v.add_workout(workout)
#         return True
#
#
#
