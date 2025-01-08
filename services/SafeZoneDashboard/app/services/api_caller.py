import json
import requests
import time

from validators.schemas import NationalParameters, CityParameters, RegionParameters, APIResponse
from excecptions.custom import UnexceptedResponse
from config.settings import API_URL
from config.logger import get_logger

logger = get_logger()


def load_taiwan_geo():
    with open("/app/utils/geo_data/taiwan_geo_data.json", "r") as f:
        taiwan_geo_cache = json.load(f)
    return taiwan_geo_cache

last_exit_time = None

def general_update(model, path):
    
    global last_exit_time

    # 記錄進入時間
    enter_time = time.perf_counter()
    logger.info(f"Enter time: {enter_time:.6f}")

    # 計算前端反應時間（如果有上次的離開時間）
    if last_exit_time is not None:
        frontend_reaction_time = enter_time - last_exit_time
        logger.info(f"Frontend Reaction Time: {frontend_reaction_time:.6f} seconds")
    
    url = f"{API_URL}/{path}"
    response = requests.get(url, params=model.model_dump())

    # raise an error if the request was not successful by http status code
    response.raise_for_status()


    # 記錄離開時間
    exit_time = time.perf_counter()
    backend_reaction_time = exit_time - enter_time
    logger.info(f"Exit time: {exit_time:.6f}")
    logger.info(f"Backend Reaction Time: {backend_reaction_time:.6f} seconds")

    # 更新全局離開時間
    last_exit_time = exit_time

    # check if the request was successful, it should a model of APIResponse
    api_response = APIResponse(**response.json()).model_dump(exclude_none=True)
    # raise an error if the response status is not success
    if not api_response["success"]:
        raise UnexceptedResponse(api_response)
    # get the data from the response
    data = api_response["data"]
    return data

def update_region(now, city, region, interval, ratio):
    # create a RegionParameters model and validate the inputs
    model = RegionParameters(now=now, interval=interval, city=city, region=region, ratio=ratio)
    return general_update(model, "cases/region")

def update_city(now, city, interval, ratio):
    # create a CityParameters model and validate the inputs
    model = CityParameters(now=now, interval=interval, city=city, ratio=ratio)
    return general_update(model, "cases/city")

def update_national(now, interval):
    # create a NationalParameters model and validate the inputs
    model = NationalParameters(now=now, interval=interval)
    data = general_update(model, "cases/national")
    # check the content of the response data
    if data["end_date"] != now:
        raise UnexceptedResponse("The end date is unexpected")
    return data["aggregated_cases"]