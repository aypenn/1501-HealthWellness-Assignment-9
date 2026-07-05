from datetime import date


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