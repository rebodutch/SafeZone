from services import data_productor, data_sender, date_checker
from exception import EmptyDataError

def handle_daily_request(date):
    # check input date
    date_checker.check_date(date)

    print(date)

    # read history data and filter by specific date
    filtered_data = data_productor.get_data_by_date(date)
    
    print(filtered_data)
    if not filtered_data:
        raise EmptyDataError
    
    data_sender.send_data(filtered_data)
    print("sent success")


def handle_interval_request(start_date, end_date):
    # check input date
    date_checker.check_date(start_date)
    date_checker.check_date(end_date)
    date_checker.check_interval(start_date, end_date)

    # read history data and filter by specific date
    filtered_data = data_productor.get_data_by_interval(start_date, end_date)
    
    if not filtered_data:
        raise EmptyDataError
    
    data_sender.send_data(filtered_data)
