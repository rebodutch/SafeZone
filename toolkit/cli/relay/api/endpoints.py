# tools/relay/api/endpoint.py
import logging

# third party library
# fastapi is a web framework for building APIs with Python.
from fastapi import APIRouter, Depends, HTTPException, Depends  # type: ignore
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # type: ignore

# google-auth is a library for Google Authentication
from google.oauth2 import id_token  # type: ignore
from google.auth.transport import requests as grequests  # type: ignore

# local library
import bin.db_helper as db_helper
import bin.time_helper as time_helper
import bin.health_helper as health_helper
import bin.service_helper as service_helper
from utils.pydantic_model.request import SimulateModel, SetTimeModel
from utils.pydantic_model.request import VerifyModel, HealthCheckModel
from utils.pydantic_model.response import APIResponse, AnalyticsAPIResponse
from utils.pydantic_model.response import SystemDateResponse, MocktimeStatusResponse
from config.settings import CLIENT_ID, ROLE_MAP

router = APIRouter()
logger = logging.getLogger(__name__)

# ---- Authentication ----
security = HTTPBearer()


def get_role(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=401, detail="Missing or malformed Authorization header"
        )
    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), CLIENT_ID)

        # Check if the token is issued by Google
        if idinfo.get("iss") != "https://accounts.google.com":
            raise HTTPException(status_code=401, detail="Invalid issuer")

        # Check if the email is verified
        if not idinfo.get("email_verified"):
            raise HTTPException(status_code=403, detail="Email not verified")

        # Check if the email is in the allowed list
        user_email = idinfo.get("email")

        logger.debug(f"Logging user email: {user_email}")

        if user_email not in ROLE_MAP:
            raise HTTPException(status_code=403, detail="Email not allowed")

        # Map the email to a role and return it
        return ROLE_MAP[user_email]
    except Exception as e:
        logger.debug(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=401, detail=f"Token verification failed: {str(e)}"
        )


def whitelist_check(role: str, allowed_roles: list):
    if role not in allowed_roles:
        logger.debug(
            f"The current role '{role}' is not allowed to access this endpoint."
        )
        raise HTTPException(
            status_code=403, detail="Access forbidden: insufficient permissions"
        )


# ---- Dataflow request ----
@router.post("/dataflow/simulate", response_model=APIResponse)
async def simulate(
    payload: SimulateModel,
    role=Depends(get_role),
):
    whitelist_check(role, ["admin"])
    try:
        logger.debug("Received request to dataflow/simulate model.")

        data = payload.model_dump()

        response_json = service_helper.simulate(
            date=data["date"], end_date=data["end_date"]
        )

        return APIResponse(**response_json)

    except Exception as e:
        logger.error(f"Dataflow/simulate execute failed: {str(e)}")
        return APIResponse(
            success=False,
            message="Dataflow/simulate execute failed.",
            errors={
                "field": "Unknown",
                "summary": "Dataflow/simulate execute failed.",
                "detail": str(e),
            },
        )


@router.get("/dataflow/verify", response_model=AnalyticsAPIResponse)
async def verify(
    date: str,
    interval: int = 1,
    city: str = None,
    region: str = None,
    ratio: bool = False,
    role=Depends(get_role),
):
    whitelist_check(role, ["admin", "user"])
    try:
        logger.debug("Received request to dataflow/verify model.")

        # Validate the parameters using Pydantic model
        _ = VerifyModel(
            date=date,
            interval=interval,
            city=city,
            region=region,
            ratio=ratio,
        )
        response_json = service_helper.verify(
            date=date,
            interval=interval,
            city=city,
            region=region,
            ratio=ratio,
        )
        return AnalyticsAPIResponse(**response_json)

    except Exception as e:
        logger.error(f"Dataflow/verify execute failed: {str(e)}")
        return AnalyticsAPIResponse(
            success=False,
            message="Dataflow/verify execute failed.",
            errors={
                "field": "Unknown",
                "summary": "Dataflow/verify execute failed.",
                "detail": str(e),
            },
        )


