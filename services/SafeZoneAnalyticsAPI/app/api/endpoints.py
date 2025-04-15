# app/api/endpoints.py
from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.schemas import (
    APIResponse,
    RegionParameters,
    CityParameters,
    NationalParameters,
)
from config.logger import get_logger
from pipeline.orchestrator import handle_query_request


router = APIRouter()
logger = get_logger()


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify if the API is running.
    """
    return JSONResponse(
        content={"status": "healthy"},
        status_code=200,
    )


@router.get("/cases/region", response_model=APIResponse)
async def process_data(params: RegionParameters = Depends()):
    end_date = params.now
    start_date = end_date - timedelta(days=int(params.interval) - 1)

    query_params = {
        "start_date": start_date,
        "end_date": end_date,
        "city": params.city,
        "region": params.region,
        "ratio": False if not params.ratio else True,
    }
    logger.debug(
        f"Received region-level request to query data with params {query_params}."
    )

    query_result = handle_query_request(query_params)

    logger.debug(f"Query region-level result: {query_result}")

    response = APIResponse(
        success=True,
        message="Data returned successfully",
        detail=f"Data returned successfully for dates {query_result["start_date"]} ~ {query_result["end_date"]}.",
        data=query_result,
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=200,
    )


@router.get("/cases/city", response_model=APIResponse)
async def process_data(params: CityParameters = Depends()):
    end_date = params.now
    start_date = end_date - timedelta(days=int(params.interval) - 1)

    query_params = {
        "start_date": start_date,
        "end_date": end_date,
        "city": params.city,
        "ratio": False if not params.ratio else True,
    }

    logger.debug(
        f"Received city-level request to query data with params {query_params}."
    )

    query_result = handle_query_request(query_params)

    logger.debug(f"Query city-level result: {query_result}")

    response = APIResponse(
        success=True,
        message="Data returned successfully",
        detail=f"Data returned successfully for dates {query_result["start_date"]} ~ {query_result["end_date"]}.",
        data=query_result,
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=200,
    )


@router.get("/cases/national", response_model=APIResponse)
async def process_data(params: NationalParameters = Depends()):
    end_date = params.now
    start_date = end_date - timedelta(days=int(params.interval) - 1)

    query_params = {"start_date": start_date, "end_date": end_date}

    logger.debug(
        f"Received national-level request to query data with params {query_params}."
    )

    query_result = handle_query_request(query_params)

    logger.debug(f"Query national-level result: {query_result}")

    response = APIResponse(
        success=True,
        message="Data returned successfully",
        detail=f"Data returned successfully for dates {query_result["start_date"]} ~ {query_result["end_date"]}.",
        data=query_result,
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=200,
    )
