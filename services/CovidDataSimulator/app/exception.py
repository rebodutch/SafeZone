# app/exceptions.py

class InvalidDateFormatError(Exception):
    def __init__(self, message="Invalid date format. Expected YYYY-MM-DD."):
        super().__init__(message)

class InvalidDateRangeError(Exception):
    def __init__(self, message="Start date must be earlier than or equal to end date."):
        super().__init__(message)

class EmptyDataError(Exception):
    def __init__(self, message="No data available for the given date(s)"):
        super().__init__(message)