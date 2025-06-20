# tools/cli/relay/bin/system_helper.py
import requests # type: ignore
import redis # type: ignore
import psycopg2 # type: ignore

from config.settings import REDIS_HOST, DB_URL, REPLICA_URL
from config.settings import SIMULATOR_URL, INGESTOR_URL, ANALYTICS_API_URL, DASHBOARD_URL, MKDOC_URL


def get_health(target: str=None, all: bool=False):
    result = ""
    if all or target == "cli-relay":
        result += "cli-relay: success\n" 
    if all or target == "db":
        result += "db: success\n" if _check_db() else "db: fail\n"
    if all or target == "redis":
        result += "redis: success\n" if _check_redis() else "redis: fail\n"
    if all or target == "data-simulator":
        result += "data simulator: success\n" if _check_core(service="data-simulator") else "data simulator: fail\n"
    if all or target == "data-ingestor":
        result += "data ingestor: success\n" if _check_core(service="data-ingestor") else "data ingestor: fail\n"
    if all or target == "analytics-api":
        result += "analytics api: success\n" if _check_core(service="analytics-api") else "analytics api: fail\n"
    if all or target == "dashboard":
        result += "dashboard: success\n" if _check_ui(service="dashboard") else "dashboard: fail\n"
    if all or target == "mkdoc":
        result += "mkdoc: success\n" if _check_ui(service="mkdoc") else "mkdoc: fail\n"
    return result

def _check_db():
    try:
        conn = psycopg2.connect(DB_URL, connect_timeout=3)
        conn.close()

        conn = psycopg2.connect(REPLICA_URL, connect_timeout=3)
        conn.close()
    except psycopg2.OperationalError:
        return False
    return True
    
def _check_redis():
    try:
        r = redis.StrictRedis(host=REDIS_HOST, port=6379, decode_responses=True)
        if not r.ping():
            return False
    except redis.ConnectionError:
        return False
    return True


def _check_core(service):
    if service == "data-simulator":
        check_point = SIMULATOR_URL
    elif service == "data-ingestor":
        check_point = INGESTOR_URL
    elif service == "analytics-api":
        check_point = ANALYTICS_API_URL
    else:
        return False

    try:
        resp = requests.get(check_point + "/health")
        if resp.status_code != 200:
            return False
    except requests.exceptions.RequestException as e:
        return False
    return True

def _check_ui(service):
    if service == "dashboard":
        check_point = DASHBOARD_URL
    elif service == "mkdoc":
        check_point = MKDOC_URL
    else:
        return False
    try:
        resp = requests.get(check_point + "/health")
        if resp.status_code != 200:
            return False
    except requests.exceptions.RequestException:
        return False
    return True