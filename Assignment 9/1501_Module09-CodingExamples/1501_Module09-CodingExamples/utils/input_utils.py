
from datetime import date

def get_valid_date(date_str : str) -> date:
    valid_date = None
    if len(date_str) == 10 and date_str[2] == "-" and date_str[5] == "-":
        # break up the date and parse
        split_date = date_str.split("-")
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

def get_int(num) -> int | None:
    try:
        return int(num)
    except ValueError:
        return None

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

def get_float(num) -> float | None:
    try:
        return float(num)
    except ValueError:
        return None