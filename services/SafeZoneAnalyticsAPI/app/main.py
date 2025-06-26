# app/main.py
import logging
from contextlib import asynccontextmanager

import uvicorn  # type: ignore
from fastapi import FastAPI  # type: ignore
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from utils.logging.baselogger import setup_logger
from api.endpoints import router
from config.settings import SERVER_IP, SERVER_PORT, SERVICE_NAME, SERVICE_VERSION
from config.settings import LOG_LEVEL, DB_URL
from exceptions.handlers import register_exception_handlers
from config.cache import get_city_region_cache, get_populations_cache, get_redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_engine(DB_URL)
    app.state.engine = engine
    app.state.Session = sessionmaker(bind=engine)
    app.state.redis_client = await get_redis_client()
    app.state.city_region_cache = get_city_region_cache(app.state.Session)
    app.state.populations_cache = get_populations_cache(app.state.Session)
    yield
    # Cleanup
    engine.dispose()


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
        lifespan=lifespan,
    )
    app.include_router(router)
    register_exception_handlers(app)
    return app


app = create_app()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting {SERVICE_NAME} version {SERVICE_VERSION}")
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT, reload=True)
