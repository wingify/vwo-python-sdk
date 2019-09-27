import unittest

from vwo.storage.user import UserStorage


class UPSTest(unittest.TestCase):
    def test_class_initialization(self):
        class UPS(UserStorage):
            pass
        self.assertIsNotNone(UPS())

    def test_check_get_is_present(self):
        ups = UserStorage()
        self.assertIsNone(ups.get(123, 'None'))

    def test_check_set_is_present(self):
        ups = UserStorage()
        self.assertIsNone(ups.set(123))
