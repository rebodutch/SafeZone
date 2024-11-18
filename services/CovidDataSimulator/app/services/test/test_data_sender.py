import os
import pandas as pd
from services import data_sender
from unittest.mock import patch

# Get the CovidDataCollector URL from environment variables
CovidDataCollector_url = os.getenv("CovidDataCollector_URL")
# Tests
@patch('requests.post')
def test_send_data(mock_post):
    # Prepare mock data
    data = pd.Series({"個案研判日": "2023-03-20", "縣市": "台北市", "鄉鎮": "信義區", "確定病例數": 2})
    
    # Call the function
    data_sender.send_data(data)
    
    # Assert that requests.post was called once with the correct parameters
    mock_post.assert_called_once_with(CovidDataCollector_url, json=data.to_dict())

@patch('requests.post')
def test_send_data_batch(mock_post):
    # Prepare mock batch data
    data_batch = pd.DataFrame({
        "個案研判日": ["2023-03-20", "2023-03-21"],
        "縣市": ["台北市", "新北市"],
        "鄉鎮": ["信義區", "之山區"],
        "確定病例數": [10, 15]
    })
    
    # Call the function
    data_sender.send_data_batch(data_batch)
    
    # Assert that requests.post was called once with the correct parameters
    data_list = data_batch.to_dict(orient='records')
    mock_post.assert_called_once_with(CovidDataCollector_url, json=data_list)