

class HealthEntry:
    def __init__(self, description: str, calories: int) -> None:
        self.__description = description
        if calories > 0:
            self.__calories = calories
        else:
            self.__calories = 0

    def __str__(self):
        return "Meal/Item: " + self.__description + ", Calories: " + str(self.__calories)

    def calories(self) -> int:
        return self.__calories