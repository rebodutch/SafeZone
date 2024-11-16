import pandas as pd

# 讀取疫情數據
data = pd.read_csv('../data/covid19_daily.csv')

# 檢查數據結構
print(data.head())