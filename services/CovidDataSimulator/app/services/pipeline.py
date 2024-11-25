from services.data_productor import get_data_by_date, get_data_by_interval
from services.data_sender import send_data
from services.date_checker import check_date, check_interval


def handle_daily_request(date):
    # check input date
    check_date(date)

    # read history data and filter by specific date
    filtered_data = get_data_by_date(date)

    send_data(filtered_data)


def handle_interval_request(start_date, end_date):
    # check input date
    check_date(start_date)
    check_date(end_date)
    check_interval(start_date, end_date)

    # read history data and filter by specific date
    filtered_data = get_data_by_interval(start_date, end_date)

    send_data(filtered_data)