# ---- System Request ----
@router.get("/system/health", response_model=APIResponse)
async def get_health(
    target: str = None,
    all: bool = False,
    role=Depends(get_role),
):
    whitelist_check(role, ["admin", "user"])
    try:
        logger.debug("Received request to system/health model.")

        # Validate the parameters using Pydantic model
        _ = HealthCheckModel(target=target, all=all)

        response_json = health_helper.get_health(target=target, all=all)

        return APIResponse(**response_json)
    except Exception as e:
        logger.error(f"System/health execute failed: {str(e)}")
        return APIResponse(
            success=False,
            message="System/health execute failed.",
            errors={
                "field": "Unknown",
                "summary": "System/health execute failed.",
                "detail": str(e),
            },
        )


@router.post("/system/time/set", response_model=APIResponse)
async def set_time(
    payload: SetTimeModel,
    role=Depends(get_role),
):
    whitelist_check(role, ["admin"])
    try:
        logger.debug("Received request to time/set model.")

        data = payload.model_dump()

        response_json = time_helper.set_mock_config(**data)

        return APIResponse(**response_json)

    except Exception as e:
        logger.error(f"Time/set execute failed: {str(e)}")
        return APIResponse(
            success=False,
            message="Time/set execute failed.",
            errors={
                "field": "Unknown",
                "summary": "Time/set execute failed.",
                "detail": str(e),
            },
        )


@router.get("/system/time/now", response_model=SystemDateResponse)
async def get_now(
    role=Depends(get_role),
):
    whitelist_check(role, ["admin", "user"])
    try:
        logger.debug("Received request to time/now model.")

        response_json = time_helper.get_system_date()

        return SystemDateResponse(**response_json)

    except Exception as e:
        logger.error(f"Time/now execute failed: {str(e)}")
        return SystemDateResponse(
            success=False,
            message="Time/now execute failed.",
            errors={
                "field": "Unknown",
                "summary": "Time/now execute failed.",
                "detail": str(e),
            },
        )


@router.get("/system/time/status", response_model=MocktimeStatusResponse)
async def get_status(
    role=Depends(get_role),
):
    whitelist_check(role, ["admin", "user"])
    try:
        logger.debug("Received request to time/status model.")

        response_json = time_helper.get_mock_config()

        logger.debug(f"Mocktime status response: {response_json}")

        return MocktimeStatusResponse(**response_json)

    except Exception as e:
        logger.error(f"Time/status execute failed: {str(e)}")
        return MocktimeStatusResponse(
            success=False,
            message="Time/status execute failed.",
            errors={
                "field": "Unknown",
                "summary": "Time/status execute failed.",
                "detail": str(e),
            },
        )


# ---- DB Request ----
@router.post("/db/init", response_model=APIResponse)
async def db_init(
    role=Depends(get_role),
):
    whitelist_check(role, ["admin"])
    try:
        logger.debug("Received request to db/init model.")

        db_helper.init_db()

        return APIResponse(success=True, message="Database initialized successfully.")

    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")

        return APIResponse(
            success=False,
            message="Database initialization failed.",
            errors={
                "field": "Unknown",
                "summary": "Database initialization failed.",
                "detail": str(e),
            },
        )


@router.post("/db/clear", response_model=APIResponse)
async def db_clear(
    role=Depends(get_role),
):
    whitelist_check(role, ["admin"])
    try:
        logger.debug("Received request to db/clear model.")

        db_helper.clear_db()

        return APIResponse(success=True, message="Database cleared successfully.")

    except Exception as e:
        logger.error(f"Database clearing failed: {str(e)}")

        return APIResponse(
            success=False,
            message="Database clearing failed.",
            errors={
                "field": "Unknown",
                "summary": "Database clearing failed.",
                "detail": str(e),
            },
        )
