# app/config/settings.py
import os

Server_IP = os.getenv("Server_IP", "0.0.0.0")
Server_PORT = int(os.getenv("Server_PORT", "6000"))
CovidDataCollector_URL = os.getenv("CovidDataCollector_URL", "http://0.0.0.0:8000/collect")
