import logging

import requests
from datetime import date

from config.settings import TIME_SERVER_URL

logger = logging.getLogger(__name__)

def get_now():
    try:
        logger.debug("Fetching current date from time server.")
        # Fetch the current date from the time server
        reps = requests.get(TIME_SERVER_URL + "/now", timeout=10)
        # date change check
        reps.raise_for_status()  # Raise an error for bad responses
        system_date = reps.json().get("system_date")
        logger.debug(f"Successfully fetched system date {system_date} from time server.")
        return system_date
    except requests.RequestException as e:
        logger.error(f"Error fetching date from time server: {e}")
        logger.info("Falling back to local date.")
        # Fallback to local date if the request fails
        return date.today().strftime("%Y-%m-%d")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.info("Falling back to local date.")
        # Fallback to local date if any other error occurs
        return date.today().strftime("%Y-%m-%d")
