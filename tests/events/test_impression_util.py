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
import random
import mock

from vwo.helpers import generic_util, impression_util, uuid_util
from vwo.constants import constants
from ..data.settings_files import SETTINGS_FILES
from ..data.constants import TEST_ACCOUNT_ID, TEST_USER_ID


class ImpressionTest(unittest.TestCase):
    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES["DUMMY_SETTINGS_FILE"]
        self.events_name = [
            constants.EVENTS.VWO_SYNC_VISITOR_PROP,
            constants.EVENTS.VWO_VARIATION_SHOWN,
            "test_goal_identifier",
        ]
        self.visitor_ua = "user_agent"
        self.visitor_ip = "user_ip"

    def test_create_impression_string_id(self):
        result = impression_util.create_impression(self.settings_file, "123", "456", self.user_id)
        self.assertIsNone(result)

    def test_get_event_query_params(self):

        with mock.patch("vwo.helpers.generic_util.get_random_number", return_value="0.123456789"), mock.patch(
            "vwo.helpers.generic_util.get_current_unix_timestamp_milli", return_value="123456789"
        ), mock.patch("vwo.services.usage_stats_manager.UsageStats.get_usage_stats", return_value={"_l": 1, "ll": 1}):
            for event_name in self.events_name:
                expected = {
                    "en": event_name,
                    "a": TEST_ACCOUNT_ID,
                    "env": self.settings_file.get("sdkKey"),
                    "eTime": generic_util.get_current_unix_timestamp_milli(),
                    "random": generic_util.get_random_number(),
                    "p": "FS",
                    constants.VISITOR.USER_AGENT: "",
                    constants.VISITOR.IP: "",
                }

                if event_name == constants.EVENTS.VWO_VARIATION_SHOWN:
                    expected.update({"_l": 1, "ll": 1})

                result = impression_util.get_events_params(self.settings_file, event_name, None, None)
                self.assertDictEqual(result, expected)

    def test_get_events_common_properties(self):

        with mock.patch("vwo.helpers.generic_util.get_random_number", return_value="0.123456789"), mock.patch(
            "vwo.helpers.generic_util.get_current_unix_timestamp", return_value="123456789"
        ), mock.patch("vwo.helpers.generic_util.get_current_unix_timestamp_milli", return_value="123456789000"):
            for event_name in self.events_name:
                expected = {
                    "d": {
                        "msgId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID)
                        + "-"
                        + str(generic_util.get_current_unix_timestamp_milli()),
                        "visId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID),
                        "sessionId": generic_util.get_current_unix_timestamp(),
                        "event": {
                            "props": {
                                "vwo_sdkName": constants.SDK_NAME,
                                "vwo_sdkVersion": constants.SDK_VERSION,
                                "vwo_envKey": self.settings_file.get("sdkKey")
                            },
                            "name": event_name,
                            "time": generic_util.get_current_unix_timestamp_milli(),
                        },
                        "visitor": {"props": {"vwo_fs_environment": self.settings_file.get("sdkKey")}},
                    }
                }

                result = impression_util.get_events_common_properties(self.settings_file, TEST_USER_ID, event_name)
                self.assertDictEqual(result, expected)

    def test_create_track_user_events_impression(self):
        with mock.patch("vwo.helpers.generic_util.get_random_number", return_value="0.123456789"), mock.patch(
            "vwo.helpers.generic_util.get_current_unix_timestamp", return_value="123456789"
        ), mock.patch("vwo.helpers.generic_util.get_current_unix_timestamp_milli", return_value="123456789000"):

            expected = {
                "d": {
                    "msgId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID)
                    + "-"
                    + str(generic_util.get_current_unix_timestamp_milli()),
                    "visId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID),
                    "sessionId": generic_util.get_current_unix_timestamp(),
                    "event": {
                        "props": {
                            "id": 1,
                            "variation": 1,
                            "isFirst": 1,
                            "vwo_sdkName": constants.SDK_NAME,
                            "vwo_sdkVersion": constants.SDK_VERSION,
                            "vwo_envKey": self.settings_file.get("sdkKey")
                        },
                        "name": constants.EVENTS.VWO_VARIATION_SHOWN,
                        "time": generic_util.get_current_unix_timestamp_milli(),
                    },
                    "visitor": {"props": {"vwo_fs_environment": self.settings_file.get("sdkKey")}},
                }
            }

            result = impression_util.create_track_user_events_impression(self.settings_file, 1, 1, TEST_USER_ID)

            self.assertDictEqual(result, expected)

    def test_create_track_goal_events_impression_without_revenue(self):

        with mock.patch("vwo.helpers.generic_util.get_random_number", return_value="0.123456789"), mock.patch(
            "vwo.helpers.generic_util.get_current_unix_timestamp", return_value="123456789"
        ), mock.patch("vwo.helpers.generic_util.get_current_unix_timestamp_milli", return_value="123456789000"):

            expected = {
                "d": {
                    "msgId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID)
                    + "-"
                    + str(generic_util.get_current_unix_timestamp_milli()),
                    "visId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID),
                    "sessionId": generic_util.get_current_unix_timestamp(),
                    "event": {
                        "props": {
                            "isCustomEvent": True,
                            "vwoMeta": {"metric": {"id_1": ["g_1"]}},
                            "vwo_sdkName": constants.SDK_NAME,
                            "vwo_sdkVersion": constants.SDK_VERSION,
                            "vwo_envKey": self.settings_file.get("sdkKey")
                        },
                        "name": "test_goal_identifier",
                        "time": generic_util.get_current_unix_timestamp_milli(),
                    },
                    "visitor": {"props": {"vwo_fs_environment": self.settings_file.get("sdkKey")}},
                }
            }

            result = impression_util.create_track_goal_events_impression(
                self.settings_file, TEST_USER_ID, "test_goal_identifier", [(1, 1, None)]
            )

            self.assertDictEqual(result, expected)

    def test_create_track_goal_events_impression_with_single_revenue(self):

        with mock.patch("vwo.helpers.generic_util.get_random_number", return_value="0.123456789"), mock.patch(
            "vwo.helpers.generic_util.get_current_unix_timestamp", return_value="123456789"
        ), mock.patch("vwo.helpers.generic_util.get_current_unix_timestamp_milli", return_value="123456789000"):

            expected = {
                "d": {
                    "msgId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID)
                    + "-"
                    + str(generic_util.get_current_unix_timestamp_milli()),
                    "visId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID),
                    "sessionId": generic_util.get_current_unix_timestamp(),
                    "event": {
                        "props": {
                            "isCustomEvent": True,
                            "vwoMeta": {"metric": {"id_1": ["g_1"]}, "revKey": 100},
                            "vwo_sdkName": constants.SDK_NAME,
                            "vwo_sdkVersion": constants.SDK_VERSION,
                            "vwo_envKey": self.settings_file.get("sdkKey")
                        },
                        "name": "test_goal_identifier",
                        "time": generic_util.get_current_unix_timestamp_milli(),
                    },
                    "visitor": {"props": {"vwo_fs_environment": self.settings_file.get("sdkKey")}},
                }
            }

            result = impression_util.create_track_goal_events_impression(
                self.settings_file, TEST_USER_ID, "test_goal_identifier", [(1, 1, "revKey")], [], 100
            )

            self.assertDictEqual(result, expected)

    def test_create_track_goal_events_impression_with_multiple_revenue(self):

        with mock.patch("vwo.helpers.generic_util.get_random_number", return_value="0.123456789"), mock.patch(
            "vwo.helpers.generic_util.get_current_unix_timestamp", return_value="123456789"
        ), mock.patch("vwo.helpers.generic_util.get_current_unix_timestamp_milli", return_value="123456789000"):

            expected = {
                "d": {
                    "msgId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID)
                    + "-"
                    + str(generic_util.get_current_unix_timestamp_milli()),
                    "visId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID),
                    "sessionId": generic_util.get_current_unix_timestamp(),
                    "event": {
                        "props": {
                            "isCustomEvent": True,
                            "vwoMeta": {
                                "metric": {"id_1": ["g_1"], "id_2": ["g_2"], "id_3": ["g_3"]},
                                "revKey1": 100,
                                "revKey2": 100,
                                "revKey3": 100,
                            },
                            "vwo_sdkName": constants.SDK_NAME,
                            "vwo_sdkVersion": constants.SDK_VERSION,
                            "vwo_envKey": self.settings_file.get("sdkKey")
                        },
                        "name": "test_goal_identifier",
                        "time": generic_util.get_current_unix_timestamp_milli(),
                    },
                    "visitor": {"props": {"vwo_fs_environment": self.settings_file.get("sdkKey")}},
                }
            }

            result = impression_util.create_track_goal_events_impression(
                self.settings_file,
                TEST_USER_ID,
                "test_goal_identifier",
                [(1, 1, "revKey1"), (2, 2, "revKey2"), (3, 3, "revKey3")], [],
                100,
            )

            self.assertDictEqual(result, expected)

    def test_create_push_events_impression_with_single_tag(self):

        with mock.patch("vwo.helpers.generic_util.get_random_number", return_value="0.123456789"), mock.patch(
            "vwo.helpers.generic_util.get_current_unix_timestamp", return_value="123456789"
        ), mock.patch("vwo.helpers.generic_util.get_current_unix_timestamp_milli", return_value="123456789000"):

            expected = {
                "d": {
                    "msgId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID)
                    + "-"
                    + str(generic_util.get_current_unix_timestamp_milli()),
                    "visId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID),
                    "sessionId": generic_util.get_current_unix_timestamp(),
                    "event": {
                        "props": {
                            "isCustomEvent": True,
                            "vwo_sdkName": constants.SDK_NAME,
                            "vwo_sdkVersion": constants.SDK_VERSION,
                            "vwo_envKey": self.settings_file.get("sdkKey")
                        },
                        "name": constants.EVENTS.VWO_SYNC_VISITOR_PROP,
                        "time": generic_util.get_current_unix_timestamp_milli(),
                    },
                    "visitor": {
                        "props": {"vwo_fs_environment": self.settings_file.get("sdkKey"), "tag_key": "tag_value"}
                    },
                }
            }

            result = impression_util.create_push_events_impression(
                self.settings_file, TEST_USER_ID, {"tag_key": "tag_value"}
            )

            self.assertDictEqual(result, expected)

    def test_create_push_events_impression_with_multiple_tags(self):

        with mock.patch("vwo.helpers.generic_util.get_random_number", return_value="0.123456789"), mock.patch(
            "vwo.helpers.generic_util.get_current_unix_timestamp", return_value="123456789"
        ), mock.patch("vwo.helpers.generic_util.get_current_unix_timestamp_milli", return_value="123456789000"):

            expected = {
                "d": {
                    "msgId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID)
                    + "-"
                    + str(generic_util.get_current_unix_timestamp_milli()),
                    "visId": uuid_util.generate_for(TEST_USER_ID, TEST_ACCOUNT_ID),
                    "sessionId": generic_util.get_current_unix_timestamp(),
                    "event": {
                        "props": {
                            "isCustomEvent": True,
                            "vwo_sdkName": constants.SDK_NAME,
                            "vwo_sdkVersion": constants.SDK_VERSION,
                            "vwo_envKey": self.settings_file.get("sdkKey")
                        },
                        "name": constants.EVENTS.VWO_SYNC_VISITOR_PROP,
                        "time": generic_util.get_current_unix_timestamp_milli(),
                    },
                    "visitor": {
                        "props": {
                            "vwo_fs_environment": self.settings_file.get("sdkKey"),
                            "tag_key_1": "tag_value_1",
                            "tag_key_2": "tag_value_2",
                            "tag_key_3": "tag_value_3",
                        }
                    },
                }
            }

            result = impression_util.create_push_events_impression(
                self.settings_file,
                TEST_USER_ID,
                {"tag_key_1": "tag_value_1", "tag_key_2": "tag_value_2", "tag_key_3": "tag_value_3"},
            )

            self.assertDictEqual(result, expected)

    def test_common_properties_with_ua_and_ip(self):
        common_properties = impression_util.get_common_properties(
            self.user_id, self.settings_file, self.visitor_ua, self.visitor_ip
        )
        expected_properties_subset = {
            constants.VISITOR.USER_AGENT: self.visitor_ua,
            constants.VISITOR.IP: self.visitor_ip,
        }
        self.assertDictContainsSubset(expected_properties_subset, common_properties)

    def test_event_params_with_ua_and_ip(self):
        event_params = impression_util.get_events_params(self.settings_file, "", self.visitor_ua, self.visitor_ip)
        expected_params_subset = {constants.VISITOR.USER_AGENT: self.visitor_ua, constants.VISITOR.IP: self.visitor_ip}
        self.assertDictContainsSubset(expected_params_subset, event_params)
