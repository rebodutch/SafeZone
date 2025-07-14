# app/api/endpoints.py
import logging

from fastapi import APIRouter, Depends # type: ignore

from utils.pydantic_model.request import DailyParameters, IntervalParameters
from utils.pydantic_model.response import APIResponse, HealthResponse
from pipeline.orchestrator import handle_request


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    return HealthResponse(
        success=True,
        message="API is running",
        data={"detail": "The API is running smoothly."},
    )


@router.get("/simulate/daily", response_model=APIResponse)
async def process_data(params: DailyParameters = Depends()):
    date = params.date.strftime("%Y-%m-%d")

    logger.info(f"Received request to simulate {date} data.")

    await handle_request(date)

    logger.info("Data simulation request handle success.")

    return APIResponse(
        success=True,
        message="Data sent successfully",
        detail=f"Data sent successfully for date {date}.",
    )


@router.get("/simulate/interval", response_model=APIResponse)
async def simulate_interval(params: IntervalParameters = Depends()):
    start_date = params.start_date.strftime("%Y-%m-%d")
    end_date = params.end_date.strftime("%Y-%m-%d")

    logger.info(
        f"Received request to simulate interval data for dates {start_date} ~ {end_date}."
    )

    await handle_request(start_date, end_date)

    logger.info("Data simulation request handle success.")

    return APIResponse(
        success=True,
        message="Data sent successfully",
        detail=f"Data sent successfully for dates {start_date} ~ {end_date}.",
    )
