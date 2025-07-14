import logging

from fastapi import FastAPI, Request  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore

from utils.pydantic_model.response import APIResponse, ErrorModel
from exceptions.custom import InvalidTaiwanCityException, InvalidTaiwanRegionException

logger = logging.getLogger(__name__)


def invalid_taiwan_city_handler(request: Request, exc: InvalidTaiwanCityException):
    logger.error(f"Invalid city name: {exc}")

    response = APIResponse(
        success=False,
        message="Invalid city name.",
        errors=ErrorModel(
            field="city",
            summary="Invalid city name",
            detail=str(exc),
        ),
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=422,
    )


def invalid_taiwan_region_handler(request: Request, exc: InvalidTaiwanRegionException):
    logger.error(f"Internal region name: {exc}")

    response = APIResponse(
        success=False,
        message="Invalid region name.",
        errors=ErrorModel(
            field="region",
            summary="Invalid region name",
            detail=str(exc),
        ),
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=422,
    )


def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal server error: {exc}")

    response = APIResponse(
        success=False,
        message="Internal server error.",
        errors=ErrorModel(
            field="unknown",
            summary="Unexpected error occurred during processing.",
            detail=str(exc),
        ),
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=500,
    )


# Register the exception handlers
def register_exception_handlers(app: FastAPI):
    # in service exception handlers
    app.add_exception_handler(InvalidTaiwanCityException, invalid_taiwan_city_handler)
    app.add_exception_handler(
        InvalidTaiwanRegionException, invalid_taiwan_region_handler
    )
    # request to database exception handlers
    # global exception handler
    app.add_exception_handler(Exception, global_exception_handler)
