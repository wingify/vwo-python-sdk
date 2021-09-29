# Copyright 2019-2021 Wingify Software Pvt. Ltd.
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
from vwo.constants import constants
from vwo.services.usage_stats_manager import UsageStats

from ..data.settings_files import SETTINGS_FILES
from ..config.config import TEST_LOG_LEVEL

TEST_LOG_LEVEL = TEST_LOG_LEVEL


class CustomLogger:
    def log(self, level, message):
        pass


class Integrations:
    def __init__(self):
        pass

    def callback(self, properties):
        pass


class ClientUserStorage:
    def __init__(self):
        self.storage = {}

    def get(self, user_id, campaign_key):
        return self.storage.get((user_id, campaign_key))

    def set(self, user_data):
        self.storage[(user_data.get("userId"), user_data.get("campaignKey"))] = user_data


class UsageStatsManagerTest(unittest.TestCase):
    def test_usage_stats_manager_CustomLogger(self):
        vwo.launch(json.dumps(SETTINGS_FILES.get("T_100_W_50_50_WS")), logger=CustomLogger())
        collected_stats = UsageStats.get_usage_stats()
        expected_stats = {"cl": 1, "_l": 1}
        self.assertDictEqual(collected_stats, expected_stats)

    def test_usage_stats_manager_CustomLogger_Integrations(self):
        vwo.launch(
            json.dumps(SETTINGS_FILES.get("T_100_W_50_50_WS")), logger=CustomLogger(), integrations=Integrations()
        )
        collected_stats = UsageStats.get_usage_stats()
        expected_stats = {"cl": 1, "ig": 1, "_l": 1}
        self.assertDictEqual(collected_stats, expected_stats)

    def test_usage_stats_manager_CustomLogger_Integrations_UserStorage(self):
        vwo.launch(
            json.dumps(SETTINGS_FILES.get("T_100_W_50_50_WS")),
            logger=CustomLogger(),
            integrations=Integrations(),
            user_storage=ClientUserStorage(),
        )
        collected_stats = UsageStats.get_usage_stats()
        expected_stats = {"cl": 1, "ig": 1, "ss": 1, "_l": 1}
        self.assertDictEqual(collected_stats, expected_stats)

    def test_usage_stats_manager_CustomLogger_Integrations_UserStorage_EventBatching(self):
        vwo.launch(
            json.dumps(SETTINGS_FILES.get("T_100_W_50_50_WS")),
            logger=CustomLogger(),
            integrations=Integrations(),
            user_storage=ClientUserStorage(),
            batch_events={"events_per_request": 5, "request_time_interval": 60},
        )
        collected_stats = UsageStats.get_usage_stats()
        expected_stats = {"cl": 1, "ig": 1, "ss": 1, "eb": 1, "_l": 1}
        self.assertDictEqual(collected_stats, expected_stats)

    def test_usage_stats_manager_CustomLogger_Integrations_UserStorage_EventBatching_GoalTypeToTrack(self,):
        vwo.launch(
            json.dumps(SETTINGS_FILES.get("T_100_W_50_50_WS")),
            logger=CustomLogger(),
            integrations=Integrations(),
            user_storage=ClientUserStorage(),
            batch_events={"events_per_request": 5, "request_time_interval": 60},
            goal_type_to_track=constants.GOAL_TYPES.ALL,
        )
        collected_stats = UsageStats.get_usage_stats()
        expected_stats = {"cl": 1, "ig": 1, "ss": 1, "eb": 1, "gt": 1, "_l": 1}
        self.assertDictEqual(collected_stats, expected_stats)

    def test_usage_stats_manager_Logger_Integrations_UserStorage_EventBatching_GoalTypeToTrack_LogLevel(self,):
        vwo.launch(
            json.dumps(SETTINGS_FILES.get("T_100_W_50_50_WS")),
            logger=CustomLogger(),
            integrations=Integrations(),
            user_storage=ClientUserStorage(),
            batch_events={"events_per_request": 5, "request_time_interval": 60},
            goal_type_to_track=constants.GOAL_TYPES.ALL,
            log_level=constants.LOG_LEVELS.DEBUG,
        )
        collected_stats = UsageStats.get_usage_stats()
        expected_stats = {"cl": 1, "ig": 1, "ss": 1, "eb": 1, "gt": 1, "ll": 1, "_l": 1}
        self.assertDictEqual(collected_stats, expected_stats)
