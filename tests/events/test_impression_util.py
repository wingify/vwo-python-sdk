import unittest
import random

from vwo.services import singleton
from vwo.helpers import impression_util
from ..data.settings_files import SETTINGS_FILES


class ImpressionTest(unittest.TestCase):
    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES["DUMMY_SETTINGS_FILE"]

    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_create_impression_string_id(self):
        result = impression_util.create_impression(self.settings_file,
                                                   '123',
                                                   '456',
                                                   self.user_id,
                                                   )
        self.assertIsNone(result)
