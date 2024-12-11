# app/services/data_sender.py
import requests
from pydantic import ValidationError
from config.settings import INGESTOR_URL
from validators.output_validator import Output
from exceptions.custom_exceptions import ServiceValidationError
from config.logger import get_logger

logger = get_logger()

def send_data(data):
    try:
        # validate the data
        try:
            for case in data:
                Output(**case)
        except ValidationError as e:
            raise ServiceValidationError(errors=e)
        
        # send the data to the CovidDataIngestor service
        response = requests.post(INGESTOR_URL, json=data, timeout=10)
        response.raise_for_status()

        logger.info(f"Data sent successfully to {INGESTOR_URL}")

        return {"status_code": response.status_code, "response": response.json()}
    # the exception will be handled in the endpioint layer
    except Exception as e:
        raise e
