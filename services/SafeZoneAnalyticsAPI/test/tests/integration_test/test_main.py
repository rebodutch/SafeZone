import json
import csv
import logging
from datetime import datetime

import pytest # type: ignore
from fastapi.testclient import TestClient # type: ignore
from sqlalchemy import create_engine, select, and_ # type: ignore
from sqlalchemy.orm import Session # type: ignore

from utils.db.schema import cities, regions, covid_cases # type: ignore
from config.settings import DB_URL # type: ignore
from main import create_app # type: ignore

# Fixtures
@pytest.fixture(scope="module")
def client():
    app = create_app()
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def logger():
    return logging.getLogger("test_integration_service")

def init_db():
    with open("/data/test_data.csv", encoding="utf-8") as f:
        init_data = csv.DictReader(f)
        # Skip the header   
        engine = create_engine(DB_URL)
        with Session(engine) as session:
            for row in init_data:
                city = row["city"]
                region = row["region"]
                date = row["date"]
                cases = row["cases"]

                print(f"city: {city}, region: {region}, date: {date}, cases: {cases}")

                # get city_id and region
                select_city = select(cities).where(cities.c.name == city)
                city_result = session.execute(select_city).fetchone()
                city_id = city_result.id
                
                select_region = select(regions).where(  
                    and_(regions.c.city_id == city_id, regions.c.name == region)
                )       
                region_result = session.execute(select_region).fetchone()
                region_id = region_result.id    

                print(f"city_id: {city_id}, region_id: {region_id}")
                # insert covid cases data   
                insert_stmt = covid_cases.insert().values(
                    date=datetime.strptime(date, "%Y-%m-%d"),
                    cases=cases,
                    city_id=city_id,
                    region_id=region_id,
                )
                session.execute(insert_stmt)
            session.commit()
        engine.dispose()  # Ensure the engine is disposed after use

# init database
init_db()

# Import test cases
with open("/test/cases/test_integration.json", encoding="utf-8") as f:
    test_cases = json.load(f)

def get_case_describes(case):
    return case["test_describes"]

# Testing case by case
@pytest.mark.parametrize("case", test_cases, ids=get_case_describes)
def test_data_product(case, client, logger):
    response = client.get(case["endpoint"], params=case["params"])
    assert response.status_code == case["expected"]["status_code"]

    # remove timestamp from response for comparison
    response_body = response.json()
    if "timestamp" in response_body:
        del response_body["timestamp"]

    # remove items if value is None
    if "data" in response_body:
        # remove items with None values from data
        response_body["data"] = {k: v for k, v in response_body["data"].items() if v is not None}
    response_body = {k: v for k, v in response_body.items() if v is not None}
    print(f"response_body: {response_body}")

    assert response_body == case["expected"]["response"]