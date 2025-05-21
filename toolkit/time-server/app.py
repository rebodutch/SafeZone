# tools/cli/relay/app.py
# third party library
import uvicorn
from fastapi import FastAPI

# local library
from config.logger import get_logger
from config.settings import SERVER_IP, SERVER_PORT, SERVICE_NAME, SERVICE_VERSION
from api.endpoints import router

app = FastAPI()
# Register routers
app.include_router(router)
# Get the logger instance
logger = get_logger()


if __name__ == "__main__":
    logger.info(f"Starting {SERVICE_NAME} version {SERVICE_VERSION}")
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)
