'''
This file is for you to help create and manage the start of your database
You are NOT tasked with creating the tables and manage them but rather use this file.

@author: Lucas Hartman
@version: 1.0
'''
import sqlite3

# if this file is in a package, the ../ puts it outside the package at the project level
database_name = "../health_data.db" # if you would like to change this, fine but mirror it to your files

CREATE_MEALS_TABLE = """
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        description TEXT NOT NULL,
        calories INTEGER NOT NULL,
        meal_type TEXT NOT NULL
    );
"""

CREATE_WORKOUTS_TABLE = """
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        description TEXT NOT NULL,
        calories INTEGER NOT NULL,
        workout_type TEXT NOT NULL
    );
"""

def  get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_meals_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_MEALS_TABLE)
    conn.commit()
    conn.close()

def create_workouts_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_WORKOUTS_TABLE)
    conn.commit()
    conn.close()

def delete_meals_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS meals;")
    conn.commit()
    conn.close()

def delete_workouts_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS workouts;")
    conn.commit()
    conn.close()

def main():
    choice = 0
    while choice != 5:
        print("** Database Management **")
        print("1. Create Meals Table")
        print("2. Create Workouts Table")
        print("3. Delete Meals Table")
        print("4. Delete Workouts Table")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                create_meals_table()
            elif choice == 2:
                create_workouts_table()
            elif choice == 3:
                delete_meals_table()
            elif choice == 4:
                delete_workouts_table()
            else:
                print("invalid operation")
        except ValueError:
            print("Error, enter a number.")


if __name__ == "__main__":
    main()


