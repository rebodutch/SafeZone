# app/services/data_sender.py
import requests
from config.settings import CovidDataCollector_URL
from common.schemas.covid_case import CovidCase

def send_data(data):
    try:
        # validate the data
        for case in data:
            CovidCase.validate_data(**case)

        # send the data to the CovidDataCollector service
        response = requests.post(CovidDataCollector_URL, json=data, timeout=10)
        response.raise_for_status()

        return {"status_code": response.status_code, "response": response.json()}
    # the exception will be handled in the endpioint layer
    except Exception as e:
        raise e
