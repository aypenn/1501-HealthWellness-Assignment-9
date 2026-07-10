from models.HealthEntry import *
from models.EntryType import *

class Meal(HealthEntry):
    def __init__(self, meal_item: str, meal_type: str, calories: int) -> None:
        meal_item: str = meal_item
        meal_type:MealType = MealType(meal_type)
        super().__init__(meal_item, str(meal_type), calories)


class Workout(HealthEntry):
    def __init__(self, workout_item: str, workout_type: str, calories: int) -> None:
        workout_item: str = workout_item
        workout_type: WorkoutType = WorkoutType(workout_type)
        super().__init__(workout_item, str(workout_type), calories)
