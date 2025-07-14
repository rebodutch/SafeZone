import json
import random
from datetime import date, timedelta

import pytest # type: ignore
import responses # type: ignore
from jinja2 import Template
from unittest.mock import patch
from pydantic import ValidationError # type: ignore
from freezegun import freeze_time # type: ignore

from services.update_cases import get_city_data
from config.settings import API_URL


# define the fixture
# freeze the time to the target date
@pytest.fixture
def frozen_time():
    def _freeze_time(target_date):
        return freeze_time(target_date)

    return _freeze_time

def generate_mocks(case):
    mock_data, mock_requests = {}, []
    # generate mock request
    url_template = case["url_template"]
    response_template = case["expected"]["response_template"]

    mock_date = date.today()
    for mock_city in case["mock_cities"].keys():
        # it's should be generated before the context,
        # becasue the different render will cause the different result
        rand_cases = random.randint(0, 1000)
        date_str = mock_date.strftime("%Y-%m-%d")
        # the context for the jinja2 template
        context = {
            "now": date_str,
            "start_date": (mock_date - timedelta(days=7)).strftime("%Y-%m-%d"),
            "mock_city": mock_city,
            "interval": 7,
            "aggregated_cases": rand_cases,
        }
        mock_data[mock_city] = context["aggregated_cases"]
   
        context["API_URL"] = API_URL
        url = Template(json.dumps(url_template)).render(context).strip('"')
        response = Template(json.dumps(response_template)).render(context)
        response = json.loads(response)

        mock_requests.append({"url": url, "json": response, "status_code": 200})
    return mock_requests, mock_data


# load the test cases from the file
def load_test_cases(file_name):
    test_case_path = "/test/cases/test_services/get_city_data/"
    with open(test_case_path + file_name, encoding="utf-8") as f:
        return json.load(f)


def get_case_describes(case):
    return case["test_describes"]


# test the update_trends function
@patch("services.update_cases.load_taiwan_admin")
@pytest.mark.parametrize(
    "case", load_test_cases("cases_success.json"), ids=get_case_describes
)
@responses.activate
def test_update_trends(mock_load_geo, case, frozen_time):
    mock_load_geo.return_value = case["mock_cities"]
    mock_date = "2023-06-26"

    with frozen_time(mock_date):
        # mock the requests
        mock_requests, mock_data = generate_mocks(case)

        # simulate request by requests_mock
        for mock_request in mock_requests:
            url = mock_request["url"]
            status_code = mock_request["status_code"]
            mock_response = mock_request["json"]
            responses.add(responses.GET, url, json=mock_response, status=status_code)

        # call the function
        data = get_city_data(mock_date, "7")
        # # assert the data's correctness
        assert data == mock_data


# test the update_trends function with the error response
@patch("services.update_cases.load_taiwan_admin")
@pytest.mark.parametrize(
    "case", load_test_cases("cases_resp_error.json"), ids=get_case_describes
)
@responses.activate 
def test_update_trends_response_error(mock_load_geo, case, frozen_time):
    mock_load_geo.return_value = case["mock_cities"]
    mock_date = "2023-06-26"

    with frozen_time(mock_date):
        # mock the requests
        mock_requests, _ = generate_mocks(case)

        # simulate request by requests_mock
        for mock_request in mock_requests:
            url = mock_request["url"]
            status_code = mock_request["status_code"]
            mock_response = mock_request["json"]
            responses.add(responses.GET, url, json=mock_response, status=status_code)

        # missing the field "end_date" in the response, it should raise the validationerror
        with pytest.raises(ValidationError):
            _ = get_city_data(mock_date, "7")
