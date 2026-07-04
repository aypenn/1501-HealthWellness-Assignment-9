
class Meal:
    def __init__(self, meal_item: str, calories: int) -> None:
       # self.__meal_date = None
        self.__meal_item = meal_item
        if calories > 0:
            self.__calories = calories
        else:
            self.__calories = 0

    def __str__(self):
        return "Meal/Item: " + self.__meal_item + ", Calories: " + str(self.__calories)

    def calories(self) -> int:
        return self.__calories


class Workout:
    def __init__(self, workout_item: str, calories: int):
       # self.meal_date = None
        self.__workout_item = workout_item
        if calories > 0:
            self.__calories = calories
        else:
            self.__calories = 0

    def __str__(self):
        return "Workout: " + self.__workout_item + ", Calories: " + str(self.__calories)

    def calories(self) -> int:
        return self.__calories