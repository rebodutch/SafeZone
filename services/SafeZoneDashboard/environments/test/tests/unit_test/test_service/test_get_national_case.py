import json
import pytest
import responses
from freezegun import freeze_time
from pydantic import ValidationError
from requests.exceptions import ConnectionError

from services.update_cases import get_national_cases
from config.settings import API_URL


# define the fixture
# freeze the time to the target date
@pytest.fixture
def frozen_time():
    def _freeze_time(target_date):
        return freeze_time(target_date)

    return _freeze_time


# load the test cases from the file
def load_test_cases(file_name):
    test_case_path = "/test/cases/test_services/get_national_case/"
    with open(test_case_path + file_name, encoding="utf-8") as f:
        return json.load(f)


def get_case_describes(case):
    return case["test_describes"]


# test the update_cases function
@pytest.mark.parametrize(
    "case", load_test_cases("cases_success.json"), 
    ids=get_case_describes
)
@responses.activate
def test_update_cases(case, frozen_time):
    with frozen_time("2023-03-26"):
        # simulate request by requests_mock
        url = f"{API_URL}/{case["api_path"]}"
        url += f"?now={case["params"]["now"]}&interval={case["params"]["interval"]}"
        mock_response = case["expected"]["response"]["response"]
        status_code = case["expected"]["response"]["status_code"]
        responses.add(responses.GET, url, json=mock_response, status=status_code)
        # call the function
        data = get_national_cases(case["params"]["interval"])
        # assert the data's correctness
        assert data == case["expected"]["data"]

# test the update_cases function in response error scenarios
@pytest.mark.parametrize(
    "case", load_test_cases("cases_resp_error.json"), 
    ids=get_case_describes
)
@responses.activate
def test_update_cases_resp_error(case, frozen_time):
    with frozen_time("2023-03-26"):
        # simulate request by requests_mock
        url = f"{API_URL}/{case["api_path"]}"
        url += f"?now={case["params"]["now"]}&interval={case["params"]["interval"]}"
        mock_response = case["expected"]["response"]["response"]
        status_code = case["expected"]["response"]["status_code"]
        responses.add(responses.GET, url, json=mock_response, status=status_code)
        # call the function and assert the error
        with pytest.raises(ValidationError) as exc_info:
            get_national_cases("1")
        # check the error message
        errors = exc_info.value.errors()
        assert errors[0]["loc"] == tuple(case["expected"]["error"])

# test the update_cases function in network error scenarios
@pytest.mark.parametrize(
    "case", load_test_cases("cases_network_error.json"), 
    ids=get_case_describes
)
def test_update_cases_network_error(case, frozen_time):
    with frozen_time("2023-03-26"):
        # simulate request by requests_mock
        url = f"{API_URL}/{case["api_path"]}"
        url += f"?now={case["params"]["now"]}&interval={case["params"]["interval"]}"
        status_code = case["expected"]["response"]["status_code"]
        responses.add(responses.GET, url, 
                      status=status_code, body= ConnectionError(),)
        # call the function and assert the error
        with pytest.raises(ConnectionError) as exc_info:
            get_national_cases("1")