import json
import pytest
import requests_mock
import datetime
import random
from collections import defaultdict
from unittest.mock import patch
from freezegun import freeze_time

from callbacks.update_cases import update_trends
from config.settings import API_URL


# define the fixture
# freeze the time to the target date
@pytest.fixture
def frozen_time():
    def _freeze_time(target_date):
        return freeze_time(target_date)

    return _freeze_time


with open("/test/cases/test_callback/test_update_trends.json", encoding="utf-8") as f:
    test_cases = json.load(f)


def get_case_describes(case):
    return case["test_describes"]


def generate_mocks(case):
    mock_requests = []
    mock_data = defaultdict(dict)
    # generate mock request

    params = case["params_template"]
    for delta in [0, 15, 30, 45, 60, 75, 90]:
        date = datetime.date.today() - datetime.timedelta(days=delta)
        params["now"] = date.strftime("%Y-%m-%d")
        for mock_city in case["mock_cities"]:
            params["city"] = mock_city
            URL = f"{API_URL}/{case['api_path']}"
            URL += f"?now={params["now"]}&city={params['city']}&interval={params['interval']}"

            # generate mock data for the request
            start_date = date - datetime.timedelta(days=14)
            mock_data[params["now"]][mock_city] = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": params["now"],
                "city": mock_city,
                "aggregated_cases": random.randint(0, 1000),
            }
            # make a copy of the response template
            response = case["expected"]["response_template"].copy()
            response["data"] = mock_data[params["now"]][mock_city]
            response["detail"] = (
                f"Data returned successfully for dates {start_date.strftime("%Y-%m-%d")} ~ {params["now"]}."
            )
            mack_request = {
                "request": {"url": URL, "json": response, "status_code": 200},
            }
            mock_requests.append(mack_request)
    return (mock_requests, mock_data)


mock_geo_data = {"台北市": {}, "高雄市": {}}


# test the update_cases function
@patch("callbacks.update_cases.load_taiwan_geo", return_value=mock_geo_data)
@pytest.mark.parametrize("case", test_cases, ids=get_case_describes)
def test_update_trends(mock_geo_data, case, requests_mock, frozen_time):
    with frozen_time("2023-06-26"):
        # mock the requests
        mock_requests, mock_data = generate_mocks(case)
        # simulate request by requests_mock
        for mock_request in mock_requests:
            requests_mock.get(**mock_request["request"])
        # call the function
        data = update_trends()
        # assert the data's correctness
        assert data == mock_data
