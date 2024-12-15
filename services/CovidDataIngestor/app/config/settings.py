import os

# Service settings
SERVICE_NAME = os.getenv("SERVICE_NAME", "CovidDataIngestor")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")
# Server settings
SERVER_IP = os.getenv("Server_IP", "0.0.0.0")
SERVER_PORT = int(os.getenv("Server_PORT", "8010"))
DB_URL = os.getenv("DB_URL", "sqlite:////db/test.db")
# Logging settings
LOG_LEVEL = os.getenv("LOGGING_LEVEL", "DEBUG")
MAX_LOG_FILE_SIZE = os.getenv("LOG_FILE_SIZE", 5 * 1024 * 1024)  # 5 MB