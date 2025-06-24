# /tools/relay/bin/service_caller.py
import requests  # type: ignore

from config.settings import SIMULATOR_URL, ANALYTICS_API_URL


def simulate(date: str, end_date: str = None):
    if end_date is None:
        params = f"?date={date}"
        response = requests.get(SIMULATOR_URL + "/simulate/daily" + params)
    else:
        params = f"?start_date={date}&end_date={end_date}"
        response = requests.get(SIMULATOR_URL + "/simulate/interval" + params)
    response.raise_for_status()
    return response.json()


def verify(date: str, interval: int, city: str, region: str, ratio: bool = False):
    params = f"?now={date}&interval={interval}"
    if city and region:
        params += f"&city={city}&region={region}&ratio={ratio}"
        response = requests.get(ANALYTICS_API_URL + "/cases/region" + params)
    elif city:
        params += f"&city={city}&ratio={ratio}"
        response = requests.get(ANALYTICS_API_URL + "/cases/city" + params)
    else:
        response = requests.get(ANALYTICS_API_URL + "/cases/national" + params)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()
