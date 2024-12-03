# app/api/endpoints.py
from typing import List
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from services.pipeline import handle_request
from utils.custom_exceptions.handler import handle_exceptions
from utils.custom_exceptions.exceptions import InvalidContentTypeException
from config.logger import get_logger

router = APIRouter()
logger = get_logger()

def type_checker(request: Request):
    try:
        if request.headers.get("content-type") != "application/json":
            raise InvalidContentTypeException()
    except InvalidContentTypeException as e:
        return handle_exceptions(e)

@router.post("/collect")
async def collect(data: List[dict], content_type_check: None = Depends(type_checker)):
    """
    Collect data from the request and handle it.

    Args:
        data (List[dict]): A list of dictionaries containing the data to be collected.
            "message": "Data collected successfully",
    Returns:
        JSONResponse: A JSON response indicating the success or failure of the data collection.
    """
    try:
        logger.info("Data collection request received.")
        
        handle_request(data)
        response = {
            "message": "Data collected successfully",
        }
        logger.info("Data collection request handle success.")
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return handle_exceptions(e)