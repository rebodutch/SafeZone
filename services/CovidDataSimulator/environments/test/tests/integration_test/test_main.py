import json
import pytest
from fastapi.testclient import TestClient
from config.settings import CovidDataCollector_URL
from main import app

client = TestClient(app)

# Import test cases
with open("/test/cases/test_integration.json", encoding="utf-8") as f:
    test_cases = json.load(f)


# Testing case by case
@pytest.mark.parametrize("case", test_cases, ids=lambda case: case["test_describes"])
def test_data_product(case, requests_mock):

    endpoint = case["endpoint"]

    # Mock CovidDataCollector behavior by returning a predefined response if 'expected_response' is present in the test case
    if "expected_response" in case:
        mock_response = case["expected_response"]
        requests_mock.post(CovidDataCollector_URL, json=mock_response)
    else:
        requests_mock.post(CovidDataCollector_URL, json={})

    # Handle daily requests
    if endpoint == "/simulate/daily":
        date = case.get("date", "")
        if not date:
            response = client.get("/simulate/daily")
        else:
            response = client.get(f"/simulate/daily?date={date}")
        assert response.status_code == case["expected_status_code"]

        if "expected_response" in case:
            assert response.json() == case["expected_response"]

    # Handle interval requests
    # Check if both start_date and end_date are provided in the test case
    elif endpoint == "/simulate/interval":
        start_date = case.get("start_date", "")
        end_date = case.get("end_date", "")
        if not (start_date and end_date):
            # If either start_date or end_date is missing, make a request without query parameters
            response = client.get("/simulate/interval")
        else:
            # If both start_date and end_date are provided, make a request with the query parameters
            response = client.get(
                f"/simulate/interval?start_date={start_date}&end_date={end_date}"
            )
        assert response.status_code == case["expected_status_code"]

        if "expected_response" in case:
            assert response.json() == case["expected_response"]

    # Handle endpoints that are not /simulate/daily or /simulate/interval
    else:
        response = client.get(endpoint)
        assert response.status_code == case["expected_status_code"]
