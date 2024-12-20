from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from requests.exceptions import ReadTimeout, ConnectionError
from exceptions.custom_exceptions import InvalidDateRangeError
from exceptions.custom_exceptions import APIValidationError
from exceptions.custom_exceptions import ServiceValidationError
from exceptions.custom_exceptions import EmptyDataError
from api.schemas import APIResponse
from config.logger import get_logger

logger = get_logger()


async def invalid_date_range_error_handler(
    request: Request, exc: InvalidDateRangeError
):
    logger.error(f"Invalid date range error: {exc}")

    response = APIResponse(
        success=False,
        message="Invalid date range.",
        errors={"fields": "start_date, end_date", "detail": str(exc)},
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=400,
    )


async def empty_data_error_handler(request: Request, exc: EmptyDataError):
    logger.error(f"Empty data error: {exc}")

    response = APIResponse(
        success=False,
        message="Empty data.",
        errors={"fields": "date", "detail": str(exc)},
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=500,
    )


async def service_validation_error_handler(
    request: Request, exc: ServiceValidationError
):
    logger.error(f"Output data validation error in service: {exc}")

    response = APIResponse(
        success=False,
        message="Validation error in the service.",
        errors={"detail": str(exc)},
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=500,
    )


def read_timeout_handler(request: Request, exc: ReadTimeout):
    logger.error(f"Read timeout error: Connection to the ingestor service timed out.")

    response = APIResponse(
        success=False,
        message="connect timeout error",
        errors={"detail": f"Connection to internal service timed out."},
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=504,
    )


def connect_error_handler(request: Request, exc: ConnectionError):
    logger.error(f"Read timeout error: Connection to the ingestor service timed out.")

    response = APIResponse(
        success=False,
        message="connect failed error.",
        errors={"detail": f"Connection to internal service failed."},
    )

    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=504,
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
    app.add_exception_handler(InvalidDateRangeError, invalid_date_range_error_handler)
    app.add_exception_handler(EmptyDataError, empty_data_error_handler)
    app.add_exception_handler(ServiceValidationError, service_validation_error_handler)
    # requests exception handlers
    app.add_exception_handler(ReadTimeout, read_timeout_handler)
    app.add_exception_handler(ConnectionError, connect_error_handler)
    # global exception handler
    app.add_exception_handler(Exception, global_exception_handler)
