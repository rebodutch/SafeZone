# app/services/data_sender.py
import requests
from config.settings import CovidDataIngestor_URL
from utils.models.case_validator import validate_data

def send_data(data):
    try:
        # validate the data
        for case in data:
            validate_data(**case)

        # send the data to the CovidDataIngestor service
        response = requests.post(CovidDataIngestor_URL, json=data, timeout=10)
        response.raise_for_status()

        return {"status_code": response.status_code, "response": response.json()}
    # the exception will be handled in the endpioint layer
    except Exception as e:
        raise e
