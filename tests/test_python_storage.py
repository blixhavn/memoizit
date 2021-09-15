from storage import PythonBackend
from tests.storage_test_case import StorageTestCase


class TestPythonStorage(StorageTestCase):
    def setUp(self):
        self.storage = PythonBackend()
