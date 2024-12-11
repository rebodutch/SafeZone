# app/api/endpoints.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pipeline.orchestrator import handle_daily_request, handle_interval_request
from validators.api_validator import DailyValidator, IntervalValidator
from exceptions.custom_exceptions import APIValidationError
from config.logger import get_logger

router = APIRouter()
logger = get_logger()


@router.get("/simulate/daily")
async def simulate_daily(date: str):
    logger.info(f"Received request to simulate daily data for date {date}")
    
    try:
        DailyValidator(date=date)
    except ValidationError as e:
        raise  APIValidationError(e)
    
    handle_daily_request(date)
    response = {
        "status": "success",
        "message": f"Data sent successfully for date {date}",
    }
    return JSONResponse(content=response, status_code=200)



@router.get("/simulate/interval")
async def simulate_interval(start_date: str, end_date: str):
    logger.info(
        f"Received request to simulate interval data for dates {start_date} ~ {end_date}"
    )

    try:
        IntervalValidator(start_date=start_date, end_date=end_date)
    except ValidationError as e:
        raise APIValidationError(e)
    
    handle_interval_request(start_date, end_date)
    response = {
        "status": "success",
        "message": f"Data sent successfully for dates {start_date} ~ {end_date}",
    }
    return JSONResponse(content=response, status_code=200)
