from fastapi import Request, HTTPException
from exceptions.custom_exceptions import InvalidDateRangeError
from exceptions.custom_exceptions import APIValidationError
from exceptions.custom_exceptions import ServiceValidationError
from exceptions.custom_exceptions import EmptyDataError

async def invalid_date_range_error_handler(request: Request, exc: InvalidDateRangeError):
    raise HTTPException(status_code=400, detail=str(exc))

async def empty_data_error_handler(request: Request, exc: EmptyDataError):
    raise HTTPException(status_code=500, detail=str(exc))

async def api_validation_error_handler(request: Request, exc: APIValidationError):
    print(type(exc.errors))
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


async def service_validation_error_handler(request: Request, exc: ServiceValidationError):
    excs = exc.json(indent=2)
    for exc in excs:
        raise HTTPException(status_code=500, detail=str(exc))


def register_exception_handlers(app):
    app.add_exception_handler(InvalidDateRangeError, invalid_date_range_error_handler)
    app.add_exception_handler(EmptyDataError, empty_data_error_handler)
    app.add_exception_handler(APIValidationError, api_validation_error_handler)
    app.add_exception_handler(ServiceValidationError, service_validation_error_handler)
    
