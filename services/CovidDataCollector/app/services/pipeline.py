# app/services/data_validator.py
from data_validator import validate_data
from data_creator import create_data

def handle_request(data):
    """
    Accept the data from endpoint and process it.
    Collect the data from the request, validate it, and store it in the database.

    Args:
        data (dict): A dictionary containing the data to be collected.

    Returns:
        dict : A dictionary containing the status of the data collection and a message.
    """
    validate_data(data)
    create_data(data)
    