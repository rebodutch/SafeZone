import json
import pytest
from sqlalchemy import create_engine
from services.data_creator import create_data
from db.schema import covid_cases

# import test cases
with open("tests/cases/test_data_creator.json", encoding="utf-8") as f:
    test_cases = json.load(f)

# create a table for testing
engine = create_engine("sqlite:///:memory:")

# testing case by case
@pytest.mark.parametrize("case", test_cases, ids=lambda case: case["test_describes"])
def test_data_creator(case):
    """
    Test the data creator function to ensure it correctly inserts data into the database.
    
    Args:
        case (dict): A dictionary containing the test case data and expected results.
    """
    # Test if insertion is successful
    with engine.connect() as connection:
        create_data(connection, case["data"])
        
        query = covid_cases.select().where(covid_cases.c.date == case["expected_data"]["date"])
        result = connection.execute(query).fetchone()

    assert result["date"] == case["expected_data"]["date"]
    assert result["cases"] == case["expected_data"]["cases"]
    assert result["city"] == case["expected_data"]["city"]
    assert result["region"] == case["expected_data"]["region"]