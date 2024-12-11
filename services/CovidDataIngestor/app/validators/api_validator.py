from pydantic import BaseModel, Field
import datetime

class CollectValidator(BaseModel):
    date: datetime.date = Field(..., description="Invalid date format. Expected 'YYYY-MM-DD'.")
    city: str = Field(..., min_length=1, max_length=50, description="The length of city name is between 1 to 50.")
    region: str = Field(..., min_length=1, max_length=50, description="The length of region name is between 1 to 50.")
    cases: int = Field(..., ge=0, description="'cases' must be a positive integer.")
    
    model_config = {"extra": "forbid"}