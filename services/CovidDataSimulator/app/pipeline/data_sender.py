# app/services/data_sender.py
import requests
from pydantic import ValidationError
from config.settings import INGESTOR_URL
from validators.service_validator import OutputValidator
from exceptions.custom_exceptions import ServiceValidationError
from config.logger import get_logger

logger = get_logger()


def send_data(data):
    # validate the data
    try:
        for case in data:
            OutputValidator(**case)
            # send the data to the CovidDataIngestor service
            logger.debug(f"Sending the case = {case} to ingrstor.")
            
            requests.post(INGESTOR_URL, json=case, timeout=10)

            logger.debug(f"Case = {case} sent to ingrstor.")
            
    except ValidationError as e:
        raise ServiceValidationError(errors=e)
