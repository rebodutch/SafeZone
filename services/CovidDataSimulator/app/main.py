# app/main.py
from fastapi import FastAPI
from api import endpoints
from exceptions.hanlders import register_exception_handlers
from config.settings import SERVER_IP, SERVER_PORT, SERVICE_NAME, SERVICE_VERSION
from config.logger import get_logger
import uvicorn

app = FastAPI()

# Register routers
app.include_router(endpoints.router)
# Register exception handlers
register_exception_handlers(app)
# Get the logger instance
logger = get_logger()

if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)
