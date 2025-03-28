import os

import requests
from dotenv import load_dotenv

from schemas.request import SimulateModel, VerifyModel
from schemas.response import APIResponse
from commander.auth import load_token


class BaseRelayClient:
    def __init__(self, base_url: str = None):
        load_dotenv()
        self.url = base_url or os.getenv("RELAY_URL")
        self._update_paths()

    def _update_paths(self):
        self.dataflow_url = f"{self.url}/dataflow"
        self.db_url = f"{self.url}/db"

    def _get_auth_header(self):
        return {
            "Authorization": f"Bearer {load_token()}",
            "Content-Type": "application/json",
        }

    def set_root_url(self, url: str):
        if url:
            self.url = url
            self._update_paths()

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
    def __init__(self, base_url: str = None):
        super().__init__(base_url)

    def simulate(self, **kwargs):
        payload = SimulateModel(**kwargs).model_dump()
        return self.post("dataflow/simulate", payload)

    def verify(self, **kwargs):
        payload = VerifyModel(**kwargs).model_dump()
        return self.get("dataflow/verify", payload)


class DBClient(BaseRelayClient):
    def __init__(self, base_url: str = None):
        super().__init__(base_url)

    def init(self):
        return self.post("db/init", {})

    def clear(self):
        return self.post("db/clear", {})

    def reset(self):
        return self.post("db/reset", {})
