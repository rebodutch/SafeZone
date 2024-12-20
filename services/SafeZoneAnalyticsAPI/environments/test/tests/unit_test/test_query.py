import json
import csv
import pytest
from datetime import datetime
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
# debug use
# from sqlalchemy import inspect, text

from utils.db.schema import covid_cases, cities, regions
from pipeline.query_service import query_cases, load_city_region_cache, load_populations_cache
from exceptions.custom import InvalidTaiwanRegionException, InvalidTaiwanCityException
from config.logger import get_logger
from config.settings import DB_URL


@pytest.fixture(scope="module")
def logger():
    return get_logger()

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
        # raise Exception("Init database successfully")
# init database
init_db()
# import test cases
with open("/test/cases/test_query_service.json", encoding="utf-8") as f:
    test_cases = json.load(f)

def get_case_describes(case):
    return case["test_describes"]

@pytest.mark.parametrize("case", test_cases, ids=get_case_describes)
def test_data_creator(case, logger):
    try:
        # init the caches
        load_city_region_cache()
        load_populations_cache()

        # date type conversion
        case["params"]["start_date"] = datetime.strptime(case["params"]["start_date"], "%Y-%m-%d").date()
        case["params"]["end_date"] = datetime.strptime(case["params"]["end_date"], "%Y-%m-%d").date()
        
        print(case)
        # query cases
        query_result = query_cases(**case["params"])
        assert query_result == case["expected"]["query_result"]
    except InvalidTaiwanRegionException:
        assert case["expected"]["exception"] == "InvalidTaiwanRegionException"
    except InvalidTaiwanCityException:
        assert case["expected"]["exception"] == "InvalidTaiwanCityException"
