# app/services/data_validator.py
from pipeline.data_creator import create_case

def handle_request(data):
    """
    Accept the data from endpoint and process it.
    Collect the data from the request, validate it, and store it in the database.

    Args:
        data (dict): A dictionary containing the data to be collected.

    Returns:
        None, but it pipeline somtiomes raise exceptions, it will be handle in endpoint.
    """    
    # store data into the database
    create_case(data)
    