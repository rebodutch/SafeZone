import json
import pytest
import datetime
import random
import responses
from jinja2 import Template
from pydantic import ValidationError
from collections import defaultdict
from unittest.mock import patch
from freezegun import freeze_time

from callbacks.update_cases import update_map
from config.settings import API_URL


# define the fixture
# freeze the time to the target date
@pytest.fixture
def frozen_time():
    def _freeze_time(target_date):
        return freeze_time(target_date)

    return _freeze_time


# def generate_mocks(case):
#     mock_requests = []
#     mock_data = defaultdict(dict)
#     # generate mock request
#     params = case["params_template"]
#     # get the current date
#     date = datetime.date.today()
#     params["now"] = date.strftime("%Y-%m-%d")
#     for mock_city, mock_regions in case["mock_regions"].items():
#         for mock_region in mock_regions:
#             # set the query parameters
#             params["city"] = mock_city
#             params["region"] = mock_region

#             # generate the api url and add the query parameters
#             URL = f"{API_URL}/{case['api_path']}"
#             # add the query parameters (time relation)
#             URL += f"?now={params["now"]}&interval={params['interval']}"
#             # add the query parameters (geo relation)
#             URL += f"&city={params['city']}&region={params['region']}"
#             # add thequery parameters (ratio)
#             URL += f"&ratio={params['ratio']}"

#             # set the response parameters
#             start_date = date - datetime.timedelta(days=int(params["interval"]))
#             start_date = start_date.strftime("%Y-%m-%d")

#             # generate mock data for the request
#             if not params["ratio"]:
#                 mock_data[mock_city][mock_region] = {
#                     "start_date": start_date,
#                     "end_date": params["now"],
#                     "city": mock_city,
#                     "region": mock_region,
#                     "aggregated_cases": random.randint(0, 1000),
#                 }
#             else:
#                 mock_data[mock_city][mock_region] = {
#                     "start_date": start_date,
#                     "end_date": params["now"],
#                     "city": mock_city,
#                     "region": mock_region,
#                     "cases_population_ratio": round(random.uniform(0, 1), 5),
#                 }
#             # make a copy of the response template
#             response = case["expected"]["response_template"].copy()
#             response["data"] = mock_data[mock_city][mock_region]
#             response["detail"] = (
#                 f"Data returned successfully for dates {start_date} ~ {params["now"]}."
#             )
#             mack_request = {
#                 "request": {"url": URL, "json": response, "status_code": 200},
#             }
#             mock_requests.append(mack_request)
#     return (mock_requests, mock_data)


def generate_mocks(case, interval, ratio=False):
    mock_data, mock_requests = defaultdict(dict), []
    # generate mock data
    data_template = case["expected"]["data_template"]
    # generate mock request
    url_template = case["url_template"]
    response_template = case["expected"]["response_template"]

    date = datetime.date.today()
    date_str = date.strftime("%Y-%m-%d")
    for mock_city, regions in case["mock_regions"].items():
        for mock_region in regions:
            # simluated the different ratio feild
            if ratio:
                # it's should be generated before the context,
                # becasue the different render will cause the different result
                rand_ratio = round(random.uniform(0, 1), 5)
                # the context for the jinja2 template
                context = {
                    "now": date_str,
                    "start_date": (
                        date - datetime.timedelta(days=int(interval))
                    ).strftime("%Y-%m-%d"),
                    "mock_city": mock_city,
                    "mock_region": mock_region,
                    "cases_population_ratio": rand_ratio,
                }
                data = json.loads(Template(json.dumps(data_template)).render(context))
                # because the jinja2 template can't save the value in int type
                # so we need to assign the int value again for the mock_data
                data["cases_population_ratio"] = rand_ratio
            else:
                # it's should be generated before the context,
                # becasue the different render will cause the different result
                rand_cases = random.randint(0, 1000)
                # the context for the jinja2 template
                context = {
                    "now": date_str,
                    "start_date": (date - datetime.timedelta(days=14)).strftime(
                        "%Y-%m-%d"
                    ),
                    "mock_city": mock_city,
                    "mock_region": mock_region,
                    "aggregated_cases": rand_cases,
                }
                data = json.loads(Template(json.dumps(data_template)).render(context))
                # because the jinja2 template can't save the value in int type
                # so we need to assign the int value again for the mock_data
                data["aggregated_cases"] = rand_cases

            mock_data[mock_city][mock_region] = data
            # add other context
            context["ratio"] = ratio
            context["interval"] = interval
            context["API_URL"] = API_URL
            url = Template(json.dumps(url_template)).render(context).strip('"')
            response = Template(json.dumps(response_template)).render(context)
            response = json.loads(response)

            mock_requests.append({"url": url, "json": response, "status_code": 200})
    return mock_requests, mock_data


# load the test cases
def load_test_cases(file_name):
    test_case_path = "/test/cases/test_callback/test_update_map/"
    with open(test_case_path + file_name, encoding="utf-8") as f:
        return json.load(f)


# get the test case description
def get_case_describes(case):
    return case["test_describes"]


# test the update_cases function in correct scenarios
@patch("callbacks.update_cases.load_taiwan_geo")
@pytest.mark.parametrize(
    "case", load_test_cases("cases_success.json"), ids=get_case_describes
)
@responses.activate
def test_update_trends(mock_load_geo, case, frozen_time):
    mock_load_geo.return_value = case["mock_regions"]
    with frozen_time("2023-06-26"):
        interval = case["params"]["interval"]
        ratio = case["params"]["ratio"]
        # mock the requests
        mock_requests, mock_data = generate_mocks(case, interval, ratio)
        # simulate request by requests_mock
        for mock_request in mock_requests:
            url = mock_request["url"]
            mock_response = mock_request["json"]
            status_code = mock_request["status_code"]
            responses.add(responses.GET, url, json=mock_response, status=status_code)

        # call the function
        data = update_map(interval, ratio)
        # assert the data's correctness
        assert data == mock_data


# test the update_cases function in parameters error scenarios
@patch("callbacks.update_cases.load_taiwan_geo")
@pytest.mark.parametrize(
    "case", load_test_cases("cases_params_error.json"), ids=get_case_describes
)
def test_update_map_params_error(mock_load_geo, case, frozen_time):
    mock_load_geo.return_value = case["mock_regions"]
    interval = case["loc"]["interval"]
    # expect the validation error beacuse the interval is not in the correct format
    with pytest.raises(ValidationError):
        update_map(interval)


# test the update_cases function in response error scenarios
@patch("callbacks.update_cases.load_taiwan_geo")
@pytest.mark.parametrize(
    "case", load_test_cases("cases_resp_error.json"), ids=get_case_describes
)
@responses.activate
def test_update_map_params_error(mock_load_geo, case, frozen_time):
    mock_load_geo.return_value = case["mock_regions"]
    with frozen_time("2023-06-26"):
        interval = case["params"]["interval"]
        ratio = case["params"]["ratio"]
        # mock the requests
        mock_requests, mock_data = generate_mocks(case, interval, ratio)
        # simulate request by requests_mock
        for mock_request in mock_requests:
            url = mock_request["url"]
            mock_response = mock_request["json"]
            status_code = mock_request["status_code"]
            responses.add(responses.GET, url, json=mock_response, status=status_code)
        # expect the validation error beacuse the response missing the end_date field 
        with pytest.raises(ValidationError):
            update_map(interval)

