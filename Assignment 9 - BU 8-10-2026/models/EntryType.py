from enum import Enum

class MealType(Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    SNACK = "Snack"
    NONE = None

    def __str__(self):
        return str(self.value)

class WorkoutType(Enum):
    CARDIO = "Cardio"
    STRENGTH = "Strength"
    FLEXIBILITY = "Flexibility"
    # HIGH_INTENSITY = "High Intensity"
    HIGH_INTENSITY = "High Intensity Interval"
    # GROUP_FITNESS = "Group_Fitness"
    GROUP_FITNESS = "Group Fitness Class"
    OTHER = "Other"

    def __str__(self):
        return str(self.value)
