import unittest
import random

from vwo.helpers import singleton, impression_util
from ..data.settings_files import SETTINGS_FILES


class ImpressionTest(unittest.TestCase):
    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES[7]

    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_build_event_string_id(self):
        result = impression_util.build_event(self.settings_file,
                                             '123',
                                             '456',
                                             self.user_id,
                                             )
        self.assertIsNone(result)
