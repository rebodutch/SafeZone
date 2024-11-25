# app/test/unit_test/test_data_validator
import json
import pytest
from services.data_validator import validate_data

# import test cases
with open("/tests/cases/test_data_validator.json", encoding="utf-8") as f:
    test_cases = json.load(f)

# testing case by case
@pytest.mark.parametrize("case", test_cases, ids=lambda case: case["test_describes"])
def test_data_validator(case):
    result = validate_data(case["data"])
    assert result["status"] == case["expected_filter_data"]["status"]
    assert result["message"] == case["expected_filter_data"]["message"] 