# Copyright 2019-2020 Wingify Software Pvt. Ltd.
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

from vwo.helpers import impression_util
from ..data.settings_files import SETTINGS_FILES


class ImpressionTest(unittest.TestCase):
    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES["DUMMY_SETTINGS_FILE"]

    def test_create_impression_string_id(self):
        result = impression_util.create_impression(self.settings_file, "123", "456", self.user_id,)
        self.assertIsNone(result)
