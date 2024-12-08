# app/test/unit_test/test_data_validator
import json
import pytest
from services.data_validator import validate_datas
from config.logger import get_logger


@pytest.fixture(scope="module")
def logger():
    return get_logger()


# import test cases
with open("/test/cases/test_data_validator.json", encoding="utf-8") as f:
    test_cases = json.load(f)


def get_case_describes(case):
    return case["test_describes"]


# testing case by case
@pytest.mark.parametrize("case", test_cases, ids=get_case_describes)
def test_data_validator(case, logger):
    try:
        validate_datas(case["data"])
        assert True
    except Exception as e:
        assert str(e) == case["expected_response"]["message"]
        return
