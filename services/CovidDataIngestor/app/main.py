# app/main.py
from fastapi import FastAPI
import uvicorn

from config.settings import SERVER_IP, SERVER_PORT, APP_NAME, APP_VERSION
from config.logger import get_logger
from api.endpoints import router

app = FastAPI()
logger = get_logger()

app.include_router(router)
logger.info(f"{APP_NAME} v{APP_VERSION} has started.")

if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT, reload=True)