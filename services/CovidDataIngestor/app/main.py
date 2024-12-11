# app/main.py
from fastapi import FastAPI
import uvicorn

from api.endpoints import router
from config.settings import SERVER_IP, SERVER_PORT, SERVICE_NAME, SERVICE_VERSION
from config.logger import get_logger
from exceptions.handlers import register_exception_handlers


app = FastAPI()
# Register routers
app.include_router(router)
# Register exception handlers
register_exception_handlers(app)
# Get the logger instance
logger = get_logger()


if __name__ == "__main__":
    logger.info(f"Starting {SERVICE_NAME} version {SERVICE_VERSION}")
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)
