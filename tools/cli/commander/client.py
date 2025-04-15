import os
import sys
import json

import requests
from dotenv import load_dotenv

from schemas.request import SimulateModel, VerifyModel
from schemas.response import APIResponse


class BaseRelayClient:
    def __init__(self):
        self._load_config()

    def _load_config(self):
        load_dotenv()
        CONFIG_FILE = os.getenv("CONFIG_FILE")

        if not os.path.exists(CONFIG_FILE):
            print("Login required. Please run login command.")
            sys.exit(1)

        with open(CONFIG_FILE, "r") as f:
            configs = json.load(f)
        self.url = configs["relay_url"]
        self.token = configs["id_token"]
        self.user_email = configs["email"]
        self._update_paths()

    def _update_paths(self):
        self.dataflow_url = f"{self.url}/dataflow"
        self.db_url = f"{self.url}/db"

    def _get_auth_header(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def post(self, path: str, payload: dict):
        response = requests.post(
            f"{self.url}/{path}",
            headers=self._get_auth_header(),
            json=payload,
            timeout=10,
        )
        return APIResponse(**response.json()).model_dump()

    def get(self, path: str, payload: dict):
        response = requests.get(
            f"{self.url}/{path}",
            headers=self._get_auth_header(),
            params=payload,
            timeout=10,
        )
        return APIResponse(**response.json()).model_dump()


class DataflowClient(BaseRelayClient):
    def __init__(self):
        super().__init__()

    def simulate(self, **kwargs):
        payload = SimulateModel(**kwargs).model_dump(mode="json")
        return self.post("dataflow/simulate", payload)

    def verify(self, **kwargs):
        payload = VerifyModel(**kwargs).model_dump(mode="json")
        return self.get("dataflow/verify", payload)


class SystemClient(BaseRelayClient):
    def __init__(self):
        super().__init__()

    def get_phase(self):
        return self.get("system/get_phase")
    

class DBClient(BaseRelayClient):
    def __init__(self):
        super().__init__()

    def init(self):
        return self.post("db/init", {})

    def clear(self):
        return self.post("db/clear", {})

    def reset(self):
        return self.post("db/reset", {})
