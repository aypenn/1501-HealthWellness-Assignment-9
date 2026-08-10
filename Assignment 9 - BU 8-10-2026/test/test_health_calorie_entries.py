from unittest import TestCase
from datetime import date
from unittest.mock import patch

from models.CalorieEntity import *

class M:
    Meal = Meal("cereal", "Breakfast", -500)

class W:
    Workout = Workout("Yoga", "Flexibility", 300)

meal_type_list = list(item.value for item in MealType)
workout_type_list = list(item.value for item in WorkoutType)

class TestCalorieEntity(TestCase):

    def setUp(self):
        self.Meal = Meal("cereal", "Breakfast", 300)
        self.Workout = Workout("Yoga", "Flexibility", 300)

    def test_meal_setter_positive_calories(self):
        self.Meal.calories = 500
        self.assertEqual(self.Meal.calories, 500)

    def test_meal_setter_negative_calories(self):
        self.Meal.calories = -500
        self.assertEqual(self.Meal.calories, -500)

    def test_meal_setter_type(self):
        self.Meal.meal_type = "Lunch"
        self.assertEqual(self.Meal.meal_type, "Lunch")

    def test_meal_getter_type(self):
        self.assertEqual(self.Meal.entry_type(), "Breakfast")

    def test_meal_type_valid(self):
        self.assertIn(self.Meal.entry_type(), meal_type_list)

    def test_meal_type_not_valid(self):
        self.Meal.entry_type_set("Null")
        self.assertNotIn(self.Meal.entry_type(), meal_type_list)

    def test_workout_setter_positive_calories(self):
        self.Workout.calories = 500
        self.assertEqual(self.Workout.calories, 500)

    def test_workout_setter_negative_calories(self):
        self.Workout.calories = -500
        self.assertEqual(self.Workout.calories, -500)

    def test_workout_setter_type(self):
        self.Workout.workout_type = "High_Intensity"
        self.assertEqual(self.Workout.workout_type, "High_Intensity")

    def test_workout_getter_type(self):
        self.assertEqual(self.Workout.entry_type(), "Flexibility")

    def test_workout_type_valid(self):
        self.assertIn(self.Workout.entry_type(), workout_type_list)

    def test_workout_type_not_valid(self):
        self.Workout.entry_type_set("Null")
        self.assertNotIn(self.Workout.entry_type(), meal_type_list)

class TestCalorieEntityConstructorPosValues(TestCalorieEntity):

    def setUp(self):
        self.Meal = Meal("cereal", "Breakfast", 500)
        self.Workout = Workout("Yoga", "Flexibility", 300)
        # m  = Meal("cereal", "Breakfast", -500)
        # self.Meal = None
        # self.Workout = None

    def test_meal_constructor_positive_calories(self):
        self.assertEqual(self.Meal.calories(), 500)

    # @patch.object("self.Meal","calories", -500)
    # def test_meal_constructor_negative_calories(self):
    #     # with patch("M.calories", new=-500):
    #     # with patch.object(self,"calories", -500):
    #     self.assertEqual(self.Meal.calories(), -500)

    # @patch('module_name.Meal.calories', new=-500)
    # def test_meal_constructor_negative_calories(self):
    #     self.assertEqual(self.Meal.calories(), -500)

    # # @patch.object(M,"calories", -500)
    # def test_meal_constructor_negative_calories(self):
    #     # with patch("M.calories", new=-500):
    #     with patch.object(M,"calories", -500):
    #         self.assertEqual(M.Meal.calories(), -500)

    def test_workout_constructor_positive_calories(self):
        self.assertEqual(self.Workout.calories(), 300)


class TestCalorieEntityConstructorNegValues(TestCalorieEntity):

    def setUp(self):
        self.Meal = Meal("cereal", "Breakfast", -500)
        self.Workout = Workout("Yoga", "Flexibility", -500)

    def test_meal_constructor_negative_calories(self):
        self.assertEqual(self.Meal.calories(), -500)

    def test_workout_constructor_negative_calories(self):
        self.assertEqual(self.Workout.calories(), -500)

