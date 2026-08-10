from unittest import TestCase
from datetime import date
from models.Owner import Owner   # adjust import as needed


class TestOwner(TestCase):

    def setUp(self):
        self.owner = Owner(
            first_name="John",
            last_name="Doe",
            street_address="123 Main St",
            city="Omaha",
            state="NE",
            zipcode="68102",
            dob=date(1990, 5, 15)
        )

    def test_full_name(self):
        self.assertEqual(self.owner.full_name, "John Doe")

    def test_address_format(self):
        expected = "123 Main St\nOmaha, NE 68102"
        self.assertEqual(self.owner.address, expected)

    def test_getters(self):
        self.assertEqual(self.owner.first_name, "John")
        self.assertEqual(self.owner.last_name, "Doe")
        self.assertEqual(self.owner.street_address, "123 Main St")
        self.assertEqual(self.owner.city, "Omaha")
        self.assertEqual(self.owner.state, "NE")
        self.assertEqual(self.owner.zipcode, "68102")
        self.assertEqual(self.owner.date_of_birth, date(1990, 5, 15))

    def test_setters(self):
        self.owner.first_name = "Jane"
        self.owner.last_name = "Smith"
        self.owner.street_address = "999 New Rd"
        self.owner.city = "Lincoln"
        self.owner.state = "NE"
        self.owner.zipcode = "68508"
        self.owner.date_of_birth = date(2000, 1, 1)

        self.assertEqual(self.owner.first_name, "Jane")
        self.assertEqual(self.owner.last_name, "Smith")
        self.assertEqual(self.owner.street_address, "999 New Rd")
        self.assertEqual(self.owner.city, "Lincoln")
        self.assertEqual(self.owner.state, "NE")
        self.assertEqual(self.owner.zipcode, "68508")
        self.assertEqual(self.owner.date_of_birth, date(2000, 1, 1))

    def test_equality_true(self):
        o2 = Owner(
            "John", "Doe", "123 Main St", "Omaha", "NE", "68102",
            date(1990, 5, 15)
        )
        self.assertEqual(self.owner, o2)

    def test_equality_false(self):
        o2 = Owner(
            "Alice", "Doe", "123 Main St", "Omaha", "NE", "68102",
            date(1990, 5, 15)
        )
        self.assertNotEqual(self.owner, o2)

    def test_str_output_contains_name_and_address(self):
        s = str(self.owner)
        self.assertIn("Owner Name: John Doe", s)
        self.assertIn("123 Main St", s)
        self.assertIn("Omaha, NE 68102", s)