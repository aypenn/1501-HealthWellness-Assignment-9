from datetime import date

from models.HealthEntry import *
from models.EntryType import *
from services import health_database


class Meal(HealthEntry):
    def __init__(self, meal_item: str, meal_type: str, calories: int, entry_id:int = 0) -> None:
        id: int = entry_id
        meal_item: str = meal_item
        meal_type:MealType = MealType(meal_type)
        super().__init__(meal_item, str(meal_type), calories, id)

    def to_dict(self) -> dict:
        return {"description": self.description(), "calories": self.calories(), "meal_type": self.entry_type()}

    # def id(self) -> int:
    #     return self.id

    # def add_update_meal(self, entry_date: date) -> bool:
    #     return health_database.update_meal(self.id, self.description(), self.calories(), self.entry_type())

    def add_meal(self, entry_date: date) -> bool:
        return health_database.add_meal(entry_date, self.description(), self.calories(), self.entry_type())

    # def update_meal(self) -> bool:
    #     return health_database.update_meal(self.id, self.description(), self.calories(), self.entry_type())

    # def update_meal_description(self, description: str) -> bool:
    #     self.__description = description
    #     return health_database.update_meal_description(self.id, description)

    # def update_description(self, description: str) -> bool:
    #     self.__description = description
    #     return health_database.update_meal_description(self.id, description)
    #
    # def update_meal_calories(self, calories: int) -> bool:
    #     return health_database.update_meal_calories(self.id, calories)
    #
    #
    # def update_meal_type(self, type: str) -> bool:
    #     return health_database.update_meal_type(self.id, type)

    def delete_meal(self) -> bool:
        return health_database.delete_meal(self.id)

    def __str__(self) -> str:
        return "Meal: " + str(self.description()) + "\tMeal Type: " + str(self.entry_type()) + "\tCalories: " + str(self.calories()) + "\tID: " + str(self.id())

class Workout(HealthEntry):
    def __init__(self, workout_item: str, workout_type: str, calories: int, entry_id:int = 0) -> None:
        id: int = entry_id
        workout_item: str = workout_item
        workout_type: WorkoutType = WorkoutType(workout_type)
        super().__init__(workout_item, str(workout_type), calories, id)

    def to_dict(self) -> dict:
        return {"description": self.description(), "calories": self.calories(), "workout_type": self.entry_type()}

    def add_workout(self, entry_date: date) -> bool:
        return health_database.add_workout(entry_date, self.description(), self.calories(), self.entry_type())

    def __str__(self) -> str:
        return "Workout: " + str(self.description()) + "\tWorkout Type: " + str(self.entry_type()) + "\tCalories: " + str(self.calories()) + "\tID: " + str(self.id())
