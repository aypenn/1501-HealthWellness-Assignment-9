import sqlite3
from datetime import date, datetime, timedelta
from logging import exception
from mimetypes import init
from pathlib import Path
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.CalorieEntity import Meal, Workout

class CalorieEntity:
    # Use a string literal for the type hint to prevent execution errors
    def add_meal(self, meal: "Meal") -> None:
        pass

    def add_workout(self, meal: "Workout") -> None:
        pass



def get_connection() -> sqlite3.Connection:

    # contect to db

    db_file = str(Path(__file__).parent.resolve().parent) + "\\health_data.db"
    conn = sqlite3.connect(db_file, timeout=30.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    return conn


def add_meal(entry_date: date, description: str, calories: int, entry_type: str) -> bool:

    # insert new meal

    conn = get_connection()
    cursor = conn.cursor()
    return_value: bool = True

    try:

        # insert data into meals table
        cursor.execute("INSERT INTO meals (date, description, calories, meal_type) VALUES (?, ?, ?, ?)",
                       (entry_date.strftime("%Y-%m-%d"), description, calories, entry_type))

        conn.execute("PRAGMA journal_mode=WAL;")
        conn.commit()

    except Exception as ex:

        print("add_meal - in exception - " + str(ex))

        conn.rollback()
        return_value = False

    finally:

        conn.close() # close no matter error or not

    return return_value

def get_meals(search_date_date: date) -> []:

    conn = get_connection()
    cursor = conn.cursor()

    meals = []

    try:

        # get meals for date

        sql = f"SELECT description, meal_type, calories, id, date FROM meals WHERE date = '{search_date_date.strftime('%Y-%m-%d')}'"

        cursor.execute(sql)

        rows = cursor.fetchall()

        # print("rows = " + str(rows))

        for row in rows:
            meals.append((row[0], row[1], row[2], row[3], row[4]))

    except Exception as ex:

        print("get_meals - in exception - " + str(ex))


    finally:

        conn.close()  # close no matter error or not

    return meals

def update_meal(id:int, description: str, calories: int, entry_type: str) -> bool:

    # update meal record

    conn = get_connection()
    cursor = conn.cursor()

    return_value: bool = True

    try:
        sql = (f"Update meals Set description = '{description}', calories = {calories}, meal_type = '{entry_type}' WHERE id = {id}")

        cursor.execute(sql)

        conn.commit()

    except Exception as ex:

        print("update_meals - in exception - " + str(ex))

        return_value = False

    finally:

        conn.close()  # close no matter error or not

    return return_value

def update_meal_description(id:int, description: str) -> bool:

    # update meal record

    conn = get_connection()
    cursor = conn.cursor()

    return_value: bool = True

    try:
        sql = (f"Update meals Set description = '{description}' WHERE id = {id}")

        cursor.execute(sql)

        conn.commit()

    except Exception as ex:

        print("update_meals_description - in exception - " + str(ex))

        return_value = False

    finally:

        conn.close()  # close no matter error or not

    return return_value

def update_meal_calories(id:int, calories: int) -> bool:

    # update meal record

    conn = get_connection()
    cursor = conn.cursor()

    return_value: bool = True

    try:
        sql = (f"Update meals Set calories = '{calories}' WHERE id = {id}")

        cursor.execute(sql)

        conn.commit()

    except Exception as ex:

        print("update_meals_calories - in exception - " + str(ex))

        return_value = False

    finally:

        conn.close()  # close no matter error or not

    return return_value

def update_meal_type(id:int, meal_type: str) -> bool:

    # update meal record

    conn = get_connection()
    cursor = conn.cursor()

    return_value: bool = True

    try:
        sql = (f"Update meals Set meal_type = '{meal_type}' WHERE id = {id}")

        cursor.execute(sql)

        conn.commit()

    except Exception as ex:

        print("update_meal_type - in exception - " + str(ex))

        return_value = False

    finally:

        conn.close()  # close no matter error or not

    return return_value


def delete_meal(id: int) -> bool:

    # delete meal record

    conn = get_connection()
    cursor = conn.cursor()

    return_value: bool = True

    try:
        sql = (f"Delete From meals WHERE id = {id}")

        cursor.execute(sql)

        conn.commit()

    except Exception as ex:

        print("delete_meal - in exception - " + str(ex))

        return_value = False

    finally:

        conn.close()  # close no matter error or not

    return return_value

def meals_min_date() -> date | None:

    # get minimum date in meals

    conn = get_connection()
    cursor = conn.cursor()

    return_value: date | None = None

    try:

        cursor.execute("Select Min(date) from meals")

        conn.execute("PRAGMA journal_mode=WAL;")
        row = cursor.fetchone()
        conn.commit()

        if row is not None:
            return_value: date = datetime.strptime(row[0], "%Y-%m-%d").date()
        else:
            return_value: date = date.today() + timedelta(days = -1)

    except Exception as ex:

        print("meals_min_date - in exception - " + str(ex))

    finally:

        conn.close()  # close no matter error or not

    return return_value

def meals_max_date() -> date | None:
    # get max date in meals
    conn = get_connection()
    cursor = conn.cursor()

    return_value: date | None = None

    try:

        cursor.execute("Select Max(date) from meals")

        conn.execute("PRAGMA journal_mode=WAL;")
        row = cursor.fetchone()
        conn.commit()

        if row is not None:
            return_value: date = datetime.strptime(row[0], "%Y-%m-%d").date()
        else:
            return_value: date = date.today()

    except Exception as ex:

        print("meals_max_date - in exception - " + str(ex))

    finally:

        conn.close()  # close no matter error or not

    return return_value



def add_workout(entry_date: date, description: str, calories: int, entry_type: str) -> bool:

    # insert new workout

    conn = get_connection()
    cursor = conn.cursor()

    return_value: bool = True

    try:

        cursor.execute("INSERT INTO workouts (date, description, calories, workout_type) VALUES (?, ?, ?, ?)",
                       (entry_date.strftime("%Y-%m-%d"), description, calories, entry_type))

        conn.execute("PRAGMA journal_mode=WAL;")
        conn.commit()

    except Exception as ex:

        print("add_workout - in exception - " + str(ex))

        conn.rollback()
        return_value = False

    finally:

        conn.close()  # close no matter error or not

    return return_value


def get_workouts(search_date_date: date) -> []:

    # get workouts for date

    conn = get_connection()
    cursor = conn.cursor()

    workouts = []

    try:

        sql = f"SELECT description, workout_type, calories, id, date FROM workouts WHERE date = '{search_date_date.strftime('%Y-%m-%d')}'"

        cursor.execute(sql)

        rows = cursor.fetchall()

        for row in rows:
            workouts.append((row[0], row[1], row[2], row[3], row[4]))

    except Exception as ex:

        print("get_workouts - in exception - " + str(ex))

    finally:

        conn.close()  # close no matter error or not

    return workouts

def update_workout(id:int, description: str, calories: int, entry_type: str) -> bool:

    # update workout record

    conn = get_connection()
    cursor = conn.cursor()

    return_value: bool = True

    try:
        sql = (f"Update workouts Set description = '{description}', calories = {calories}, workout_type = '{entry_type}' WHERE id = {id}")

        cursor.execute(sql)

        conn.commit()

    except Exception as ex:

        print("update_workout - in exception - " + str(ex))

        return_value = False

    finally:

        conn.close()  # close no matter error or not

    return return_value

def delete_workout(id:int) -> bool:

    # delete workout record

    conn = get_connection()
    cursor = conn.cursor()

    return_value: bool = True

    try:
        sql = (f"Delete From workouts WHERE id = {id}")

        cursor.execute(sql)

        conn.commit()

    except Exception as ex:

        print("delete_workout - in exception - " + str(ex))

        return_value = False

    finally:

        conn.close()  # close no matter error or not

    return return_value

def workouts_min_date() -> date | None:

    # get workout table min date
    conn = get_connection()
    cursor = conn.cursor()

    return_value: date | None = None

    try:

        cursor.execute("Select Min(date) from workouts")

        conn.execute("PRAGMA journal_mode=WAL;")
        row = cursor.fetchone()
        conn.commit()

        if row is not None:
            return_value: date = datetime.strptime(row[0], "%Y-%m-%d").date()
        else:
            return_value: date = date.today() + timedelta(days = -1)


    except Exception as ex:

        print("workouts_min_date - in exception - " + str(ex))

    finally:

        conn.close()  # close no matter error or not

    return return_value


def workouts_max_date() -> date | None:
    # get workout table max date
    conn = get_connection()
    cursor = conn.cursor()

    return_value: date | None = None

    try:

        cursor.execute("Select Max(date) from workouts")

        conn.execute("PRAGMA journal_mode=WAL;")
        row = cursor.fetchone()
        conn.commit()

        if row is not None:
            return_value: date = datetime.strptime(row[0], "%Y-%m-%d").date()
        else:
            return_value: date = date.today()



    except Exception as ex:

        print("workouts_max_date - in exception - " + str(ex))

    finally:

        conn.close()  # close no matter error or not

    return return_value

def get_day(date: date) -> []:

    # get meal and workout calories for date

    conn = get_connection()
    cursor = conn.cursor()

    try:

        meal_calories: int = 0
        workout_calories: int = 0

        sql = (f"Select SUM(calories) FROM meals where date = '{date.strftime('%Y-%m-%d')}'")
        cursor.execute(sql)

        row_meal = cursor.fetchone()

        if row_meal is not None:
            meal_calories = row_meal[0]
        else:
            meal_calories = 0

        sql = (f"Select * FROM workouts WHERE date = '{date.strftime('%Y-%m-%d')}'")
        cursor.execute(sql)

        row_workouts = cursor.fetchone()

        if row_workouts is not None:
            workout_calories = row_workouts[0]
        else:
            workout_calories = 0

    except Exception as ex:

        print("get_day - in exception - " + str(ex))

    finally:

        conn.close()  # close no matter error or not

    return [meal_calories, workout_calories]



