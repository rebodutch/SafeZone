import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# Redis settings
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_LOG_FILE_SIZE = int(os.getenv("MAX_LOG_FILE_SIZE", str(5 * 1024 * 1024)))

# Relay API settings
## access the environment variables
SERVER_IP = os.getenv("SERVER_IP", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "80"))
## name and version of the service
SERVICE_NAME = os.getenv("SERVICE_NAME", "time-server")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.0.0")     
