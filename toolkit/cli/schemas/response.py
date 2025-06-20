from datetime import datetime, timezone
from typing import Generic, TypeVar, Optional

from pydantic import BaseModel, Field # type: ignore

# --- data models  --- #
class VerifyDataModel(BaseModel):
    start_date: str = Field(
        ..., description="Invalid date format. Expected 'YYYY-MM-DD'."
    )
    end_date: str = Field(
        ..., description="Invalid date format. Expected 'YYYY-MM-DD'."
    )
    city: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="The length of city name is between 1 to 50.",
    )
    region: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="The length of region name is between 1 to 50.",
    )
    aggregated_cases: Optional[int] = Field(
        None, ge=0, description="'cases' must be a positive integer."
    )
    cases_population_ratio: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="'cases_population_ratio' must be a float between 0 and 1.",
    )


# --- response model --- #
class ErrorModel(BaseModel):
    fields: Optional[str] = Field(
        None, description="Short message describing the status."
    )
    detail: str = Field(..., description="Detailed explanation of the message.")


class APIResponse(BaseModel):
    success: bool = Field(..., description="State of the response.")
    message: str = Field(..., description="Short message describing the status.")
    errors: Optional[ErrorModel] = Field(None, description="Error detail.")
    # timestamp automatically generated with current UTC time in ISO 8601 format
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        description="UTC timestamp of response generation"
    )

class VerifyResponseModel(APIResponse):
    data: VerifyDataModel = Field(
        ..., description="Data field containing verification results."
    )


