# /tools/relay/bin/service_caller.py
"""
This module is used to call the services in cluster by api.
"""
import requests
from config.settings import SIMULATOR_URL, ANALYTICS_API_URL

def simulate(date: str, end_date: str = None):
    """
    simulate the covid data for specific date by calling the simulate api.
    """
    try:
        if end_date is None:
            params = f"?date={date}"
            requests.get(SIMULATOR_URL + "/simulate/daily" + params)
            return f"Simulated covid data for {date}"
        else:
            params = f"?start_date={date}&end_date={end_date}"
            requests.get(SIMULATOR_URL + "/simulate/interval" + params)
            return f"Simulated covid data from {date} to {end_date}"
    except Exception as e:
        return f"Failed to simulate covid data: {e}"


def verify(date: str, interval: int, city: str, region: str, ratio: bool = False):
    """
    verify the covid data in the database by api.
    """
    try:
        # call the api to get the data by the given parameters
        params = f"?now={date}&interval={interval}"
        if city and region:
            params += f"&city={city}&region={region}&ratio={ratio}"
            response = requests.get(ANALYTICS_API_URL + "/cases/region" + params)
        elif city:
            params += f"&city={city}&ratio={ratio}"
            response = requests.get(ANALYTICS_API_URL + "/cases/city" + params)
        else:
            response = requests.get(ANALYTICS_API_URL + "/cases/national" + params)

        return response.json()
    except Exception as e:
        return f"Failed to verify covid data: {e}"
