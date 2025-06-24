# tools/cli/relay/app.py
import uuid
import logging

# third party library
import uvicorn  # type: ignore
from fastapi import FastAPI  # type: ignore

# local library
from config.settings import SERVER_IP, SERVER_PORT
from config.settings import LOG_LEVEL, SERVICE_NAME, SERVICE_VERSION
from utils.logging.baselogger import setup_logger, trace_id_var
from api.endpoints import router

# Setup logger
setup_logger(LOG_LEVEL, SERVICE_NAME, SERVICE_VERSION)
# Create FastAPI app instance
app = FastAPI()
# Register routers
app.include_router(router)
# Get the logger instance
logger = logging.getLogger(__name__)

# ---- Middleware ----
@app.middleware("http")
async def add_trace_id(request, call_next):
    """
    Middleware to add trace_id to the request context.
    This is useful for logging and tracing requests.
    """
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    logger.debug(f"Received request with trace_id: {trace_id}")

    # Set the trace_id in the context variable
    token = trace_id_var.set(trace_id)

    try:
        response = await call_next(request)
    finally:
        trace_id_var.reset(token)
    response.headers["X-Trace-ID"] = trace_id
    return response


if __name__ == "__main__":
    logger.info(f"Starting {SERVICE_NAME} version {SERVICE_VERSION}")
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)
