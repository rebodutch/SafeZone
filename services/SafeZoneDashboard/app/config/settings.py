# app/config/settings.py
import os
from dotenv import load_dotenv # type: ignore

# load environment variables
load_dotenv()

# Server settings
API_URL = os.getenv("ANALYTICS_API_URL", "http://0.0.0.0:8000")
TIME_SERVER_URL = os.getenv("TIME_SERVER_URL", "http://0.0.0.0:8000")

# Service settings
SERVICE_NAME = os.getenv("SERVICE_NAME", "SafeZoneDashboard")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")
SERVER_IP = os.getenv("SERVER_IP", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))
# Logging settings
LOG_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
    