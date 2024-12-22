import json
import requests
from pydantic import ValidationError

from validators.schemas import NationalParameters, CityParameters, RegionParameters, APIResponse
from config.settings import API_URL


def load_taiwan_geo():
    with open("/app/utils/geo_data/taiwan_geo_data.json", "r") as f:
        taiwan_geo_cache = json.load(f)
    return taiwan_geo_cache

def general_update(model, path):
    response = requests.get(f"{API_URL}/{path}", params=model.model_dump())
    # raise an error if the request was not successful by http status code
    response.raise_for_status()
    # check if the request was successful, it should a model of APIResponse
    try:
        api_response = APIResponse(**response.json()).model_dump(exclude_none=True)
    except ValidationError as e:
        raise ValueError(e.errors())
    # get the data from the response
    data = api_response["data"]
    return data

def update_region(now, city, region, interval, ratio):
    # create a RegionParameters model and validate the inputs
    try:
        model = RegionParameters(now=now, interval=interval, city=city, region=region, ratio=ratio)
    except ValidationError as e:
        raise ValueError(e.errors())
    return general_update(model, "cases/region")

def update_city(now, city, interval):
    # create a CityParameters model and validate the inputs
    try:
        model = CityParameters(now=now, interval=interval, city=city)
    except ValidationError as e:
        raise ValueError(e.errors())
    return general_update(model, "cases/city")

def update_national(now, interval):
    # create a NationalParameters model and validate the inputs
    try:
        model = NationalParameters(now=now, interval=interval)
    except ValidationError as e:
        raise ValueError(e.errors())
    return general_update(model, "cases/national")