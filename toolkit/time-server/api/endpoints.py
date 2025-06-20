# toolkit/time-server/api/endpoints.py
import json
from datetime import datetime, timedelta

import redis
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from config.logger import get_logger
from config.settings import REDIS_HOST
from schemas import SetTimeModel
from schemas import APIResponse, ErrResponse, TimeResponse, StatResponse

router = APIRouter()
logger = get_logger()


def get_time_config():
    r = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)
    value = r.get("time:config")
    if not value:
        raise ValueError("No time config found in redis.")
    return json.loads(value)


def get_current_date(
    launch_time: datetime, mock_time: datetime, acceleration: int = 1
) -> str:
    """
    Get the current date, adjusted by the number of bias days.
    """
    shift = datetime.now() - launch_time
    currtime = mock_time + shift * acceleration
    return currtime.strftime("%Y-%m-%d")


@router.get("/now", response_model=APIResponse)
async def get_now():
    try:
        logger.debug("Received request to get_now model.")

        time_config = get_time_config()

        mock = bool(time_config["mock"])

        if not mock:
            return TimeResponse(
                message="Current date retrieved successfully.",
                date=datetime.now().strftime("%Y-%m-%d"),
            )
        else:
            return TimeResponse(
                message="Current date retrieved successfully.",
                date=get_current_date(
                    launch_time=datetime.strptime(
                        time_config["launch_time"], "%Y-%m-%d %H:%M:%S"
                    ),
                    mock_time=datetime.strptime(
                        time_config["mock_time"], "%Y-%m-%d %H:%M:%S"
                    ),
                    acceleration=int(time_config["acceleration"]),
                ),
            )
    except Exception as e:
        logger.debug(f"Error while get_now model: {str(e)}")
        return ErrResponse(
            success=False,
            message="Error while get_now model.",
            detail=str(e),
        )


@router.post("/set", response_model=APIResponse)
async def set_time_config(
    payload: SetTimeModel,
):
    try:
        logger.debug("Received request to set_time model.")

        data = payload.model_dump()

        mock = bool(data["mock"])
        mock_date = data["mock_date"] if "mock_date" in data else None
        acceleration = data["accelerate"] if "accelerate" in data else 1

        time_config = get_time_config()
        time_config["mock"] = mock
        if mock:
            if mock_date:
                time_config["mock_time"] = mock_date + " 00:00:00"
                if "launch_time" not in time_config:
                    time_config["launch_time"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                # check if mock_time later than launch_time
                launch_time = datetime.strptime(
                    time_config["launch_time"], "%Y-%m-%d %H:%M:%S"
                )
                mock_time = datetime.strptime(
                    time_config["mock_time"], "%Y-%m-%d %H:%M:%S"
                )
                if mock_time > launch_time:
                    raise ValueError("Launch time must be later than mock time.")
            time_config["acceleration"] = acceleration

        r = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)
        r.set("time:config", json.dumps(time_config))
        logger.debug(f"Set time config: {time_config}")

        return APIResponse(success=True, message="Time configuration set successfully.")
    except Exception as e:
        logger.debug(f"Error while set_time model: {str(e)}")
        return ErrResponse(
            success=False,
            message="Error while set_time model.",
            detail=str(e),
        )


@router.get("/status", response_model=StatResponse)
async def get_time_config():
    try:
        logger.debug("Received request to get_time_config model.")

        time_config = get_time_config()
        mock = bool(time_config.get("mock", False))
        launch_time = datetime.strptime(
            time_config.get("launch_time", "1970-01-01 00:00:00"),
            "%Y-%m-%d %H:%M:%S",
        )
        mock_time = datetime.strptime(
            time_config.get("mock_time", "1970-01-01 00:00:00"),
            "%Y-%m-%d %H:%M:%S",
        )
        acceleration = int(time_config.get("acceleration", 1))

        return StatResponse(
            message="Time configuration retrieved successfully.",
            mock=mock,
            mock_time=mock_time.strftime("%Y-%m-%d %H:%M:%S"),
            launch_time=launch_time.strftime("%Y-%m-%d %H:%M:%S"),
            accelerate=acceleration,
            current_date=get_current_date(
                launch_time=launch_time, mock_time=mock_time, acceleration=acceleration
            ),
            real_date=datetime.now().strftime("%Y-%m-%d"),
        )
    except Exception as e:
        logger.debug(f"Error while get_time_config model: {str(e)}")
        return ErrResponse(
            success=False,
            message="Error while get_time_config model.",
            detail=str(e),
        )
