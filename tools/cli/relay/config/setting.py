import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# DB settings
DB_URL = os.getenv("DB_URL", "sqlite:///relay.db")
# Service settings
SIMULATOR_URL = os.getenv("SIMULATOR_URL", "http://localhost:5000")
ANALYTICS_API_URL = os.getenv("ANALYTICS_API_URL", "http://localhost:5001")

# logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_LOG_FILE_SIZE = int(os.getenv("MAX_LOG_FILE_SIZE", str(5 * 1024 * 1024)))

# Relay API settings
## access the environment variables
SERVER_IP = os.getenv("SERVER_IP", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "80"))
## name and version of the service
SERVICE_NAME = os.getenv("SERVICE_NAME", "cli_relay")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.0.0")     
