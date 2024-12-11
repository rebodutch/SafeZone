from pydantic import BaseModel, Field, model_validator
import datetime
from exceptions.custom_exceptions import InvalidDateRangeError


class IntervalValidator(BaseModel):
    start_date: datetime.date = Field(
        ..., description="Invalid date format. Expected 'YYYY-MM-DD'."
    )
    end_date: datetime.date = Field(
        ..., description="Invalid date format. Expected 'YYYY-MM-DD'."
    )

    @model_validator(mode="after")
    def validate_dates(cls, values):
        start_date = values.start_date
        end_date = values.end_date
        if end_date < start_date:
            raise InvalidDateRangeError()
        return values


class DailyValidator(BaseModel):
    date: datetime.date = Field(
        ..., description="Invalid date format. Expected 'YYYY-MM-DD'."
    )



