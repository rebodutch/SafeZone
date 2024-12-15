import datetime
from typing import Optional
from pydantic import BaseModel, Field

# request data models
class CollectData(BaseModel):
    date: datetime.date = Field(..., description="Invalid date format. Expected 'YYYY-MM-DD'.")
    city: str = Field(..., min_length=1, max_length=50, description="The length of city name is between 1 to 50.")
    region: str = Field(..., min_length=1, max_length=50, description="The length of region name is between 1 to 50.")
    cases: int = Field(..., ge=1, description="'cases' must be a positive integer.")


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
