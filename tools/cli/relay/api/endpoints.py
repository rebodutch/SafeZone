# tools/relay/api/endpoint.py
# third party library
# fastapi is a web framework for building APIs with Python.
from fastapi import APIRouter, Depends, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# google-auth is a library for Google Authentication
from google.oauth2 import id_token
from google.auth.transport import requests

# local library
import bin.db_helper as db_helper
import bin.service_caller as service_caller
from schemas.request import SimulateModel, VerifyModel
from schemas.response import APIResponse
from config.logger import get_logger
from config.settings import ADMIN_EMAILS


router = APIRouter()
security = HTTPBearer()

logger = get_logger()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request())
        email = idinfo["email"]
        return "admin" if email in ADMIN_EMAILS else "user"
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


# endpoint: /dataflow/simulate
@router.post("/dataflow/simulate", response_model=APIResponse)
async def simulate(
    payload: SimulateModel,
    role=Depends(get_current_user),
):
    try:
        logger.debug("Received request to simulate model.")
        data = payload.model_dump()
        if not data["dry_run"]:
            service_caller.simulate(date=data["date"], end_date=data["end_date"])
        return APIResponse(success=True, message="Model simulated successfully.")

    except Exception as e:
        logger.debug(f"Error while simulating model: {str(e)}")
        return APIResponse(
            success=False,
            message="Error while simulating model.",
            errors={"detail": str(e)},
        )


# endpoint: /dataflow/verify
@router.get("/dataflow/verify", response_model=APIResponse)
async def verify(
    payload: VerifyModel,
    role=Depends(get_current_user),
):
    try:
        logger.debug("Received request to verify model.")
        data = payload.model_dump()
        response = service_caller.verify(
            date=data["date"],
            interval=data["interval"],
            city=data["city"],
            region=data["region"],
            ratio=data["ratio"],
        )
        return APIResponse(
            success=True, message="Model verified successfully.", data=response
        )

    except Exception as e:
        logger.debug(f"Error while verifying model: {str(e)}")
        return APIResponse(
            success=False,
            message="Error while verifying model.",
            errors={"detail": str(e)},
        )


# endpoint: /db/init
@router.post("/db/init", response_model=APIResponse)
async def db_init(
    role=Depends(get_current_user),
):
    try:
        if role != "admin":
            raise HTTPException(status_code=403, detail="Permission denied.")

        logger.debug("Received request to initialize database.")
        db_helper.init_db()
        return APIResponse(success=True, message="Database initialized successfully.")

    except Exception as e:
        logger.debug(f"Error while initializing database: {str(e)}")
        return APIResponse(
            success=False,
            message="Error while initializing database.",
            errors={"detail": str(e)},
        )


# endpoint: /db/clear
@router.post("/db/clear", response_model=APIResponse)
async def db_clear(
    role=Depends(get_current_user),
):
    try:
        if role != "admin":
            raise HTTPException(status_code=403, detail="Permission denied.")

        logger.debug("Received request to clear database.")
        db_helper.clear_db()
        return APIResponse(success=True, message="Database cleared successfully.")

    except Exception as e:
        logger.debug(f"Error while clearing database: {str(e)}")
        return APIResponse(
            success=False,
            message="Error while clearing database.",
            errors={"detail": str(e)},
        )


# endpoint: /db/reset
@router.post("/db/reset", response_model=APIResponse)
async def db_reset(
    role=Depends(get_current_user),
):
    try:
        if role != "admin":
            raise HTTPException(status_code=403, detail="Permission denied.")

        logger.debug("Received request to reset database.")
        db_helper.reset_db_id()
        return APIResponse(success=True, message="Database reset successfully.")

    except Exception as e:
        logger.debug(f"Error while resetting database: {str(e)}")
        return APIResponse(
            success=False,
            message="Error while resetting database.",
            errors={"detail": str(e)},
        )
