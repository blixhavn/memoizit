from unittest import mock
from unittest.case import TestCase

from memoize import Memoizer


class TestMemoizer(TestCase):
    def setUp(self):
        self.mm = Memoizer()
        self.mm.storage.get = mock.MagicMock(side_effect=self.mm.storage.get)
        self.mm.storage.set = mock.MagicMock(side_effect=self.mm.storage.set)

    def test_memoize(self):
        self.reset_mocks()

        @self.mm.memoize()
        def test_function1():
            return "testing"

        val = test_function1()
        self.assertEqual(val, "testing")

        test_function1()
        self.mm.storage.set.assert_called_once()

    def test_memoize_invalidate(self):
        self.reset_mocks()

        @self.mm.memoize()
        def test_function2(some: str = "", arguments: str = ""):
            return f"test {some}{arguments}"

        val = test_function2(some="one arg")
        self.assertEqual(val, "test one arg")

        self.mm.invalidate_memoize("test_function2")
        self.assertEqual(len(self.mm.storage.keys_startswith("test_function2")), 0)

        test_function2(some="one arg")
        test_function2(some="one arg", arguments="two")
        self.assertEqual(
            len(self.mm.storage.keys_startswith("memoize_test_function2")), 2
        )

        # Will not invalidate anything
        self.mm.invalidate_memoize("test_function2", arguments="two")
        self.assertEqual(
            len(self.mm.storage.keys_startswith("memoize_test_function2")), 2
        )

        self.mm.invalidate_memoize("test_function2", some="one arg")
        self.assertEqual(
            len(self.mm.storage.keys_startswith("memoize_test_function2")), 0
        )

    def reset_mocks(self):
        self.mm.storage.get.reset_mock()
        self.mm.storage.set.reset_mock()
