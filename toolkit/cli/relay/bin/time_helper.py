# tools/cli/relay/bin/time_healper.py
import requests
from config.settings import TIME_SERVER_URL

def get_current_time():
    """
    Get the current time from the WorldTimeAPI.
    """
    try:
        response = requests.get(url=f"{TIME_SERVER_URL}/now")
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data['current_date']
    except requests.RequestException as e:
        print(f"Error fetching time: {e}")
        return None
    
def set_time_config(mock: bool, acceleration: int, bias_days: int):
    """
    Set the time configuration on the server.
    """
    try:
        response = requests.post(
            url=f"{TIME_SERVER_URL}/set_time",
            json={
                "mock": mock,
                "acceleration": acceleration,
                "bias_days": bias_days
            }
        )
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data['success']
    except requests.RequestException as e:
        print(f"Error setting time config: {e}")
        return False

def get_time_config():
    """
    Get the current time configuration from the server.
    """
    try:
        response = requests.post(url=f"{TIME_SERVER_URL}/status")
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data['data']
    except requests.RequestException as e:
        print(f"Error fetching time config: {e}")
        return None