from models.HealthEntry import *
from models.EntryType import *

class Meal(HealthEntry):
    def __init__(self, meal_item: str, meal_type: str, calories: int) -> None:
        meal_item: str = meal_item
        meal_type:MealType = MealType(meal_type)
        super().__init__(meal_item, str(meal_type), calories)

        # self.__meal_item = meal_item
        # if calories > 0:
        #     self.__calories = calories
        # else:
        #     self.__calories = 0

    # def __str__(self):
    #     return "Meal/Item: " + self.__meal_item + ", Calories: " + str(self.__calories)

    # def calories(self) -> int:
    #     return self.calories()


class Workout(HealthEntry):
    def __init__(self, workout_item: str, workout_type: str, calories: int) -> None:
        workout_item: str = workout_item
        workout_type: WorkoutType = WorkoutType(workout_type)
        super().__init__(workout_item, str(workout_type), calories)

    # def __init__(self, workout_item: str, calories: int):
    #    # self.meal_date = None
    #     self.__workout_item = workout_item
    #     if calories > 0:
    #         self.__calories = calories
    #     else:
    #         self.__calories = 0
    #
    # def __str__(self):
    #     return "Workout: " + self.__workout_item + ", Calories: " + str(self.__calories)

    # def calories(self) -> int:
    #     return self.calories()