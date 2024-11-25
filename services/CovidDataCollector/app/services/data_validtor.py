# app/services/data_validator.py
import json
from datetime import datetime
from exceptions.custom_exceptions import InvalidTaiwanCityException
from exceptions.custom_exceptions import InvalidTaiwanRegionException
from exceptions.custom_exceptions import InvalidCasesNumberException
from exceptions.custom_exceptions import InvalidDataFormatException
from exceptions.custom_exceptions import MissingDataException
from exceptions.custom_exceptions import ExtraFieldException


def validate_date(input_date):
    if not isinstance(input_date, str):
        raise InvalidDataFormatException
    try:
        datetime.strptime(input_date, "%Y-%m-%d")
    except ValueError:
        raise InvalidDataFormatException


def validate_geo(input_city, input_region, geo_data):
    if not isinstance(input_city, str) or not isinstance(input_region, str):
        raise InvalidDataFormatException

    if input_city not in geo_data:
        raise InvalidTaiwanCityException
    if input_region not in geo_data[input_city]:
        raise InvalidTaiwanRegionException


def validate_cases(input_cases):
    if not isinstance(input_cases, int):
        raise InvalidDataFormatException
    if input_cases < 0:
        raise InvalidCasesNumberException


def validate_data(data):
    """
    Validate the data to ensure it is in the correct format.

    Args:
        data (dict): A dictionary containing the data to be validated.

    Returns:
        dict: A dictionary containing the status of the validation and a message.
    """
    # Check if all required fields are present in the data
    if (
        "date" not in data
        or "cases" not in data
        or "city" not in data
        or "region" not in data
    ):
        raise MissingDataException

    # Check if there are redundant fields in the data
    if len(data) > 4:
        raise ExtraFieldException

    # Check the values in every field in the data
    validate_date(data["date"])

    # Load geo data once
    with open("app/data/taiwan_geo_data.json", encoding="utf-8") as f:
        geo_data = json.load(f)
    validate_geo(data["city"], data["region"], geo_data)

    validate_cases(data["cases"])

    return {"status": "success", "message": "Data is valid"}
