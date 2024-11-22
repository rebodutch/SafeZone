# app/api/endpoints.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.request_handler import handle_daily_request, handle_interval_request
from services.exception_handler import handle_exceptions
import traceback
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
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {e}")
        print("Traceback:")
        traceback.print_exc()
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
