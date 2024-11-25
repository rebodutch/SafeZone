# common/custom_exceptions/exceptions.py

# covid_case data validation exceptions
class InvalidTaiwanCityException(Exception):
    def __init__(self, message="Invalid city name. Expected it is a Taiwan city."):
        super().__init__(message)


class InvalidTaiwanRegionException(Exception):
    def __init__(
        self, message="Invalid region name. Expected it is a region in Taiwan."
    ):
        super().__init__(message)

class InvalidCasesNumberException(Exception):
    def __init__(self, message="'cases' must be a positive integer."):
        super().__init__(message)


class MissingDataException(Exception):
    def __init__(
        self, message="Missing data. Expected 'date', 'cases', 'city', and 'region'."
    ):
        super().__init__(message)

class InvalidDateFormatException(Exception):
    def __init__(self, message="Invalid date format. Expected 'YYYY-MM-DD'."):
        super().__init__(message)

class ExtraFieldException(Exception):
    def __init__(
        self, message='Unexpected field "extra_field" found in the request body.'
    ):
        super().__init__(message)


class InvalidContentTypeException(Exception):
    def __init__(self, message="Invalid Content-Type. Expected 'application/json'."):
        super().__init__(message)

# service :covid_data_simulator exceptions
class EmptyDataException(Exception):
    def __init__(self, message="No data available for the given date(s)."):
        super().__init__(message)

class InvalidDateRangeException(Exception):
    def __init__(self, message="Invalid date range. 'start_date' must be before 'end_date'."):
        super().__init__(message)


# the api side exceptions be tranlated by any service side exceptions

