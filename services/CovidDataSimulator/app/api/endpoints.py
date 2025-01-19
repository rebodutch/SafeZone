# app/api/endpoints.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pipeline.orchestrator import handle_daily_request, handle_interval_request
from api.schemas import (
    APIResponse,
    DailyParameters,
    IntervalParameters,
)
from config.logger import get_logger

router = APIRouter()
logger = get_logger()


@router.get("/simulate/daily", response_model=APIResponse)
async def process_data(params: DailyParameters = Depends()):
    date = params.date.strftime("%Y-%m-%d")

    logger.info(f"Received request to simulate {date} data.")

    handle_daily_request(date)

    response = APIResponse(
        success=True,
        message="Data sent successfully",
        data={"detail": f"Data sent successfully for date {date}."},
    )
    
    logger.info("Data simulation request handle success.")

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=200,
    )


@router.get("/simulate/interval", response_model=APIResponse)
async def simulate_interval(params: IntervalParameters = Depends()):
    start_date = params.start_date.strftime("%Y-%m-%d")
    end_date = params.end_date.strftime("%Y-%m-%d")

    logger.info(
        f"Received request to simulate interval data for dates {start_date} ~ {end_date}."
    )

    handle_interval_request(start_date, end_date)

    response = APIResponse(
        success=True,
        message="Data sent successfully",
        data={"detail": f"Data sent successfully for dates {start_date} ~ {end_date}."},
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=200,
    )
