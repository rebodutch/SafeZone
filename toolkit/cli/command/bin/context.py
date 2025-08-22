# bin/context.py
from typing import Any

from utils.context import trace_id_var

class GlobalContextManager:
    def __init__(self):
        self._state_dict: dict = {}

    def get(self, key: str, default: Any = None) -> Any:
        if key == "trace_id":
            return trace_id_var.get()
        return self._state_dict.get(key, default)

    def set(self, key: str, value: Any):
        if key == "trace_id":
            trace_id_var.set(value)
        else:
            self._state_dict[key] = value

# Singleton
global_context = GlobalContextManager()