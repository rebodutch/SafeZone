from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from utils.custom_exceptions.exceptions import (
    InvalidTaiwanCityException,
    InvalidTaiwanRegionException,
    DataDuplicateException,
)
from utils.models.covid_case import City, Region, CovidCase
from config.settings import DB_URL
from config.logger import get_logger

from utils.db.schema import cities, regions

logger = get_logger()


def create_cases(cases):
    """
    Create the cases in the database.

    Args:
        cases (list): A list of dictionaries, each containing the following keys:
            - city (str): The name of the city.
            - region (str): The name of the region.
            - date (str): The date of the case in 'YYYY-MM-DD' format.
            - cases (int): The number of cases.
    """    
    failed_cases_by_city = []
    failed_cases_by_region = []
    try:
        engine=create_engine(DB_URL)
        with sessionmaker(bind=engine)() as session:
            # foregin_id cache
            city_id_map = {}
            region_id_map = {}
            for case in cases:
                # check if city exist and cache its id
                if case["city"] not in city_id_map:
                    city = session.query(City).filter_by(name=case["city"]).first()
                    # if city not exist, add to failed_cases_by_city
                    if not city:
                        logger.error(f"City not found: {case['city']}")
                        failed_cases_by_city.append(case)
                        continue
                    city_id_map[case["city"]] = city.id
                # check if region exist and cache its id
                if case["region"] not in region_id_map:
                    region = (
                        session.query(Region)
                        .filter_by(
                            name=case["region"], city_id=city_id_map[case["city"]]
                        )
                        .first()
                    )
                    # if region not exist, add to failed_cases_by_region
                    if not region:
                        failed_cases_by_region.append(case)
                        continue
                    region_id_map[f"{case['city']}-{case['region']}"] = region.id

                # create covid case
                covid_case = CovidCase(
                    date=datetime.strptime(case["date"], "%Y-%m-%d").date(),
                    city_id=city_id_map[case["city"]],
                    region_id=region_id_map[f"{case["city"]}-{case["region"]}"],
                    cases=case["cases"],
                )
                logger.debug(f"Adding case: city={case["city"]}-{covid_case.city_id}, region={case["region"]}-{covid_case.region_id}, {covid_case.date}, {covid_case.cases}")
                session.add(covid_case)
                session.commit()

        # prevent the failed cases from being added to the database
        # let suuceessful cases be added to the database
        if failed_cases_by_city:
            logger.error(f"Failed cases by city: {failed_cases_by_city}")
            raise InvalidTaiwanCityException()
        if failed_cases_by_region:
            logger.error(f"Failed cases by region: {failed_cases_by_region}")
            raise InvalidTaiwanRegionException()
    # propagate exception to endpoint
    except IntegrityError as e:
        logger.error(f"Data already exists: {e}")
        raise DataDuplicateException()
    except Exception as e:
        raise e
