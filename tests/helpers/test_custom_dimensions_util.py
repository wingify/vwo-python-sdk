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
import mock
import json

from vwo.helpers import custom_dimensions_util, uuid_util, generic_util
from vwo.constants import constants
from ..data.settings_files import SETTINGS_FILES
from ..data.constants import TEST_ACCOUNT_ID


class CustomDimensionUtilTest(unittest.TestCase):
    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES["DUMMY_SETTINGS_FILE"]

    def test_get_url_param_(self):

        with mock.patch(
            "vwo.helpers.generic_util.get_random_number",
            return_value="123456789",
        ), mock.patch(
            "vwo.helpers.generic_util.get_current_unix_timestamp",
            return_value="123456789",
        ):
            result = custom_dimensions_util.get_url_params(
                self.settings_file, "browser", "chrome", self.user_id,
            )
            tags = {"u": {"browser": "chrome"}}
            params = {
                "url": "https://dev.visualwebsiteoptimizer.com/server-side/push",
                "account_id": TEST_ACCOUNT_ID,
                "u": uuid_util.generate_for(self.user_id, TEST_ACCOUNT_ID),
                "sId": generic_util.get_current_unix_timestamp(),
                "tags": json.dumps(tags),
                "random": generic_util.get_random_number(),
                "sdk": constants.SDK_NAME,
                "sdk-v": constants.SDK_VERSION,
                "ap": constants.PLATFORM,
                "uId": self.user_id,
            }
            self.assertDictEqual(params, result)
