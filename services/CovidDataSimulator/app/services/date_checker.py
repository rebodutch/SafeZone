# app/services/date_checker.py
from datetime import datetime
from common.custom_exceptions.exceptions import InvalidDateFormatException, InvalidDateRangeException

def check_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as e:
        raise InvalidDateFormatException

def check_interval(start_date, end_date):
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    if start_date_obj > end_date_obj:
        raise InvalidDateRangeException