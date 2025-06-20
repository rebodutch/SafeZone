# /test/unit_test/test_data_sender
import json
import pytest

from config.settings import INGESTOR_URL
from config.logger import get_logger
from pipeline.data_sender import send_data

@pytest.fixture(scope="module")
def logger():
    return get_logger()

# import test cases
with open("/test/cases/test_data_sender.json", encoding="utf-8") as f:
    test_cases = json.load(f)

# testing case by case
@pytest.mark.parametrize("case", test_cases, ids=lambda case: case["test_describes"])
def test_send_data(case, requests_mock, logger):
    mock_url = INGESTOR_URL
    # simulate request by requests_mock 
    requests_mock.post(mock_url, json=case["expected_response"], status_code=case["expected_status_code"])
    try:
        send_data(case["data"])
        # if no exception is raised, the test is successful
        logger.debug("Data sending success.")
        assert True
    except Exception as e:  
        # if an exception is raised, the test is failed
        logger.debug(f"Data sending failed. {str(e)}")
        assert False, f"Data sending failed. {str(e)}"
