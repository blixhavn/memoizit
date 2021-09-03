import os
from typing import Any, List
import redis

from storage.backend import StorageBackend

class RedisBackend(StorageBackend):

    def __init__(self, **kwargs):

        env_host = os.getenv("REDIS_HOST")
        env_port = os.getenv("REDIS_PORT")
        env_username = os.getenv("REDIS_USERNAME")
        env_password = os.getenv("REDIS_PASSWORD")
                
        kwargs.setdefault("host", env_host)
        kwargs.setdefault("port", env_port)
        kwargs.setdefault("username", env_username)
        kwargs.setdefault("password", env_password)

        self.r = redis.Redis(**kwargs)

    def get(self, key: str) -> Any:
        return self.r.get(key)

    def set(self, key: str, value: Any) -> bool:
        return self.r.set(key, value)

    def keys(self, key_pattern: str) -> List[str]:
        key_pattern += "*"
        return self.r.keys(key_pattern)