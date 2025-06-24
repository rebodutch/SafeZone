import os
from dotenv import load_dotenv # type: ignore

# load environment variables
load_dotenv()

# Redis settings
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Relay API settings
## access the environment variables
SERVER_IP = os.getenv("SERVER_IP", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
## name and version of the service
SERVICE_NAME = os.getenv("SERVICE_NAME", "time-server")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.0.0")     
