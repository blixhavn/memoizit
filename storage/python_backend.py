import os
from typing import Any, List
import re
import redis

from storage.backend import StorageBackend

class PythonBackend(StorageBackend):

    def __init__(self, **kwargs):
        self.storage = dict()

    def get(self, key: str) -> Any:
        return self.storage.get(key)

    def set(self, key: str, value: Any) -> bool:
        self.storage[key] = value
        return True

    def keys(self, key_pattern: str) -> List[str]:
        return list(filter(
            None,
            map(
                lambda key: key if re.match(key_pattern, key) else None,
                self.storage.keys()
            )
        ))