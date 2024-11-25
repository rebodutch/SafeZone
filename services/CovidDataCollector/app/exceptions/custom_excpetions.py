# app/exceptions/custom_exceptions.py


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


class InvalidDataFormatException(Exception):
    def __init__(
        self,
        message="Invalid field type. 'date' should be in the form 'YYYY-MM-DD', 'city' and 'region' should be strings, and 'cases' should be an integer.",
    ):
        super().__init__(message)


class ExtraFieldException(Exception):
    def __init__(
        self, message='Unexpected field "extra_field" found in the request body.'
    ):
        super().__init__(message)


class InvalidContentTypeException(Exception):
    def __init__(self, message="Invalid Content-Type. Expected 'application/json'."):
        super().__init__(message)
