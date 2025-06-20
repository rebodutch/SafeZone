from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions.custom import InvalidTaiwanCityException, InvalidTaiwanRegionException
from config.logger import get_logger
from api.schemas import APIResponse

logger = get_logger()


def invalid_taiwan_city_handler(request: Request, exc: InvalidTaiwanCityException):
    logger.error(f"Invalid city name: {exc}")

    response = APIResponse(
        success=False,
        message="Invalid city name.",
        errors={"fields": ["city"], "detail": str(exc)},
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
        errors={"fields": ["city", "region"], "detail": str(exc)},
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
        errors={"detail": "An unexpected error occurred. Please contact support."},
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
