from pydantic import BaseModel, Field, model_validator
from typing import Optional
import datetime
from exceptions.custom_exceptions import InvalidDateRangeError


# query parameter models
class IntervalParameters(BaseModel):
    start_date: datetime.date = Field(
        ..., description="Start date in 'YYYY-MM-DD' format."
    )
    end_date: datetime.date = Field(..., description="End date in 'YYYY-MM-DD' format.")

    @model_validator(mode="after")
    def validate_dates(cls, values):
        start_date = values.start_date
        end_date = values.end_date
        if end_date < start_date:
            raise InvalidDateRangeError()
        return values


class DailyParameters(BaseModel):
    date: datetime.date = Field(..., description="Date in 'YYYY-MM-DD' format.")


# response models
class DataDetail(BaseModel):
    detail: str = Field(..., description="Detailed explanation of the message.")


class ErrorDetail(BaseModel):
    fields: Optional[str] = Field(
        None, description="Short message describing the status."
    )
    detail: str = Field(..., description="Detailed explanation of the message.")


class APIResponse(BaseModel):
    success: bool = Field(..., description="State of the response.")
    message: str = Field(..., description="Short message describing the status.")
    data: Optional[DataDetail] = Field(None, description="Data details.")
    errors: Optional[ErrorDetail] = Field(None, description="Error details.")
