# tools/relay/api/endpoint.py
import logging
from datetime import datetime

# third party library
# fastapi is a web framework for building APIs with Python.
from fastapi import APIRouter, Depends, HTTPException, Depends  # type: ignore
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # type: ignore

# google-auth is a library for Google Authentication
from google.oauth2 import id_token  # type: ignore
from google.auth.transport import requests as grequests  # type: ignore

# local library
import bin.db_helper as db_helper
import bin.health_helper as health_helper
import bin.service_caller as service_caller
from schemas.request import SimulateModel
from schemas.response import APIResponse, VerifyResponseModel, VerifyDataModel
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

        service_caller.simulate(date=data["date"], end_date=data["end_date"])

        return APIResponse(
            success=True, message="Dataflow/simulate execute successfully."
        )

    except Exception as e:
        logger.error(f"Dataflow/simulate execute failed: {str(e)}")
        return APIResponse(
            success=False,
            message="Dataflow/simulate execute failed.",
            errors={"detail": str(e)},
        )


@router.get("/dataflow/verify", response_model=VerifyResponseModel)
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
        # Validate the parameters
        response = service_caller.verify(
            date=date,
            interval=interval,
            city=city,
            region=region,
            ratio=ratio,
        )
        logger.debug(f"Response from analytics api: {response}")
        resp_data = response["data"]

        return VerifyResponseModel(
            success=True,
            message="Dataflow/verify execute successfully.",
            data=VerifyDataModel(
                start_date=resp_data["start_date"],
                end_date=resp_data["end_date"],
                city=resp_data.get("city"),
                region=resp_data.get("region"),
                aggregated_cases=resp_data.get("aggregated_cases"),
                cases_population_ratio=resp_data.get("cases_population_ratio"),
            ),
        )

    except Exception as e:
        logger.error(f"Dataflow/verify execute failed: {str(e)}")
        return APIResponse(
            success=False,
            message="Dataflow/verify execute failed.",
            errors={"detail": str(e)},
        )


# ---- System Request ----
@router.get("/system/health", response_model=APIResponse)
async def get_health(
    role=Depends(get_role),
):
    whitelist_check(role, ["admin", "user"])


@router.post("/time/set", response_model=APIResponse)
async def set_time(
    role=Depends(get_role),
):
    whitelist_check(role, ["admin"])


@router.get("/time/now", response_model=APIResponse)
async def get_now(
    role=Depends(get_role),
):
    whitelist_check(role, ["admin", "user"])


@router.get("/time/status", response_model=APIResponse)
async def get_now(
    role=Depends(get_role),
):
    whitelist_check(role, ["admin", "user"])


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
            errors={"detail": str(e)},
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
            errors={"detail": str(e)},
        )
