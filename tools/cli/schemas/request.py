import datetime
from typing import Optional
from pydantic import BaseModel, Field

# request data models
class SimulateModel(BaseModel):
    date: datetime.date = Field(..., description="Invalid date format. Expected 'YYYY-MM-DD'.")
    end_date: Optional[datetime.date] = Field(None, description="Invalid date format. Expected 'YYYY-MM-DD'.")
    dry_run: bool = Field(False, description="Dry run the simulation or not.")

class VerifyModel(BaseModel):
    date: datetime.date = Field(..., description="Invalid date format. Expected 'YYYY-MM-DD'.")
    interval: int = Field(..., description="Invalid interval format. Expected integer.")
    city: Optional[str] = Field(None, description="The length of city name is between 1 to 50.")
    region: Optional[str] = Field(None, description="The length of region name is between 1 to 50.")
    ratio: bool = Field(False, description="The data is ratio of population or not.")

class InitdbModel(BaseModel):
    pass

class CleardbModel(BaseModel):
    pass

class ResetdbModel(BaseModel):
    pass