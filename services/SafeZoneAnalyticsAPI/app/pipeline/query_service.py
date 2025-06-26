import logging

from sqlalchemy import create_engine, select, func  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from utils.db.schema import covid_cases
from exceptions.custom import InvalidTaiwanCityException, InvalidTaiwanRegionException
from config.settings import DB_URL

logger = logging.getLogger(__name__)

RATIO_FACTOR = 10000  # used to calculate cases to population ratio


def query_cases(db_session, geo_cache, populations_cache, params):
    if "city" in params and "region" in params:
        result = query_cases_by_region(db_session, geo_cache, populations_cache, params)
    elif "city" in params:
        result = query_cases_by_city(db_session, geo_cache, populations_cache, params)
    else:
        result = query_cases_national(db_session, params)
    return result


def query_cases_by_region(Session, geo_cache, populations_cache, params):
    logger.debug(f"Query region cases with {params}.")

    with Session() as session:
        # check if city and region are valid
        if params["city"] not in geo_cache:
            raise InvalidTaiwanCityException(params["city"])
        if params["region"] not in geo_cache[params["city"]][1]:
            raise InvalidTaiwanRegionException(params["city"], params["region"])

        city_id = geo_cache[params["city"]][0]
        region_id = geo_cache[params["city"]][1][params["region"]]

        # query cases by region
        query = select(func.sum(covid_cases.c.cases).label("total_cases")).where(
            covid_cases.c.date >= params["start_date"],
            covid_cases.c.date <= params["end_date"],
            covid_cases.c.city_id == city_id,
            covid_cases.c.region_id == region_id,
        )
        cases = session.execute(query).scalar()
        cases = cases if cases else 0

    logger.debug(f"Query region cases successful with {params}.")

    if "ratio" in params and params["ratio"]:
        # calculate cases to population ratio
        population = populations_cache[city_id][region_id]
        cases = round(cases * RATIO_FACTOR / population, 5)

        return {
            "start_date": params["start_date"].strftime("%Y-%m-%d"),
            "end_date": params["end_date"].strftime("%Y-%m-%d"),
            "city": params["city"],
            "region": params["region"],
            "cases_population_ratio": cases,
        }
    else:
        return {
            "start_date": params["start_date"].strftime("%Y-%m-%d"),
            "end_date": params["end_date"].strftime("%Y-%m-%d"),
            "city": params["city"],
            "region": params["region"],
            "aggregated_cases": cases,
        }


def query_cases_by_city(Session, geo_cache, populations_cache, params):
    logger.debug(f"Query city case with {params}.")

    with Session() as session:
        # check if city is valid
        if params["city"] not in geo_cache:
            raise InvalidTaiwanCityException(params["city"])

        city_id = geo_cache[params["city"]][0]
        # query cases by city
        query = select(func.sum(covid_cases.c.cases).label("total_cases")).where(
            covid_cases.c.date >= params["start_date"],
            covid_cases.c.date <= params["end_date"],
            covid_cases.c.city_id == city_id,
        )
        cases = session.execute(query).scalar()
        cases = cases if cases else 0

    logger.debug(f"Query city cases successful with {params}.")

    if "ratio" in params and params["ratio"]:
        city_populations = 0
        for _, population in populations_cache[city_id].items():
            city_population += population
        # calculate cases to population ratio
        population = city_populations
        cases = round(cases * RATIO_FACTOR / population, 5)

        return {
            "start_date": params["start_date"].strftime("%Y-%m-%d"),
            "end_date": params["end_date"].strftime("%Y-%m-%d"),
            "city": params["city"],
            "cases_population_ratio": cases,
        }

    else:
        return {
            "start_date": params["start_date"].strftime("%Y-%m-%d"),
            "end_date": params["end_date"].strftime("%Y-%m-%d"),
            "city": params["city"],
            "aggregated_cases": cases,
        }


def query_cases_national(Session, params):
    logger.debug(f"Querying national cases with {params}.")

    with Session() as session:
        #  query cases for the whole country
        query = select(func.sum(covid_cases.c.cases).label("total_cases")).where(
            covid_cases.c.date >= params["start_date"],
            covid_cases.c.date <= params["end_date"],
        )
        cases = session.execute(query).scalar()
        cases = cases if cases else 0

    logger.debug(f"Query national cases successful with {params}.")

    return {
        "start_date": params["start_date"].strftime("%Y-%m-%d"),
        "end_date": params["end_date"].strftime("%Y-%m-%d"),
        "aggregated_cases": cases,
    }
