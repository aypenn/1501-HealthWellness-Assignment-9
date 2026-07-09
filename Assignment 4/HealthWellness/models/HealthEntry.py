

class HealthEntry:
    def __init__(self, description: str, entry_type: str, calories: int) -> None:
        self.__description = description
        self.__entry_type = entry_type
        if calories > 0:
            self.__calories = calories
        else:
            self.__calories = 0

    def __str__(self):
        return "Entry: " + self.__description + ", Calories: " + str(self.__calories) + ", Type: " + self.__entry_type

    def calories(self) -> int:
        return self.__calories