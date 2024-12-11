from fastapi import Request, HTTPException
from exceptions.custom_exceptions import InvalidDateRangeError
from exceptions.custom_exceptions import APIValidationError
from exceptions.custom_exceptions import ServiceValidationError
from exceptions.custom_exceptions import EmptyDataError
from config.logger import get_logger

logger = get_logger()

async def invalid_date_range_error_handler(
    request: Request, exc: InvalidDateRangeError
):
    logger.error(f"Invalid date range error: {exc}")
    raise HTTPException(status_code=400, detail=str(exc))


async def empty_data_error_handler(request: Request, exc: EmptyDataError):
    logger.error(f"Empty data error: {exc}")
    raise HTTPException(status_code=500, detail=str(exc))


async def service_validation_error_handler(
    request: Request, exc: ServiceValidationError
):
    logger.error(f"Validation error in service: {exc}")
    raise HTTPException(status_code=500, detail=exc["msg"])


async def api_validation_error_handler(request: Request, exc: APIValidationError):
    logger.error(f"Validation error in request: {exc}")
    for exc in exc.errors:
        if exc["type"] == "value_error.missing":
            raise HTTPException(
                status_code=422,
                detail=f"Missing required field(s): {' and '.join(exc["loc"])}.",
            )
        elif exc["type"] == "value_error.extra":
            raise HTTPException(
                status_code=422,
                detail=f"Unexpected field(s): {' and '.join(exc["loc"])} found in the request body.",
            )
        else:
            raise HTTPException(status_code=422, detail=exc["msg"])

# Register the exception handlers
def register_exception_handlers(app):
    app.add_exception_handler(InvalidDateRangeError, invalid_date_range_error_handler)
    app.add_exception_handler(EmptyDataError, empty_data_error_handler)
    app.add_exception_handler(APIValidationError, api_validation_error_handler)
    app.add_exception_handler(ServiceValidationError, service_validation_error_handler)