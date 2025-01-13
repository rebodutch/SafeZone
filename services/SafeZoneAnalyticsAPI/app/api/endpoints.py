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


@router.get("/cases/region", response_model=APIResponse)
async def process_data(params: RegionParameters = Depends()):
    end_date = params.now
    start_date = end_date - timedelta(days=int(params.interval))

    logger.info(
        f"Received request to query aggregated data for date {start_date} ~ {end_date}"
    )
    query_params = {
        "start_date": start_date,
        "end_date": end_date,
        "city": params.city,
        "region": params.region,
        "ratio": False if not params.ratio else True,
    }

    query_result = handle_query_request(query_params)

    logger.debug(f"Query result: {query_result}")

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
    start_date = end_date - timedelta(days=int(params.interval))

    logger.info(
        f"Received request to query aggregated data for date {start_date} ~ {end_date}"
    )

    query_params = {
        "start_date": start_date,
        "end_date": end_date,
        "city": params.city,
        "ratio": False if not params.ratio else True,
    }

    query_result = handle_query_request(query_params)

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
    start_date = end_date - timedelta(days=int(params.interval))

    logger.info(
        f"Received request to query aggregated data for date {start_date} ~ {end_date}"
    )

    query_params = {"start_date": start_date, "end_date": end_date}

    query_result = handle_query_request(query_params)

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
