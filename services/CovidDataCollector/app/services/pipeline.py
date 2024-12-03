# app/services/data_validator.py
from services.data_validator import validate_datas
from services.data_creator import create_cases

def handle_request(data):
    """
    Accept the data from endpoint and process it.
    Collect the data from the request, validate it, and store it in the database.

    Args:
        data (dict): A dictionary containing the data to be collected.

    Returns:
        None, but it pipeline somtiomes raise exceptions, it will be handle in endpoint.
    """  
    # validate the data
    validate_datas(data)
  
    # store data into the database
    create_cases(data)
    