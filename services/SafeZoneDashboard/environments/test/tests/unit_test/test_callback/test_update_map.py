import json
import pytest
import requests_mock
from freezegun import freeze_time

from callbacks.update_cases import update_map
from callbacks.api_caller import load_taiwan_geo
from config.settings import API_URL


# define the fixture
# freeze the time to the target date
@pytest.fixture
def frozen_time():
    def _freeze_time(target_date):
        return freeze_time(target_date)
    return _freeze_time
# load the geo data from the file
@pytest.fixture
def taiwan_geo_cache():
    with open("/app/utils/geo_data/taiwan_geo_data.json", "r") as f:
        taiwan_geo_cache = json.load(f)
    return taiwan_geo_cache


with open("/test/cases/test_callback/test_update_map.json", encoding="utf-8") as f:
    test_cases = json.load(f)

def get_case_describes(case):
    return case["test_describes"]

# test the update_cases function
@pytest.mark.parametrize("case", test_cases, ids=get_case_describes)
def test_update_map(case, requests_mock, frozen_time, taiwan_geo_cache):
    with frozen_time("2023-03-26"):
        # simulate request by requests_mock
        # requests_mock.get(
        #     f"{API_URL}/{case["api_path"]}?now={case["params"]["now"]}&interval={case["params"]["interval"]}",
        #     json=case["expected"]["response"]["response"],
        #     status_code=case["expected"]["response"]["status_code"],
        # )
        # # call the function
        # data = update_cases()
        # print(data)
        # # assert the data's correctness
        # assert data == case["expected"]["data"]
        assert True