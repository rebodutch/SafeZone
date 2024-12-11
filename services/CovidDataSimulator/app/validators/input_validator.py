from pydantic import BaseModel, Field, validator
import datetime
from exceptions.custom_exceptions import InvalidDateRangeError


class IntervalInput(BaseModel):
    start_date: datetime.date = Field(
        ..., description="Invalid date format. Expected 'YYYY-MM-DD'."
    )
    end_date: datetime.date = Field(
        ..., description="Invalid date format. Expected 'YYYY-MM-DD'."
    )

    @validator("end_date")
    def validate_dates(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date < start_date:
            raise InvalidDateRangeError()
        return end_date


class DateInput(BaseModel):
    date: datetime.date = Field(
        ..., description="Invalid date format. Expected 'YYYY-MM-DD'."
    )



