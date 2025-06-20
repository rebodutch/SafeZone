from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from utils.db.orm import City, Region, CovidCase
from exceptions.custom_exceptions import (
    InvalidTaiwanCityException,
    InvalidTaiwanRegionException,
    DataDuplicateException,
)
from config.settings import DB_URL
from config.logger import get_logger

logger = get_logger()


def create_case(case):
    """
    Create the cases in the database.

    Args:
        cases (list): A list of dictionaries, each containing the following keys:
            - city (str): The name of the city.
            - region (str): The name of the region.
            - date (str): The date of the case in 'YYYY-MM-DD' format.
            - cases (int): The number of cases.
    """
    try:
        logger.debug(f"Creating case: {case}")

        engine = create_engine(DB_URL)
        with sessionmaker(bind=engine)() as session:
            # check if city exist and cache its id
            city = session.query(City).filter_by(name=case["city"]).first()
            # if city not exist, raise exception
            if not city:
                raise InvalidTaiwanCityException()

            # check if region exist and cache its id
            region = (
                session.query(Region)
                .filter_by(name=case["region"], city_id=city.id)
                .first()
            )
            # if region not exist, raise exception
            if not region:
                raise InvalidTaiwanRegionException()

            # create covid case
            covid_case = CovidCase(
                date=case["date"],
                city_id=city.id,
                region_id=region.id,
                cases=case["cases"],
            )
            session.add(covid_case)
            session.commit()

        logger.debug(f"Case created: {case}")

    # handle exception is rasied by inserted the duplicate data into database
    except IntegrityError as e:
        raise DataDuplicateException()
    except Exception as e:
        raise e
