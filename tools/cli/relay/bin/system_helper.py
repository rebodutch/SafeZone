# tools/cli/relay/bin/system_helper.py
import redis
import requests
import psycopg2

from config.settings import REDIS_HOST, DB_URL, REPLICA_URL
from config.settings import SIMULATOR_URL, INGESTOR_URL, ANALYTICS_API_URL, DASHBOARD_URL

def get_phase():
    """
    Get the current phase of the system.
    """
    if _check_infra() and _check_core() and _check_init() and _check_ui():
        return "ui"
    elif _check_infra() and _check_core() and _check_init():
        return "init"
    elif _check_infra() and _check_core():
        return "core"
    elif _check_infra():
        return "infra"
    else:
        return "unknown"


def _check_infra():
    # check db
    try:
        conn = psycopg2.connect(DB_URL, connect_timeout=3)
        conn.close()

        conn = psycopg2.connect(REPLICA_URL, connect_timeout=3)
        conn.close()
    except psycopg2.OperationalError:
        return False
    
    # check redis
    try:
        r = redis.StrictRedis(host=REDIS_HOST, port=6379, decode_responses=True)
        if not r.ping():
            return False
    except redis.ConnectionError:
        return False

    # check cli-relay <- self checking ?
    # try:
    #     resp = requests.get(RELAY_URL + "/health")
    #     if resp.status_code != 200:
    #         return False
    # except requests.exceptions.RequestException:
    #     return False
    return True


def _check_core():
    check_points = [SIMULATOR_URL, INGESTOR_URL, ANALYTICS_API_URL]
    for entry in check_points:
        try:
            resp = requests.get(entry + "/health")
            if resp.status_code != 200:
                return False
        except requests.exceptions.RequestException as e:
            return False
    return True

def _check_init():
    try:
        r = redis.StrictRedis(host=REDIS_HOST, port=6379, decode_responses=True)
        if not r.get("safezone:phase:initJob") == "completed":
            return False
    except redis.ConnectionError:
        return False
    return True

def _check_ui():
    try:
        resp = requests.get(DASHBOARD_URL + "/health")
        if resp.status_code != 200:
            return False
    except requests.exceptions.RequestException:
        return False
    return True