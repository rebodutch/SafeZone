import json
import datetime

from callbacks.api_caller import load_taiwan_geo
from callbacks.api_caller import update_national, update_city, update_region
from collections import defaultdict

def update_cases():
    # get now date in format 'YYYY-MM-DD'
    now_date = datetime.date.today().strftime("%Y-%m-%d")
    # update national cases
    return update_national(now_date, "1")

def update_map(interval):
    # load taiwan geo data
    taiwan_geo_data = load_taiwan_geo()
    
    now_date = datetime.date.today().strftime("%Y-%m-%d")

    # get each city data for the last 3 months date by interval 15 days
    data = defaultdict(dict)

    for city, region in taiwan_geo_data.items():
        data[city][region] = update_region(now_date, city, region, interval)
    
    return data

def update_trends():
    # load taiwan geo data
    taiwan_geo_data = load_taiwan_geo()
    # update city cases
    dates = []
    now_date = datetime.date.today()

    # set dates are the last 3 months date by step 15 days
    for delta in [0, 15, 30, 45, 60, 75, 90]:
        date = now_date - datetime.timedelta(days=delta)
        dates.append(date.strftime("%Y-%m-%d")) 

    # get each city data for the last 3 months date by interval 15 days
    data = defaultdict(dict)
    for date in dates:
        for city in taiwan_geo_data.keys():
            data[date][city] = update_city(date, city, "14")
    
    return data