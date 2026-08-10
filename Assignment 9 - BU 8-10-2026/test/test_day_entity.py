from unittest import TestCase
from datetime import date
from datetime import datetime
from models.CalorieEntity import *
from unittest.mock import patch
import unittest
from dataclasses import dataclass

from models.DayEntity import DayEntity

d_equal1: DayEntity = DayEntity(date(2026, 5, 1))
d_equal1.add_meal(Meal("cereal", "Breakfast", 500))
d_equal1.add_workout(Workout("Yoga", "Flexibility", 300))

d_equal2: DayEntity = DayEntity(date(2026, 5, 1))
d_equal2.add_meal(Meal("cereal", "Breakfast", 500))
d_equal2.add_workout(Workout("Yoga", "Flexibility", 300))

d_not_equal1: DayEntity = DayEntity(date(2026, 5, 2))
d_not_equal1.add_meal(Meal("cereal", "Breakfast", 500))
d_not_equal1.add_workout(Workout("Yoga", "Flexibility", 300))

d_not_equal2: DayEntity = DayEntity(date(2026, 5, 1))
d_not_equal2.add_meal(Meal("cereal", "Lunch", 500))
d_not_equal2.add_workout(Workout("Yoga", "Flexibility", 300))

d_not_equal3: DayEntity = DayEntity(date(2026, 5, 1))
d_not_equal3.add_meal(Meal("cereal", "Breakfast", 500))
d_not_equal3.add_workout(Workout("Pilates", "Flexibility", 300))



class TestDayEntity(TestCase):

    def setUp(self):
        self.day_entity = DayEntity(date(2026, 5, 1))
        self.day_entity.add_meal(Meal("cereal", "Breakfast", 500))
        self.day_entity.add_workout(Workout("Yoga", "Flexibility", 300))


    def test_net_calories(self):
        self.assertEqual(self.day_entity.net_calories() , 200)

    def test_equals_calories(self):
        # issue
        d: DayEntity = DayEntity(date(2026, 5, 1))
        self.assertEqual(d.meal_calories, 0)
        self.assertEqual(d.workout_calories, 0)
        self.assertEqual(d.net_calories(), 0)

        # self.assertEqual(self.meal_calories(), 0)
        # self.assertEqual(self.day_entity.workout_calories, 0)
        # self.assertEqual(self.day_entity.net_calories(), 0)


    def test_str(self):
        output_string = self.day_entity.__str__()
        assert "Meals:" in output_string
        assert "Workouts:" in output_string
        assert "Net Calories:" in output_string

    def test_equals_entity(self):

        # d1_date = d_equal1.entry_date
        # string_date = d1_date.strftime("%Y-%m-%d")
        # print("d_equal1.entry_date = ", d1_date)

        self.assertEqual(self.day_entity, d_equal1)


    def test_not_equals_entity(self):
        # issue
        self.assertNotEqual(self.day_entity, d_not_equal1)
        self.assertNotEqual(self.day_entity, d_not_equal2)
        self.assertNotEqual(self.day_entity, d_not_equal3)

    # def test_not_equals(self):
    #     d_not_equal1: DayEntity = DayEntity(date(2026, 5, 2))
    #     # d_not_equal1.entry_date = date(2026, 5, 2)
    #     d_not_equal1.add_meal(Meal("cereal", "Breakfast", 500))
    #     d_not_equal1.add_workout(Workout("Yoga", "Flexibility", 300))
    #
    #     self.assertNotEqual(self, d_not_equal1)


class TestObjects(unittest.TestCase):

    def test_list_equality(self):
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]

        self.assertEqual(list1, list2)

    def test_meals_equal(self):

        m1 = Meal("cereal", "Breakfast", 500)
        m2 = Meal("cereal", "Breakfast", 500)

        # self.assertEqual(m1, m2)
        assert m1 == m2

    def test_meals_equal2(self):

        ml1 = []
        ml2 = []

        m1a = Meal("cereal", "Breakfast", 300)
        m1b = Meal("sandwich", "Lunch", 500)
        m2a = Meal("cereal", "Breakfast", 300)
        m2b = Meal("sandwich", "Lunch", 500)

        ml1.append(m1a)
        ml1.append(m1b)
        ml2.append(m2a)
        ml2.append(m2b)


        self.assertEqual(ml1, ml2)
        # assert ml1  == ml2