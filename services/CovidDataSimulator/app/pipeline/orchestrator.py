from pipeline.data_productor import get_data_by_date, get_data_by_interval
from pipeline.data_sender import send_data


def handle_daily_request(date):
    # read history data and filter by specific date
    filtered_data = get_data_by_date(date)

    send_data(filtered_data)


def handle_interval_request(start_date, end_date):

    # read history data and filter by specific date
    filtered_data = get_data_by_interval(start_date, end_date)

    send_data(filtered_data)
