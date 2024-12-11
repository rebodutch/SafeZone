# app/api/endpoints.py
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from validators.api_validator import CollectValidator
from exceptions.custom_exceptions import InvalidContentTypeException, APIValidationError
from pipeline.orchestrator import handle_request
from config.logger import get_logger

router = APIRouter()
logger = get_logger()


def type_checker(request: Request):
    print(request.headers.get("content-type"))
    if request.headers.get("content-type") != "application/json":
        raise InvalidContentTypeException()


@router.post("/collect")
async def collect(data: dict, content_type_check: None = Depends(type_checker)):
    """
    Collect data from the request and handle it.

    Args:
        data (List[dict]): A list of dictionaries containing the data to be collected.
            "message": "Data collected successfully",
    Returns:
        JSONResponse: A JSON response indicating the success or failure of the data collection.
    """
    logger.info("Received request to collect data.")

    # validate the data in the request body
    try:
        CollectValidator(**data)
    except ValidationError as e:
        raise APIValidationError(e)

    handle_request(data)

    response = {
        "status": "success",
        "message": "Data collected successfully",
    }
    logger.info("Data collection request handle success.")
    return JSONResponse(content=response, status_code=200)
