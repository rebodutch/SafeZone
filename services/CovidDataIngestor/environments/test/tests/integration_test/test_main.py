import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from utils.db.schema import cities, regions, covid_cases
from config.settings import DB_URL
from config.logger import get_logger
from main import app

client = TestClient(app)

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

# Import test cases
with open("/test/cases/test_integration.json", encoding="utf-8") as f:
    test_cases = json.load(f)

def get_case_describes(case):
    return case["test_describes"]

# Testing case by case
@pytest.mark.parametrize("case", test_cases, ids=get_case_describes)
def test_data_product(case, db_session, logger):
    if "content_type" in case:
        result = client.post("/collect", json=case["data"], headers={"Content-Type": case["content_type"]})
    else:
        result = client.post("/collect", json=case["data"])
   
    # the error cases
    if result.status_code != 200:
        assert result.status_code == case["expected_response"]["status_code"]
        assert result.json()["detail"] == case["expected_response"]["message"]
    else:    
        # check the data in the database
        for row in case["data"]:
            # get the city id
            city_query = select(cities).where(
                cities.c.name == row["city"]
            )
            city_result = db_session.execute(city_query).fetchone()
            # check if the city is in the database
            if city_result is None:
                assert False, f"City '{row['city']}' not found in the database"
            city_id = city_result.id
            
            # get the region id
            region_query = select(regions).where(
                regions.c.name == row["region"],
                regions.c.city_id == city_id)
            region_result = db_session.execute(region_query).fetchone()
            # check if the region is in the database
            if region_result is None:
                assert False, f"Region '{row['region']}' not found in the database"
            region_id = region_result.id
            
            # get the covid cases data by expected data fields
            query = select(covid_cases).where(
                covid_cases.c.city_id == city_id,
                covid_cases.c.region_id == region_id,
                covid_cases.c.date == row["date"],
                covid_cases.c.cases == row["cases"])
            if db_session.execute(query).fetchone() is None:
                assert False, "Covid case data not found in the database"
