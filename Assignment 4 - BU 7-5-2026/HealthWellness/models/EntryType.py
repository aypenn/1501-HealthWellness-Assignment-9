from enum import Enum

class MealType(Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    SNACK = "Snack"

    def __str__(self):
        return str(self.value)

class WorkoutType(Enum):
    CARDIO = "CARDIO"
    STRENGTH = "STRENGTH"
    FLEXIBILITY = "FLEXIBILITY"
    HIGH_INTENSITY = "HIGH_INTENSITY"
    GROUP_FITNESS = "GROUP_FITNESS"
    OTHER = "OTHER"

    def __str__(self):
        return str(self.value)
