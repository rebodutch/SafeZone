# app/api/endpoints.py
import json
import logging

from fastapi import APIRouter, Request  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from pydantic import ValidationError  # type: ignore

from utils.pydantic_model.request import CovidDataModel
from utils.pydantic_model.response import ErrorModel, APIResponse, HealthResponse
from config.settings import KAFKA_TOPIC

router = APIRouter()
logger = logging.getLogger(__name__)


def generate_partition_key(city: str, region: str) -> str:
    # hash region(utf-8 str) to numeric value, betwwn 0 and 10
    region_hash = hash(region.encode("utf-8")) % 10
    return f"{city}-{region_hash}"


async def sent_to_kafka(producer, payload: dict, partition_key: str):
    if producer:
        await producer.send_and_wait(
            topic=KAFKA_TOPIC,
            value=json.dumps(payload).encode("utf-8"),
            key=partition_key,
        )
    # If the producer is not available, log the payload and partition key for testing purposes or debugging.
    else:
        logger.debug(
            "Kafka producer is not available, the expected behavior is sent following data to Kafka"
        )
        logger.debug(f"Payload: {payload}, Partition Key: {partition_key}")
        return


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(success=True, message="Service is healthy.", status="healthy")


@router.post("/covid_event", response_model=APIResponse)
async def covid_event_handler(
    request: Request,
    payload: CovidDataModel,
):
    try:
        logger.debug("Received request to endpoint /covid_event with payload")

        data = payload.model_dump()
        logger.debug(f"Sent data to Kafka: {data}")
        await sent_to_kafka(
            producer=request.app.state.kafka_producer ,
            payload=data,
            partition_key=generate_partition_key(
                city=data["city"],
                region=data["region"],
            ),
        )
        logger.debug("Data sent to Kafka successfully")

        return APIResponse(
            success=True,
            message="Data produced to Kafka successfully.",
        )
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        resp = APIResponse(
            success=False,
            message="Validation error occurred",
            errors=ErrorModel(
                field=ve.errors()[0].get("loc", ["unknown"])[0],
                summary=ve.errors()[0].get("msg", "Invalid input"),
                detail=str(ve),
            ),
        )
        return JSONResponse(
            status_code=422,
            content=resp.model_dump(),
        )
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        resp = APIResponse(
            success=False,
            message="Failed to process the request",
            errors=ErrorModel(
                field="unknown",
                summary="Error processing the request, please try again later.",
                detail=str(e),
            ),
        )
        return JSONResponse(
            status_code=500,
            content=resp.model_dump(),
        )
