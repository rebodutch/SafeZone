import os
import requests

# Get the CovidDataCollector URL from environment variables
CovidDataCollector_url = os.getenv("CovidDataCollector_URL")

def send_data(data):
    """
    Send a single data entry to the CovidDataCollector.
    
    Args:
        data (pd.Series): A single row of data to be sent.
    """
    # Sending data to CovidDataCollector as JSON
    response = requests.post(CovidDataCollector_url, json=data.to_dict())
    print(f"Data sent. Status Code: {response.status_code}")

def send_data_batch(data_batch):
    """
    Send multiple data entries to the CovidDataCollector in batch.
    
    Args:
        data_batch (pd.DataFrame): A batch of data entries to be sent.
    """
    # Convert the entire DataFrame to a list of dictionaries, then send as a single request
    data_list = data_batch.to_dict(orient='records')
    response = requests.post(CovidDataCollector_url, json=data_list)
    print(f"Batch data sent. Status Code: {response.status_code}")