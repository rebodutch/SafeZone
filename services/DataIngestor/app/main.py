# app/main.py
import logging
from contextlib import asynccontextmanager

import uvicorn  # type: ignore
from fastapi import FastAPI  # type: ignore

from utils.logging.baselogger import setup_logger

from config.settings import SERVER_IP, SERVER_PORT, SERVICE_NAME, SERVICE_VERSION
from config.settings import LOG_LEVEL
from config.kafka import startup_event, shutdown_event
from api.endpoints import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.kafka_producer = await startup_event()
    yield
    await shutdown_event(app.state.kafka_producer)


def create_app() -> FastAPI:
    """App factory: setup logging, routers, exception handlers, preload caches."""
    setup_logger(
        log_level=LOG_LEVEL, service_name=SERVICE_NAME, service_version=SERVICE_VERSION
    )
    app = FastAPI(
        title=SERVICE_NAME,
        version=SERVICE_VERSION,
        lifespan=lifespan,
    )
    app.include_router(router)
    return app


app = create_app()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting {SERVICE_NAME} version {SERVICE_VERSION}")
    uvicorn.run("main:app", host=SERVER_IP, port=SERVER_PORT, reload=True)
