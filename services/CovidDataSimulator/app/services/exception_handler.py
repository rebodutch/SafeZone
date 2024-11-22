# test_exception_handler.py
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from exception import InvalidDateFormatError, InvalidDateRangeError, EmptyDataError
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException


def handle_exceptions(e):
    # date excptions
    if isinstance(e, InvalidDateFormatError):
        raise HTTPException(status_code=422, detail=str(e))
    elif isinstance(e, InvalidDateRangeError):
        raise HTTPException(status_code=400, detail=str(e))
    elif isinstance(e, EmptyDataError):
        response = {
            "status": "success",
            "message": "No data available for the given date(s).",
        }
        return JSONResponse(content=response, status_code=200)
    # requests exceptions
    elif isinstance(e, ConnectionError):
        raise HTTPException(status_code=503, detail="Failed to connect to the server.")
    elif isinstance(e, Timeout):
        raise HTTPException(status_code=504, detail="The request timed out.")
    elif isinstance(e, HTTPError):
        raise HTTPException(status_code=400, detail=f"HTTP error occurred: {str(e)}")
    elif isinstance(e, RequestException):
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred")
    else:
        raise HTTPException(status_code=400, detail=str(e))
