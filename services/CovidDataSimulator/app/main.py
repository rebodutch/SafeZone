# app/main.py
import logging

import uvicorn
from fastapi import FastAPI

from utils.logging.baselogger import setup_logger
from api.endpoints import router
from config.settings import SERVER_IP, SERVER_PORT, SERVICE_NAME, SERVICE_VERSION
from config.settings import LOG_LEVEL
from exceptions.hanlders import register_exception_handlers


def create_app() -> FastAPI:
    """App factory: setup logging, routers, exception handlers, preload caches."""
    setup_logger(
        log_level=LOG_LEVEL,
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    app = FastAPI(
        title=SERVICE_NAME,
        version=SERVICE_VERSION,
    )
    app.include_router(router)
    register_exception_handlers(app)
    return app

app = create_app()
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info(f"Starting {SERVICE_NAME} version {SERVICE_VERSION}")
    uvicorn.run("main:app", host=SERVER_IP, port=SERVER_PORT, reload=True)