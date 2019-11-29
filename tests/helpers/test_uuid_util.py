# Copyright 2019 Wingify Software Pvt. Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import random

import uuid
from vwo.services import singleton
from vwo.helpers import uuid_util
from ..data.settings_files import SETTINGS_FILES
from ..data.constants import TEST_USER_ID


VWO_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, 'https://vwo.com')


class UuidUtilTest(unittest.TestCase):
    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES["DUMMY_SETTINGS_FILE"]

    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_generate_empty_namespace(self):
        result = uuid_util.generate('', TEST_USER_ID)
        self.assertIsNone(result)

    def test_generate_empty_name(self):
        result = uuid_util.generate(VWO_NAMESPACE, '')
        self.assertIsNone(result)

    def test_generate_valid_params(self):
        result = uuid_util.generate(VWO_NAMESPACE, TEST_USER_ID)
        self.assertIsNotNone(result)
