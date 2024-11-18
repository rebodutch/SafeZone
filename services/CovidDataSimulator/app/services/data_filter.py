import pandas as pd 

def filter_by_date(data, date):
    # Filter data for a specific date
    return data[data["個案研判日"] == date]

def filter_by_interval(data, start_date, end_date):
    # Filter data for a specific date range
    return data[(data["個案研判日"] >= start_date) & (data["個案研判日"] <= end_date)]
