import json
import datetime

from services.api_caller import update_national, update_city, update_region
from config.logger import get_logger
from config.time_manager import get_now

logger = get_logger()

taiwan_admin_cache = None

def load_taiwan_admin():
    global taiwan_admin_cache
    if not taiwan_admin_cache:
        with open("/app/utils/geo_data/administrative/taiwan_admin.json", "r") as f:
            taiwan_admin_cache = json.load(f)
    return taiwan_admin_cache


def get_national_cases(interval):
    if interval not in ["1", "7"]:
        return 0
    now_date = get_now().strftime("%Y-%m-%d")
    # update national cases
    return update_national(now_date, interval)


def get_region_data(city, interval, ratio=False):
    # load taiwan geo data
    taiwan_admin = load_taiwan_admin()
    now_date = get_now().strftime("%Y-%m-%d")

    data = {}
    for region in taiwan_admin[city]:
        region_data = update_region(now_date, city, region, interval, ratio)
        if ratio:
            data[region] = region_data["cases_population_ratio"]
        else:
            data[region] = region_data["aggregated_cases"]
    return data


def get_city_data(interval, ratio=False):
    # load taiwan geo data
    taiwan_admin = load_taiwan_admin()
    now_date = get_now().strftime("%Y-%m-%d")

    data = {}
    for city in taiwan_admin.keys():
        city_data = update_city(now_date, city, interval, ratio)
        if ratio:
            data[city] = city_data["cases_population_ratio"]
        else:
            data[city] = city_data["aggregated_cases"]
    return data
