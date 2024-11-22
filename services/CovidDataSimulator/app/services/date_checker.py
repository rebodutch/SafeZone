# app/services/date_checker.py
from datetime import datetime
from exception import InvalidDateFormatError, InvalidDateRangeError

def check_date(date):
    try:
        valid_date = datetime.strptime(date, "%Y-%m-%d")
        return valid_date
    except ValueError as e:
        raise InvalidDateFormatError

def check_interval(start_date, end_date):
    if start_date > end_date:
        raise InvalidDateRangeError

print(check_date('2023-11-10'))