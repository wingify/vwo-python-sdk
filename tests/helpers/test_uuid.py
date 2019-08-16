import unittest
import random

import uuid
from vwo.helpers import singleton, uuid_util
from ..data.settings_files import SETTINGS_FILES

VWO_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, 'https://vwo.com')


class UuidTest(unittest.TestCase):
    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES[7]

    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_generate_empty_namespace(self):
        result = uuid_util.generate('', 'shravan')
        self.assertIsNone(result)

    def test_generate_empty_name(self):
        result = uuid_util.generate(VWO_NAMESPACE, '')
        self.assertIsNone(result)

    def test_generate_valid_params(self):
        result = uuid_util.generate(VWO_NAMESPACE, 'shravan')
        self.assertIsNotNone(result)
