# app/config/settings.py
import os

# Service settings
SERVICE_NAME = os.getenv("SERVICE_NAME", "SafeZoneDashboard")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")
# Server settings
API_URL = os.getenv("Analytics_API_URL", "http://0.0.0.0:8000")
# Logging settings
LOG_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
MAX_LOG_FILE_SIZE = os.getenv("LOG_FILE_SIZE", 5 * 1024 * 1024)  # 5 MB