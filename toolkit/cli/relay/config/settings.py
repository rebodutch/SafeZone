import os
import yaml

from dotenv import load_dotenv  # type: ignore

environment = os.getenv("ENVIRONMENT").lower()
if environment == "test":
    # load environment variables
    load_dotenv(".env")
    print("Loaded environment variables from .env file")
else:
    print("No .env loading, all config must come from env (docker/k8s)")


def get_setted_env(name: str) -> str:
    """Get the environment variable or return the default value."""
    value = os.getenv(name, None)
    if value is None:
        print(f"Environment variable {name} is not set.")
        raise ValueError(f"Environment variable {name} is not set.")
    return value


def load_roles(path="roles.example.yaml") -> dict:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data["roles"]


# Load roles from the YAML file
ROLE_MAP = load_roles(get_setted_env("ROLE_FILE"))

# DB settings
DB_URL = get_setted_env("DB_URL")
REPLICA_URL = get_setted_env("REPLICA_URL")
# Redis settings
REDIS_HOST = get_setted_env("REDIS_HOST")
# Service settings
SIMULATOR_URL = get_setted_env("SIMULATOR_URL")
INGESTOR_URL = get_setted_env("INGESTOR_URL")
ANALYTICS_API_URL = get_setted_env("ANALYTICS_API_URL")
DASHBOARD_URL = get_setted_env("DASHBOARD_URL")
MKDOC_URL = get_setted_env("MKDOC_URL")
TIME_SERVER_URL = get_setted_env("TIME_SERVER_URL")
# Security settings
CLIENT_ID = get_setted_env("CLIENT_ID")

# default settings
## api server settings
SERVER_IP = os.getenv("SERVER_IP", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
## service settings
SERVICE_NAME = os.getenv("SERVICE_NAME", "cli_relay")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.0.0")
## logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
