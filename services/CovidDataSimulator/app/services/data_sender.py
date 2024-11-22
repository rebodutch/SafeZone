# app/services/data_sender.py
import requests
from config import CovidDataCollector_URL


def send_data(data):
    response = requests.post(CovidDataCollector_URL, json=data)
    return {"status_code": response.status_code, "response": response.json()}
