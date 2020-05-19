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

from __future__ import print_function
import unittest
import json

import vwo
from ..data.settings_files import SETTINGS_FILES


class LaunchTest(unittest.TestCase):
    def test_launch_invalid_settings_file_passed(self):
        vwo_instance = vwo.launch("INVALID_SETTINGS_FILE")
        self.assertIsNone(vwo_instance)

    def test_launch_valid_settings_file_passed(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")))
        print(type(vwo_instance))
        self.assertIsInstance(vwo_instance, vwo.vwo.VWO)

    def test_launch_invalid_logger_object_passed(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), logger="LOGGER")
        self.assertIsNone(vwo_instance)

    def test_launch_valid_logger_object_passed(self):
        class Logger:
            def log(self, log_level, log_message):
                print(log_level, log_message)

        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), logger=Logger())
        print(type(vwo_instance))
        self.assertIsInstance(vwo_instance, vwo.vwo.VWO)

    def test_launch_invalid_user_storage_object_passed(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), user_storage="USER_STORAGE")
        self.assertIsNone(vwo_instance)

    def test_launch_valid_user_storage_object_passed(self):
        class UserStorage:
            def get(self, *args):
                pass

            def set(self, *args):
                pass

        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), user_storage=UserStorage())
        self.assertIsInstance(vwo_instance, vwo.vwo.VWO)

    def test_launch_invalid_is_development_mode_passed(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), is_development_mode="abcd")
        self.assertIsNone(vwo_instance)

    def test_launch_valid_is_development_mode_passed(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), is_development_mode=True)
        self.assertIsInstance(vwo_instance, vwo.vwo.VWO)

    def test_launch_invalid_log_level_passed(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), log_level="INFO")
        self.assertIsNone(vwo_instance)

    def test_launch_valid_log_level_passed(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), log_level=vwo.LOG_LEVELS.INFO)
        self.assertIsInstance(vwo_instance, vwo.vwo.VWO)

    def test_launch_invalid_goal_type_to_track_passed(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), goal_type_to_track="abcd")
        self.assertIsNone(vwo_instance)

    def test_launch_valid_goal_type_to_track_passed(self):
        vwo_instance = vwo.launch(
            json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), goal_type_to_track=vwo.GOAL_TYPES.ALL
        )
        self.assertIsInstance(vwo_instance, vwo.vwo.VWO)

    def test_launch_invalid_should_track_returning_user_passed(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), should_track_returning_user="abcd")
        self.assertIsNone(vwo_instance)

    def test_launch_valid_should_track_returning_user_passed(self):
        vwo_instance = vwo.launch(json.dumps(SETTINGS_FILES.get("AB_T_50_W_50_50")), should_track_returning_user=True)
        self.assertIsInstance(vwo_instance, vwo.vwo.VWO)
