from pydantic import ValidationError


class APIValidationError(Exception):
    def __init__(self, exc: ValidationError):
        self.errors = exc.errors()
        super().__init__(f"a validation error occurred in the API")


class DataDuplicateException(Exception):
    def __init__(self, message="Some data are duplicate. collected failed."):
        super().__init__(message)


class InvalidTaiwanCityException(Exception):
    def __init__(self, message="Invalid city name. Expected it is a Taiwan city."):
        super().__init__(message)


class InvalidTaiwanRegionException(Exception):
    def __init__(
        self, message="Invalid region name. Expected it is a region in Taiwan."
    ):
        super().__init__(message)


class InvalidContentTypeException(Exception):
    def __init__(self, message="Invalid Content-Type. Expected 'application/json'."):
        super().__init__(message)
