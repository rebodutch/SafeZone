import pandas as pd
from services import data_filter

# 模擬數據
data = pd.DataFrame({
    "個案研判日": ["2023-03-20", "2023-03-21"],
    "確定病例數": [10, 15]
})

def test_filter_by_date():
    filtered_data = data_filter.filter_by_date(data, "2023-03-20")
    assert len(filtered_data) == 1
    assert filtered_data.iloc[0]["確定病例數"] == 10

def test_filter_by_interval():
    filtered_data = data_filter.filter_by_interval(data, "2023-03-20", "2023-03-21")
    assert len(filtered_data) == 2
