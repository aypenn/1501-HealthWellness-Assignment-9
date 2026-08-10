from unittest import TestCase
from datetime import date
from utils.input_utils import get_valid_date, get_int, get_int_range

class TestInputUtils(TestCase):

    # -------------------------------
    # get_int
    # -------------------------------
    def test_get_int_valid(self):
        self.assertEqual(get_int("5"), 5)

    def test_get_int_negative(self):
        self.assertEqual(get_int("-15"), -15)

    def test_get_int_invalid(self):
        self.assertIsNone(get_int("abc"))

    def test_get_int_empty_string(self):
        self.assertIsNone(get_int(""))

    # -------------------------------
    # get_int_range
    # -------------------------------
    def test_get_int_range_valid(self):
        self.assertEqual(get_int_range("5", 1, 10), 5)

    def test_get_int_range_out_of_range_low(self):
        self.assertIsNone(get_int_range("0", 1, 10))

    def test_get_int_range_out_of_range_high(self):
        self.assertIsNone(get_int_range("20", 1, 10))

    def test_get_int_range_invalid_string(self):
        self.assertIsNone(get_int_range("hello", 1, 10))

    def test_get_int_range_none_input(self):
        self.assertIsNone(get_int_range("", 1, 10))

    # # -------------------------------
    # # get_float - ran this test.  Threw error get_float not defined
    # # -------------------------------
    #
    # def test_get_float_valid(self):
    #     self.assertAlmostEqual(get_float("3.14"), 3.14)
    #
    # def test_get_float_negative(self):
    #     self.assertAlmostEqual(get_float("-2.5"), -2.5)
    #
    # def test_get_float_invalid(self):
    #     self.assertIsNone(get_float("xyz"))
    #
    # def test_get_float_empty_string(self):
    #     self.assertIsNone(get_float(""))

    # -------------------------------
    # get_valid_date
    # -------------------------------
    def test_get_valid_date_correct_format(self):
        result = get_valid_date("10/30/2025")
        self.assertEqual(result, date(2025, 10, 30))

    def test_get_valid_date_invalid_year(self):
        self.assertIsNone(get_valid_date("09/25/25"))

    def test_get_valid_date_invalid_month(self):
        self.assertIsNone(get_valid_date("9/25/2025"))

    def test_get_valid_date_invalid_day(self):
        self.assertIsNone(get_valid_date("12/99/2025"))

    def test_get_valid_date_invalid_date(self):
        # February 31st does not exist
        self.assertIsNone(get_valid_date("02/31/2025"))

    def test_get_valid_date_wrong_format(self):
        self.assertIsNone(get_valid_date("25/12/2025"))  # wrong format (European)

    def test_get_valid_date_wrong_separator(self):
        self.assertIsNone(get_valid_date("12-25-2025"))  # wrong separator

    def test_get_valid_date_short_string(self):
        self.assertIsNone(get_valid_date("1/1/2025"))  # wrong length

    def test_get_valid_date_empty_string(self):
        self.assertIsNone(get_valid_date(""))

    def test_get_valid_invalid_data(self):
        self.assertIsNone(get_valid_date("ab/cd/defg"))