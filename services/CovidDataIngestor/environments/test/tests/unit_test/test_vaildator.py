# app/test/unit_test/test_data_validator
import json
import pytest
from pydantic import ValidationError

from validators.api_validator import CollectValidator
from config.logger import get_logger


@pytest.fixture(scope="module")
def logger():
    return get_logger()


# import test cases
with open("/test/cases/test_validator.json", encoding="utf-8") as f:
    test_cases = json.load(f)


def get_case_describes(case):
    return case["test_describes"]


# testing case by case
@pytest.mark.parametrize("case", test_cases, ids=get_case_describes)
def test_data_validator(case, logger):
    try:
        for row in case["data"]:
            CollectValidator(**row)
        logger.debug("Data validation success.")
        assert True
    except Exception as e:
        if isinstance(e, ValidationError):
            logger.debug(f"Data validation failed. {str(e)}")
            assert True, f"Data validation failed. {str(e)}"
        else:
            logger.debug(f"Raise an unexpected exception. {str(e)}")
            assert False, f"Raise an unexpected exception. {str(e)}"
