# tools/cli/relay/bin/time_helper.py
import requests  # type: ignore

from config.settings import TIME_SERVER_URL
from utils.pydantic_model.request import SetTimeModel


def get_system_date():
    response = requests.get(url=f"{TIME_SERVER_URL}/now")
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()


def set_mock_config(mock: bool = None, mock_date: str = None, acceleration: int = None):
    payload = SetTimeModel(mock=mock, mock_date=mock_date, acceleration=acceleration)
    response = requests.post(
        url=f"{TIME_SERVER_URL}/set", json=payload.model_dump(exclude_none=True)
    )
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()


def get_mock_config():
    response = requests.get(url=f"{TIME_SERVER_URL}/status")
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()
