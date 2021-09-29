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


class UsageStats:
    """ Collect usage stats passed to the SDK """

    __usage_stats_data = {}

    @staticmethod
    def collect_usage_stats(**kwargs):
        """
        Collect the usage stats from the params passed to the SDK

        Keyword Args:
            batch_event_settings (dict): settings for configuring and enabling event batching
            integrations (object): an integrations service instance for third party integrations
            storage_service (object): a storage service object capable of doing get and set on
                SDK provide data
            goal_type_to_track (vwo.GOAL_TYPES): which goal type to track when using track api.
            logger (object): an object capable of logging events happening inside the SDK
            log_level (vwo.LOG_LEVELS): a log_level with which SDK should be initialized.
        """

        batch_event_settings = kwargs.get("batch_event_settings")
        integrations = kwargs.get("integrations")
        storage_service = kwargs.get("storage_service")
        goal_type_to_track = kwargs.get("goal_type_to_track")
        logger = kwargs.get("logger")
        log_level = kwargs.get("log_level")

        data = {
            "eb": int(bool(batch_event_settings)),
            "ig": int(bool(integrations)),
            "ss": int(bool(storage_service)),
            "cl": int(bool(logger)),
            "ll": int(bool(log_level)),
            "gt": int(bool(goal_type_to_track)),
        }

        # removing falsy keys from payload
        UsageStats.__usage_stats_data = {k: v for k, v in data.items() if v}

        if UsageStats.__usage_stats_data:
            UsageStats.__usage_stats_data.update({"_l": 1})

    @staticmethod
    def get_usage_stats():
        """
        Returns the collected usage stats

        Returns:
            dict: collected usage stats data
        """

        return UsageStats.__usage_stats_data
