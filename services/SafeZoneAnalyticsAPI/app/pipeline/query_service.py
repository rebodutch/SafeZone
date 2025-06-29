from datetime import datetime

from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker

from utils.db.orm import City, Region
from utils.db.schema import populations, covid_cases
from exceptions.custom import InvalidTaiwanCityException, InvalidTaiwanRegionException
from config.settings import DB_URL
from config.logger import get_logger

logger = get_logger()

# caches
# geo_cache stores city-region mapping in the format:
# city -> (city_id, {region_name -> region_id})
geo_cache = {}
# populations_cache stores population data in the format:
# city_id -> {region_id -> population}
populations_cache = {}


def load_city_region_cache():
    engine = create_engine(DB_URL)
    with sessionmaker(bind=engine)() as session:
        geo_cache.clear()

        results = (
            session.query(City, Region)
            .outerjoin(Region, Region.city_id == City.id)
            .all()
        )
        for city, region in results:
            if city.name not in geo_cache:
                geo_cache[city.name] = (city.id, {})
            if region:
                geo_cache[city.name][1][region.name] = region.id
    logger.debug("City-region cache loaded successfully.")


def load_populations_cache():
    engine = create_engine(DB_URL)
    with sessionmaker(bind=engine)() as session:
        populations_cache.clear()
        select_stmt = select(
            populations.c.city_id, populations.c.region_id, populations.c.population
        )
        for city_id, region_id, population in session.execute(select_stmt):
            # print(f"city_id: {city_id}, region_id: {region_id}, population: {population}")
            if city_id not in populations_cache:
                populations_cache[city_id] = {}
            populations_cache[city_id][region_id] = population
    logger.debug("population cache loaded successfully.")


def query_population(city_id, region_id=None):
    if region_id:
        return populations_cache[city_id][region_id]
    aggregated_population = 0
    for region_id, population in populations_cache[city_id].items():
        aggregated_population += population
    return aggregated_population


def query_cases(**params):
    if "city" in params and "region" in params:
        result = query_cases_by_region(**params)
    elif "city" in params:
        result = query_cases_by_city(**params)
    else:
        result = query_cases_national(**params)

    return result


def query_cases_by_region(**params):
    logger.debug(f"Query region cases with {params}.")

    engine = create_engine(DB_URL)
    with sessionmaker(bind=engine)() as session:
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
        population = query_population(city_id, region_id)
        cases = round(cases * 10000 / population, 5)

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


def query_cases_by_city(**params):
    logger.debug(f"Query city case with {params}.")

    engine = create_engine(DB_URL)
    with sessionmaker(bind=engine)() as session:
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
        # calculate cases to population ratio
        population = query_population(city_id)
        cases = round(cases * 10000 / population, 5)

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


def query_cases_national(**params):
    logger.debug(f"Querying national cases with {params}.")

    engine = create_engine(DB_URL)
    with sessionmaker(bind=engine)() as session:
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
