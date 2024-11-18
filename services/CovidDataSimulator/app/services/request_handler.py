from services import csv_reader, data_filter, data_sender

def handle_daily_request(date):
    # read history data
    data = csv_reader.read_csv()
    # filter by specific date 
    filtered_data = data_filter.filter_by_date(data, date)
    # sent the data to CovidDataCollector
    data_sender.send_data(filtered_data)
    return {"status": "success", "message": "Data sent successfully for date " + date}

def handle_interval_request(start_date, end_date):
    # read history data
    data = csv_reader.read_csv()
    # filter by specific date range
    filtered_data = data_filter.filter_by_interval(data, start_date, end_date)
    # sent the batch data to CovidDataCollector
    data_sender.send_data_batch(filtered_data)

    return {"status": "success", "message": "Data sent successfully for interval " + start_date + " to " + end_date}