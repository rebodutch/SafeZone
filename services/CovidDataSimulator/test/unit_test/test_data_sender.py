import requests_mock
import json
import pytest
from services.data_sender import send_data
from config import CovidDataCollector_URL 

# import test cases
with open("/app/data/cases/test_data_sender.json", encoding="utf-8") as f:
    test_cases = json.load(f)

# testing case by case
@pytest.mark.parametrize("case", test_cases, ids=lambda case: case["test_describes"])
def test_send_data(case, requests_mock):
    mock_url = CovidDataCollector_URL
    # simulate request by requests_mock 
    requests_mock.post(mock_url, json=case["expected_response"], status_code=case["expected_status_code"])

    result = send_data(case["data"])

    print(result["response"] )

    assert result["status_code"] == case["expected_status_code"]
    assert result["response"] == case["expected_response"]

