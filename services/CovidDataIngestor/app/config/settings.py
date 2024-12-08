import os 

SERVER_IP = os.getenv("Server_IP", "0.0.0.0")
SERVER_PORT = int(os.getenv("Server_PORT", "6010"))
DB_URL = os.getenv("db_url", "sqlite:////db/test.db")
APP_NAME = os.getenv("app_name", "CovidDataIngestor")
APP_VERSION = os.getenv("app_version", "1.0.0")