from redis.exceptions import ConnectionError
import unittest

from memoizit.storage.redis_backend import RedisBackend
from tests.storage_test_case import StorageTestCase


class TestRedisStorage(StorageTestCase):
    def setUp(self):
        self.storage = RedisBackend()
        try:
            self.storage.r.ping()
        except ConnectionError:
            raise unittest.SkipTest("Redis not available")
