import time
from typing import Any, List, Optional

from .backend import StorageBackend


class PythonBackend(StorageBackend):
    def __init__(self, **kwargs):
        self.storage = dict()

    def get(self, key: str) -> Any:
        now = int(time.time())
        try:
            val = self.storage[key]
            if val[1] != 0 and val[1] < now:
                del self.storage[key]
                return None
            else:
                return val[0]
        except KeyError:
            return None

    def set(self, key: str, value: bytes, expiration: Optional[int] = None) -> bool:
        ex = int(time.time()) + expiration if expiration else 0
        self.storage[key] = (value, ex)
        return True

    def delete(self, key: str) -> int:
        now = int(time.time())
        try:
            val = self.storage[key]
            del self.storage[key]

            if val[1] != 0 and val[1] < now:
                return 0
            else:
                return 1
        except IndexError:
            return 0

    def keys_startswith(self, key_start: str) -> List[str]:
        return list(
            filter(
                None,
                map(
                    lambda key: key if key.startswith(key_start) else None,  # type: ignore
                    self.storage.keys(),
                ),
            )
        )
