import datetime
from typing import Optional
from pydantic import BaseModel, Field # type: ignore

# request data models
class SimulateModel(BaseModel):
    date: datetime.date = Field(..., description="Invalid date format. Expected 'YYYY-MM-DD'.")
    end_date: Optional[datetime.date] = Field(None, description="Invalid date format. Expected 'YYYY-MM-DD'.")

class VerifyModel(BaseModel):
    date: datetime.date = Field(..., description="Invalid date format. Expected 'YYYY-MM-DD'.")
    interval: int = Field(1, description="Invalid interval format. Expected integer.")
    city: Optional[str] = Field(None, description="The length of city name is between 1 to 50.")
    region: Optional[str] = Field(None, description="The length of region name is between 1 to 50.")
    ratio: bool = Field(False, description="The data is ratio of population or not.")

class SetTimeModel(BaseModel):
    mock_time: Optional[str] = Field(None, description="Invalid date format. Expected 'YYYY-MM-DD'.")
    accelerate: Optional[int] = Field(None, description="Invalid accelerate format. Expected integer.")
    # 0: no acceleration, 1: 1x, 2: 2x, 3: 3x, etc.

class HealthModel(BaseModel):
    target: Optional[str] = Field(None, description="Component (db, redis, mkdoc)")
    all: bool = Field(False, description="Check all components")

class InitdbModel(BaseModel):
    pass

class CleardbModel(BaseModel):
    pass

class ResetdbModel(BaseModel):
    pass