import datetime
from typing import Optional
from pydantic import BaseModel, Field

# response models


class ErrorDetail(BaseModel):
    fields: Optional[str] = Field(
        None, description="Short message describing the status."
    )
    detail: str = Field(..., description="Detailed explanation of the message.")


class APIResponse(BaseModel):
    success: bool = Field(..., description="State of the response.")
    message: str = Field(..., description="Short message describing the status.")
    errors: Optional[ErrorDetail] = Field(None, description="Error details.")


class VerifyData(BaseModel):
    date: datetime.date = Field(
        ..., description="Invalid date format. Expected 'YYYY-MM-DD'."
    )
    interval: int = Field(..., description="Invalid interval format. Expected integer.")
    city: Optional[str] = Field(
        None, description="The length of city name is between 1 to 50."
    )
    region: Optional[str] = Field(
        None, description="The length of region name is between 1 to 50."
    )
    cases: Optional[int] = Field(
        None, ge=1, description="'cases' must be a positive integer."
    )
    ratio: Optional[float] = Field(
        None, description="The data is ratio of population or not."
    )


class VerifyResponse(APIResponse):
    data: VerifyData = Field(..., description="Verify Data details.")


class PhaseResponse(APIResponse):
    phase: str = Field(..., description="The current phase of the system.")
    timestamp: datetime.datetime = Field(
        ..., description="The timestamp of the phase checked."
    )
