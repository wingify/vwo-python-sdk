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
import json
from ..data.settings_files import SETTINGS_FILES
import vwo


class test_validate(unittest.TestCase):
    def setUp(self):
        self.log_level = vwo.LOG_LEVELS.DEBUG

    def test_validate_extra_param_in_campaign(self):
        self.settings_file = SETTINGS_FILES.get("VALIDATE_EXTRA_PARAM_IN_CAMPAIGN")
        self.vwo_instance = vwo.launch(json.dumps(self.settings_file))
        campaign_key = self.settings_file["campaigns"][0]["key"]

        # check if valid variation is returned
        variation = self.vwo_instance.get_variation_name(campaign_key, "Ashley")
        self.assertIsNotNone(variation)
        self.assertEqual(variation, "Variation-1")

    def test_validate_extra_param_in_root(self):
        self.settings_file = SETTINGS_FILES.get("VALIDATE_EXTRA_PARAM_IN_ROOT")
        self.vwo_instance = vwo.launch(json.dumps(self.settings_file))
        campaign_key = self.settings_file["campaigns"][0]["key"]

        # check if valid variation is returned
        variation = self.vwo_instance.get_variation_name(campaign_key, "Ashley")
        self.assertIsNotNone(variation)
        self.assertEqual(variation, "Variation-1")
