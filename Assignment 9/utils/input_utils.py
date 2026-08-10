from datetime import date
from datetime import timedelta

#takes input num and returns the integer value.  Returns None if not an int
def get_int(num) -> int | None:
    try:
        return int(num)
    except ValueError:
        return None

#determines if num is between high and low values
def get_int_range(num, low, high) -> int | None:
    value = get_int(num)
    # check if none
    if value is None:
        return None
    # if out of range
    if value < low or value > high:
        return None
    # valid int and in range
    return value

#converts date string to date
def get_valid_date(date_str : str) -> date | None:
    valid_date = None
    if len(date_str) == 10 and date_str[2] == "/" and date_str[5] == "/":
        # break up the date and parse
        split_date = date_str.split("/")
        month = get_int(split_date[0])
        day = get_int(split_date[1])
        year = get_int(split_date[2])
        if month and day and year:
            try:
                valid_date = date(year, month, day)
            except Exception:
                pass
        # build string date
        # then parse as the other

    return valid_date

 # -------------------------------
# get_valid_date
# -------------------------------
def test_get_valid_date_correct_format(self):
    result = get_valid_date("12-25-2025")
    self.assertEqual(result, date(2025, 12, 25))

def test_get_valid_date_invalid_month(self):
    self.assertIsNone(get_valid_date("99-10-2025"))

def test_get_valid_date_invalid_day(self):
    self.assertIsNone(get_valid_date("12-99-2025"))

def test_get_valid_date_invalid_date(self):
    # February 31st does not exist
    self.assertIsNone(get_valid_date("02-31-2025"))

def test_get_valid_date_wrong_format(self):
    self.assertIsNone(get_valid_date("12/25/2025"))  # wrong separator

def test_get_valid_date_short_string(self):
    self.assertIsNone(get_valid_date("1-1-2025"))  # wrong length

def test_get_valid_date_empty_string(self):
    self.assertIsNone(get_valid_date(""))


def daterange(start_date: date, end_date : date):
    print("start_date = ", start_date)
    print("end_date = ", end_date)
    # Generates dates from start_date up to (but not including) end_date
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


