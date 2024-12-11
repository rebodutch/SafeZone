from pydantic import ValidationError

class APIValidationError(Exception):
   def __init__(self, exc: ValidationError):
        self.errors = exc.errors()
        super().__init__(f"a validation error occurred in the API")

class ServiceValidationError(Exception):
   def __init__(self, original_error: ValidationError):
        self.errors = original_error.json(indent=2)
        super().__init__(f"a validation error occurred in the Service")

class InvalidDateRangeError(Exception):
    def __init__(
        self, message="Invalid date range. 'start_date' must be before 'end_date'."
    ):
        super().__init__(message)

class EmptyDataError(Exception):
    def __init__(self, message="No data available for the given date(s)."):
        super().__init__(message)