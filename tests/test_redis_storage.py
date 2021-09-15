from storage import RedisBackend
import unittest
from redis.exceptions import ConnectionError

from tests.storage_test_case import StorageTestCase


class TestRedisStorage(StorageTestCase):
    def setUp(self):
        self.storage = RedisBackend()
        try:
            self.storage.r.ping()
        except ConnectionError:
            raise unittest.SkipTest("Redis not available")
