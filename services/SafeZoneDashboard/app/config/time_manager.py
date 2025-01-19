import os
from datetime import datetime

def get_now():
    freeze_time = os.getenv("FREEZE_TIME")
    if freeze_time:
        return datetime.strptime(freeze_time, "%Y-%m-%d")
    return datetime.now()
