from fastapi import APIRouter
from services import request_handler

router = APIRouter()

@router.get("/simulate/daily")
async def simulate_daily(date: str):
    return request_handler.handle_daily_request(date)

@router.get("/simulate/interval")
async def simulate_interval(start_date: str, end_date: str):
    return request_handler.handle_interval_request(start_date, end_date)