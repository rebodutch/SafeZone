# /bin/client.py
import os
import sys
import json

import requests
from dotenv import load_dotenv

from schemas.request import SimulateModel, VerifyModel, SetTimeModel, HealthModel
from schemas.response import APIResponse

class BaseRelayClient:
    def __init__(self, config: Optional[dict] = None):
        self.config = config or self._load_config()
        self.url = self.config["relay_url"]
        self.token = self.config["id_token"]
        self.user_email = self.config["email"]

    def _load_config(self):
        load_dotenv()
        config_file = os.getenv("CONFIG_FILE")
        if not (config_file and os.path.exists(config_file)):
            print("Login required. Please run login command.")
            sys.exit(1)
        with open(config_file) as f:
            return json.load(f)

    def _get_auth_header(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def request(
        self,
        method: str,
        path: str,
        payload: Optional[dict] = None,
        response_model: Optional[Type[Any]] = None,
        params: Optional[dict] = None,
    ):
        try:
            resp = requests.request(
                method=method,
                url=f"{self.url}/{path}",
                headers=self._get_auth_header(),
                json=payload if method != "GET" else None,
                params=params if method == "GET" else None,
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return response_model(**data).model_dump() if response_model else data
        except Exception as e:
            print(f"[Request fail] {method} {path}: {e}")
            raise


class DataflowClient(BaseRelayClient):
    def simulate(self, **kwargs):
        payload = SimulateModel(**kwargs).model_dump(mode="json")
        return self.request(
            "POST", "dataflow/simulate", payload=payload, response_model=APIResponse
        )

    def verify(self, **kwargs):
        payload = VerifyModel(**kwargs).model_dump(mode="json")
        return self.request(
            "GET", "dataflow/verify", params=payload, response_model=APIResponse
        )

class TimeClient(BaseRelayClient):
    def now(self):
        return self.request("GET", "system/time/now", response_model=APIResponse)

    def set(self, **kwargs):
        payload = SetTimeModel(**kwargs).model_dump(mode="json")
        return self.request(
            "POST", "system/time/set", payload=payload, response_model=APIResponse
        )

    def get_status(self):
        return self.request("GET", "system/time/status", response_model=APIResponse)

class HealthClient(BaseRelayClient):
    def check(self, **kwargs):
        payload = HealthModel(**kwargs).model_dump(mode="json")
        return self.request(
            "GET", "system/health", params=payload, response_model=APIResponse
        )

class DBClient(BaseRelayClient):
    def init(self):
        return self.request("POST", "db/init", response_model=APIResponse)

    def clear(self):
        return self.request("POST", "db/clear", response_model=APIResponse)

