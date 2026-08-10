

class HealthEntry:
    def __init__(self, description: str, entry_type: str, calories: int, entry_id: int = 0) -> None:
        self.__description = description
        self.__entry_type = entry_type
        self.__calories = calories
        self.__entry_id = entry_id


    def __str__(self):
        description = self.__description
        entry_type = self.__entry_type
        calories = str(self.__calories)
        return "Entry: " + self.__description + ", Calories: " + str(self.__calories) + ", Type: " + self.__entry_type

    def calories(self) -> int:
        return self.__calories

    def description(self) -> str:
        return self.__description

    def id(self) -> str:
        return self.__entry_id

    def entry_type(self) -> str:
        return self.__entry_type

    def entry_type_set(self, entry_type: str) -> None:
        self.__entry_type = entry_type

    def entry_id_get(self) -> int:
        return self.__entry_id

    def id(self) -> int:
        return self.__entry_id

    def calories_set(self, calories: int) -> None:
        self.__calories = calories

    def description_set(self, description: str) -> None:
        self.__description = description

    def __eq__(self, other):
        # Ensure the other object is of the same type
        if not isinstance(other, HealthEntry):
            return False
        return self.__description == other.__description and self.__entry_type == other.__entry_type and self.__calories == other.__calories



