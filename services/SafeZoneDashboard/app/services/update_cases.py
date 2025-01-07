import datetime

from services.api_caller import load_taiwan_geo
from services.api_caller import update_national, update_city, update_region
from config.logger import get_logger

logger = get_logger()


def get_national_cases(interval):
    if interval not in ["1", "7"]:
        return 0
    now_date = datetime.date.today().strftime("%Y-%m-%d")
    # update national cases
    return update_national(now_date, interval)


def get_region_data(city, interval, ratio=False):
    # load taiwan geo data
    taiwan_geo_data = load_taiwan_geo()
    now_date = datetime.date.today().strftime("%Y-%m-%d")

    data = {}
    for region in taiwan_geo_data[city]:
        region_data = update_region(now_date, city, region, interval, ratio)
        if ratio:
            data[region] = region_data["cases_population_ratio"]
        else:
            data[region] = region_data["aggregated_cases"]
    return data


def get_city_data(interval, ratio=False):
    # load taiwan geo data
    taiwan_geo_data = load_taiwan_geo()
    now_date = datetime.date.today()

    data = {}
    for city in taiwan_geo_data.keys():
        city_data = update_city(now_date, city, interval, ratio)
        if ratio:
            data[city] = city_data["cases_population_ratio"]
        else:
            data[city] = city_data["aggregated_cases"]
    return data
