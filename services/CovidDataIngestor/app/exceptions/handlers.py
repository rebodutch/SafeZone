from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.custom_exceptions import (
    DataDuplicateException,
    InvalidTaiwanCityException,
    InvalidTaiwanRegionException,
    InvalidContentTypeException,
)
from api.schemas import APIResponse
from config.logger import get_logger

logger = get_logger()


async def data_duplicate_error_handler(request: Request, exc: DataDuplicateException):
    logger.error(f"Data duplication error: {exc}.")

    response = APIResponse(
        success=False,
        message="Data duplication error.",
        errors={
            "fields": "date, city, region",
            "detail": f"Data duplication error: {exc}",
        },
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=409,
    )


async def invalid_taiwan_city_error_handler(
    request: Request, exc: InvalidTaiwanCityException
):
    logger.error(f"Invalid Taiwan city error: {exc}")

    response = APIResponse(
        success=False,
        message="Invalid Taiwan city error.",
        errors={"fields": "city", "detail": f"Invalid Taiwan city error: {exc}"},
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=422,
    )


async def invalid_taiwan_region_error_handler(
    request: Request, exc: InvalidTaiwanRegionException
):
    logger.error(f"Invalid Taiwan region error: {exc}")

    response = APIResponse(
        success=False,
        message="Invalid Taiwan region error.",
        errors={"fields": "region", "detail": f"Invalid Taiwan region error: {exc}"},
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=422,
    )


async def invalid_content_type_error_handler(
    request: Request, exc: InvalidContentTypeException
):
    logger.error(f"Invalid content type error: {exc}")

    response = APIResponse(
        success=False,
        message="Invalid content type error.",
        errors={"fields": "header", "detail": f"Invalid content type error: {exc}"},
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=415,
    )


def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal server error: {exc}")

    response = APIResponse(
        success=False,
        message="Internal server error.",
        errors={"detail": "An unexpected error occurred. Please contact support."},
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=500,
    )


def register_exception_handlers(app):
    app.add_exception_handler(DataDuplicateException, data_duplicate_error_handler)
    app.add_exception_handler(
        InvalidTaiwanCityException, invalid_taiwan_city_error_handler
    )
    app.add_exception_handler(
        InvalidTaiwanRegionException, invalid_taiwan_region_error_handler
    )
    app.add_exception_handler(
        InvalidContentTypeException, invalid_content_type_error_handler
    )
    # global exception handler
    app.add_exception_handler(Exception, global_exception_handler)
