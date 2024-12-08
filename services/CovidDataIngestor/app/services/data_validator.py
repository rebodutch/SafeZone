# app/services/data_validator.py
from utils.models.case_validator import validate_data
from config.logger import get_logger

logger = get_logger()

def validate_datas(data):
    try:
        for case in data:
            print(f"validating case = {case}")
            validate_data(**case)
    except Exception as e:
        raise e
          