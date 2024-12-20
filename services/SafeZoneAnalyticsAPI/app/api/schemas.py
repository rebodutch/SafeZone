from pydantic import BaseModel, Field, validator
from typing import Optional, Literal, List
import datetime

# query parameter models
class NationalParameters(BaseModel):
    now: datetime.date = Field(..., description="Date in 'YYYY-MM-DD' format.")
    interval: Literal["1", "3", "7", "14", "30"] = Field(..., description="the aggergate data form number of days before now")


class CityParameters(NationalParameters):
    city: str = Field(..., min_length=1, max_length=50, description="The length of city name is between 1 to 50.")
  
class RegionParameters(CityParameters):  
    region: str = Field(..., min_length=1, max_length=50, description="The length of region name is between 1 to 50.")
    ratio: Optional[bool] = Field(False, description="Whether to include cases/population ratio in the response.")

# response models
class DataDetail(BaseModel):
    start_date: str = Field(..., description="Invalid date format. Expected 'YYYY-MM-DD'.")
    end_date: str = Field(..., description="Invalid date format. Expected 'YYYY-MM-DD'.")
    city: Optional[str] = Field(None, min_length=1, max_length=50, description="The length of city name is between 1 to 50.")
    region: Optional[str] = Field(None, min_length=1, max_length=50, description="The length of region name is between 1 to 50.")
    aggregated_cases: Optional[int] = Field(None, ge=0, description="'cases' must be a positive integer.")
    cases_population_ratio: Optional[float] = Field(None, ge=0, le=1, description="'cases_population_ratio' must be a float between 0 and 1.")


class ErrorDetail(BaseModel):
    fields: Optional[List] = Field(
        None, description="Short message describing the status."
    )
    detail: str = Field(..., description="Detailed explanation of the message.")


class APIResponse(BaseModel):
    success: bool = Field(..., description="State of the response.")
    message: str = Field(..., description="Short message describing the status.")
    detail: Optional[str] = Field(None, description="Detailed explanation of the message.")
    data: Optional[DataDetail] = Field(None, description="Data details.")
    errors: Optional[ErrorDetail] = Field(None, description="Error details.")
