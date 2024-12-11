from fastapi import HTTPException, Request
from exceptions.custom_exceptions import (
    APIValidationError,
    DataDuplicateException,
    InvalidTaiwanCityException,
    InvalidTaiwanRegionException,
    InvalidContentTypeException,
)
from config.logger import get_logger

logger = get_logger()


async def api_validation_error_handler(request: Request, exc: APIValidationError):
    logger.error(f"Validation error in request: {exc}")
    for error in exc.errors:
        print(error)
        if error["type"] == "missing":
            raise HTTPException(
                status_code=422,
                detail=f"Missing required field(s): {' and '.join(error["loc"])}.",
            )
        elif error["type"] == "extra_forbidden":
            raise HTTPException(
                status_code=422,
                detail=f"Unexpected field(s): {' and '.join(error["loc"])} found in the request body.",
            )
        elif error["type"] == "date_from_datetime_parsing":
            raise HTTPException(
                status_code=422,
                detail=f"Invalid date format. Expected 'YYYY-MM-DD'.",
            )
        elif error["type"] == "greater_than_equal":
            raise HTTPException(
                status_code=422,
                detail=f"'cases' must be a positive integer.",
            )
        else:
            raise HTTPException(status_code=422, detail=error["msg"])

async def data_duplicate_error_handler(request: Request, exc: DataDuplicateException):
    logger.error(f"Data duplication error: {exc}")
    raise HTTPException(status_code=409, detail=str(exc))

async def invalid_taiwan_city_error_handler(request: Request, exc: InvalidTaiwanCityException):
    logger.error(f"Invalid Taiwan city error: {exc}")
    raise HTTPException(status_code=422, detail=str(exc))

async def invalid_taiwan_region_error_handler(request: Request, exc: InvalidTaiwanRegionException):
    logger.error(f"Invalid Taiwan region error: {exc}")
    raise HTTPException(status_code=422, detail=str(exc))

async def invalid_content_type_error_handler(request: Request, exc: InvalidContentTypeException):
    logger.error(f"Invalid content type error: {exc}")
    raise HTTPException(status_code=415, detail=str(exc))

def register_exception_handlers(app):
    app.add_exception_handler(APIValidationError, api_validation_error_handler)
    app.add_exception_handler(DataDuplicateException, data_duplicate_error_handler)
    app.add_exception_handler(InvalidTaiwanCityException, invalid_taiwan_city_error_handler)
    app.add_exception_handler(InvalidTaiwanRegionException, invalid_taiwan_region_error_handler)
    app.add_exception_handler(InvalidContentTypeException, invalid_content_type_error_handler)

