# Copyright 2019-2022 Wingify Software Pvt. Ltd.
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
from ..data.settings_files import SETTINGS_FILES
import json
import vwo

from vwo.storage.user import UserStorage


class UPSTest(unittest.TestCase):
    def test_class_initialization(self):
        class UPS(UserStorage):
            pass

        self.assertIsNotNone(UPS())

    def test_check_get_is_present(self):
        ups = UserStorage()
        self.assertIsNone(ups.get(123, "None"))

    def test_check_set_is_present(self):
        ups = UserStorage()
        self.assertIsNone(ups.set(123))

    """ def test_redis(self):
        settings_file = SETTINGS_FILES["SETTINGS_WITH_ISNB_WITHOUT_ISOB"]
        campaign_key = "BUCKET_ALGO_WITH_SEED_WITH_isNB_WITHOUT_isOB"
        redis_creds = {"url": "127.0.0.1", "user_id": None, "password": None}
        vwo_instance = vwo.launch(json.dumps(settings_file), redis_creds=redis_creds)

        vwo_instance.activate(campaign_key, "RD")
    """
