# app/api/endpoints.py
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from exceptions.custom_exceptions import InvalidContentTypeException
from api.schemas import APIResponse, CollectData
from pipeline.orchestrator import handle_request
from config.logger import get_logger

router = APIRouter()
logger = get_logger()


def type_checker(request: Request):
    print(request.headers.get("content-type"))
    if request.headers.get("content-type") != "application/json":
        raise InvalidContentTypeException()


@router.post("/collect", response_model=APIResponse)
async def collect(
    payload: CollectData, content_type_check: None = Depends(type_checker)
):
    logger.info("Received request to collect data.")

    data = payload.model_dump()
    logger.debug(f"Request data: {data}")

    handle_request(data)

    response = APIResponse(
        success=True,
        message="Data created successfully",
        data={
            "detail": f"The data was created in the database successfully."
        },
    )
    logger.info("Data collection request handle success.")
    
    return JSONResponse(
        content=response.model_dump(exclude_none=True),
        status_code=200,
    )

