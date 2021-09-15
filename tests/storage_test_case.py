import time
from unittest.case import TestCase

from storage import StorageBackend


class StorageTestCase(TestCase):
    def __init__(self, methodName="runTest"):
        if self.__class__ is StorageTestCase:
            # don't run these tests on the abstract base implementation
            methodName = "runNoTestsInBaseClass"
        super().__init__(methodName)

    def runNoTestsInBaseClass(self):
        print("Not running tests in abstract base class")
        pass

    def setUp(self):
        self.storage: StorageBackend

    def test_set_get(self):
        self.storage.set("test", b"one")
        val = self.storage.get("test")
        self.assertEqual(val, b"one")

    def test_expiration(self):
        self.storage.set("test2", b"two", expiration=1)
        val = self.storage.get("test2")
        self.assertEqual(val, b"two")
        time.sleep(2)
        val2 = self.storage.get("test2")
        self.assertIsNone(val2)

    def test_delete(self):
        self.storage.set("test3", b"three")
        no_deleted = self.storage.delete("test3")
        val = self.storage.get("test3")
        self.assertEqual(no_deleted, 1)
        self.assertEqual(val, None)

    def test_delete_expired(self):
        self.storage.set("test4", b"four", expiration=1)
        time.sleep(2)
        no_deleted = self.storage.delete("test4")
        self.assertEqual(no_deleted, 0)
