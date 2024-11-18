import pandas as pd 

def read_csv():
    data = pd.read_csv('../data/covid19_daily.csv')
    # Keep only useful information in the data
    selected_columns = ["個案研判日", "縣市", "鄉鎮", "確定病例數"]
    data = data[selected_columns]
    # format the date in the data 
    data["個案研判日"] = pd.to_datetime(data["個案研判日"], format="%Y/%m/%d")
    # Reformat the date to "%Y-%m-%d"
    data["個案研判日"] = data["個案研判日"].dt.strftime("%Y-%m-%d")
    
    return data
