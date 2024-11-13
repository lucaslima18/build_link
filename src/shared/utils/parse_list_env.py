import os, json
from typing import List


def parse_list_env(var_name: str, default: List[str] = []) -> list:
    value = os.getenv(var_name, default)
    if value:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value.split(",") if isinstance(value, str) else []
    return []
