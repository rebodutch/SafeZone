# app/api/endpoints.py
import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, Request  # type: ignore

from utils.pydantic_model.request import (
    RegionParameters,
    CityParameters,
    NationalParameters,
)
from utils.pydantic_model.response import (
    AnalyticsAPIData,
    AnalyticsAPIResponse,
    HealthResponse,
)
from pipeline.orchestrator import handle_query_request
from config.cache import redis_cache  # decorator for caching


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(success=True, message="Service is healthy.", status="healthy")


@router.get("/cases/region", response_model=AnalyticsAPIResponse)
@redis_cache(endpoint="cases_region", ttl=86400)  # Cache for 1 day
async def process_data(request: Request, params: RegionParameters = Depends()):
    """
    Endpoint to process region-level data requests.
    """
    end_date = params.now
    start_date = end_date - timedelta(days=int(params.interval) - 1)

    query_params = {
        # Parameters for querying data
        "start_date": start_date,
        "end_date": end_date,
        "city": params.city,
        "region": params.region,
        "ratio": False if not params.ratio else True,
    }
    logger.info(
        f"Received region-level request to query data with params {query_params}.",
        extra={"event": "query_region_cases"},
    )

    query_result = handle_query_request(request, query_params)

    logger.info(
        f"Query region-level result: {query_result}",
        extra={"event": "query_region_cases"},
    )

    return AnalyticsAPIResponse(
        success=True,
        message="Data returned successfully",
        detail=f"Data returned successfully for dates {query_result["start_date"]} ~ {query_result["end_date"]}.",
        data=AnalyticsAPIData(**query_result),
    )


@router.get("/cases/city", response_model=AnalyticsAPIResponse)
@redis_cache(endpoint="cases_city", ttl=86400)  # Cache for 1 day
async def process_data(request: Request, params: CityParameters = Depends()):
    end_date = params.now
    start_date = end_date - timedelta(days=int(params.interval) - 1)

    query_params = {
        # Parameters for querying data
        "start_date": start_date,
        "end_date": end_date,
        "city": params.city,
        "ratio": False if not params.ratio else True,
    }

    logger.info(
        f"Received city-level request to query data with params {query_params}.",
        extra={"event": "query_city_cases"},
    )

    query_result = handle_query_request(request, query_params)

    logger.info(
        f"Query city-level result: {query_result}", extra={"event": "query_city_cases"}
    )

    return AnalyticsAPIResponse(
        success=True,
        message="Data returned successfully",
        detail=f"Data returned successfully for dates {query_result['start_date']} ~ {query_result['end_date']}.",
        data=AnalyticsAPIData(**query_result),
    )


@router.get("/cases/national", response_model=AnalyticsAPIResponse)
@redis_cache(endpoint="cases_national", ttl=86400)  # Cache for 1 day
async def process_data(request: Request, params: NationalParameters = Depends()):
    end_date = params.now
    start_date = end_date - timedelta(days=int(params.interval) - 1)

    query_params = {
        # Parameters for querying data
        "start_date": start_date,
        "end_date": end_date,
    }

    logger.info(
        f"Received national-level request to query data with params {query_params}.",
        extra={"event": "query_national_cases"},
    )

    query_result = handle_query_request(request, query_params)

    logger.info(
        f"Query national-level result: {query_result}",
        extra={"event": "query_national_cases"},
    )

    return AnalyticsAPIResponse(
        success=True,
        message="Data returned successfully",
        detail=f"Data returned successfully for dates {query_result['start_date']} ~ {query_result['end_date']}.",
        data=AnalyticsAPIData(**query_result),
    )
