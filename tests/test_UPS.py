import unittest

from vwo.user_profile import UserProfileService


class UPSTest(unittest.TestCase):
    def test_class_initialization(self):
        class UPS(UserProfileService):
            pass
        self.assertIsNotNone(UPS())

    def test_check_lookup_is_present(self):
        ups = UserProfileService()
        self.assertIsNone(ups.lookup(123))

    def test_check_save_is_present(self):
        ups = UserProfileService()
        self.assertIsNone(ups.save(123))
