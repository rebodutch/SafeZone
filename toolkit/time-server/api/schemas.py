import datetime
from typing import Optional
from pydantic import BaseModel, Field

# ---- Request models ---- 
class SetTimeModel(BaseModel):
    mock: bool = Field(False, description="Set to True to enable mock time mode.")
    mock_time: Optional[str] = Field(None, description="Invalid date format. Expected 'YYYY-MM-DD'.")
    accelerate: Optional[int] = Field(None, description="Invalid accelerate format. Expected integer.")

# ---- Response models ----
class APIResponse(BaseModel):
    success: bool = Field(True, description="State of the response.")
    message: str = Field(..., description="Short message describing the status.")

class ErrResponse(APIResponse):
    detail: str = Field(..., description="Detailed error message.")
    
class TimeResponse(APIResponse):
    date: datetime.date = Field(..., description="Invalid date format. Expected 'YYYY-MM-DD'.")

class StatResponse(APIResponse):
    mock: bool = Field(..., description="State of the mock time.")
    mock_time: datetime.datetime = Field(..., description="Invalid time format. Expected 'YYYY-MM-DD HH:MM:SS'.")
    launch_time: datetime.datetime = Field(..., description="Invalid time format. Expected 'YYYY-MM-DD HH:MM:SS'.")
    accelerate: int = Field(..., description="Invalid accelerate format. Expected integer.")
    mock_date: datetime.date = Field(..., description="Invalid date format. Expected 'YYYY-MM-DD'.")
    current_date: datetime.date = Field(..., description="Invalid date format. Expected 'YYYY-MM-DD'.")
