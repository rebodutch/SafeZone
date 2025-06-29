# app/config/settings.py
import os
from dotenv import load_dotenv # type: ignore

# load environment variables
load_dotenv()

# Service settings
SERVICE_NAME = os.getenv("SERVICE_NAME", "CovidDataSimulator")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")
# Server settings
SERVER_IP = os.getenv("Server_IP", "0.0.0.0")
SERVER_PORT = int(os.getenv("Server_PORT", "8000"))
INGESTOR_URL = os.getenv("INGESTOR_URL", "http://0.0.0.0:8010/collect")
# Logging settings
LOG_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
MAX_LOG_FILE_SIZE = int(os.getenv("LOG_FILE_SIZE", str(5 * 1024 * 1024)))  # 5 MB