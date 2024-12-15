import json
import pytest
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
from datetime import datetime

from config.settings import DB_URL
from utils.db.schema import covid_cases, cities, regions
from exceptions.custom_exceptions import DataDuplicateException
from pipeline.data_creator import create_case
from config.logger import get_logger


@pytest.fixture(scope="module")
def logger():
    return get_logger()


@pytest.fixture(scope="module")
def db_session():
    engine = create_engine(DB_URL)
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


# import test cases
with open("/test/cases/test_data_creator.json", encoding="utf-8") as f:
    test_cases = json.load(f)


def get_case_describes(case):
    return case["test_describes"]


@pytest.mark.parametrize("case", test_cases, ids=get_case_describes)
def test_data_creator(case, db_session, logger):
    """
    Test the data creator function to ensure it correctly inserts data into the database.

    Args:
        case (dict): A dictionary containing the test case data and expected results.
    """
    try:
        for row in case["data"]:
            row["date"] = datetime.strptime(row["date"], "%Y-%m-%d").date()
            create_case(row)
    # check dataduplicate exception is raised when inserting duplicate data
    except DataDuplicateException as e:
        logger.debug(f"Data creation failed. {str(e)}")
        assert str(e) == case["expected_response"]["message"]
        return

    # check the data in the database
    # get the city id
    city_query = select(cities).where(
        cities.c.name == case["expected_response"]["city"]
    )
    city_result = db_session.execute(city_query).fetchone()
    # check if city is not found in the database
    if city_result is None:
        logger.debug(
            f"City {case['expected_response']['city']} not found in the database."
        )
        assert (
            False
        ), f"City {case['expected_response']['city']} not found in the database."
    city_id = city_result.id

    #  get the region id
    region_query = select(regions).where(
        regions.c.city_id == city_id,
        regions.c.name == case["expected_response"]["region"],
    )
    region_result = db_session.execute(region_query).fetchone()
    # check if region is not found in the database
    if region_result is None:
        logger.debug(
            f"Region {case['expected_response']['region']} not found in the database."
        )
        assert (
            False
        ), f"Region {case['expected_response']['region']} not found in the database."
    region_id = region_result.id

    # get the covid cases data by expected data fields
    query = select(covid_cases).where(
        and_(
            covid_cases.c.date == datetime.strptime(case["expected_response"]["date"], "%Y-%m-%d").date(),
            covid_cases.c.city_id == city_id,
            covid_cases.c.region_id == region_id,
        )
    )
    result = db_session.execute(query).fetchone()
    # check if covid case is not found in the database
    if region_result is None:
        logger.debug(f"Covid case not found in the database.")
        assert False, f"Covid case not found in the database."

    assert result.date.strftime("%Y-%m-%d") == case["expected_response"]["date"]
    assert result.cases == case["expected_response"]["cases"]
    assert result.city_id == city_id
    assert result.region_id == region_id
    logger.debug("Data creation success.")
