# app/api/endpoints.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.pipeline import handle_daily_request, handle_interval_request
from utils.custom_exceptions.handler import handle_exceptions

router = APIRouter()


@router.get("/simulate/daily")
async def simulate_daily(date: str):
    try:
        handle_daily_request(date)
        response = {
            "status": "success",
            "message": f"Data sent successfully for date {date}",
        }
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return handle_exceptions(e)


@router.get("/simulate/interval")
async def simulate_interval(start_date: str, end_date: str):
    try:
        handle_interval_request(start_date, end_date)
        response = {
            "status": "success",
            "message": f"Data sent successfully for dates {start_date} ~ {end_date}",
        }
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return handle_exceptions(e)
