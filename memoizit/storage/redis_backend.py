import os
from typing import Any, List, Optional
import redis

from .backend import StorageBackend


class RedisBackend(StorageBackend):
    def __init__(self, **kwargs):

        env_host = os.getenv("REDIS_HOST", "localhost")
        env_port = os.getenv("REDIS_PORT", "6379")
        env_username = os.getenv("REDIS_USERNAME")
        env_password = os.getenv("REDIS_PASSWORD")

        kwargs.setdefault("host", env_host)
        kwargs.setdefault("port", env_port)
        kwargs.setdefault("username", env_username)
        kwargs.setdefault("password", env_password)

        self.r = redis.Redis(**kwargs)
        self.r.ping()

    def get(self, key: str) -> Any:
        return self.r.get(key)

    def set(self, key: str, value: Any, expiration: Optional[int] = None) -> bool:
        return bool(self.r.set(key, value, ex=expiration))

    def delete(self, key: str) -> int:
        return int(self.r.delete(key))

    def keys_startswith(self, key_start: str) -> List[str]:
        return list(self.r.keys(key_start + "*"))
