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

from __future__ import division
import mmh3 as Hasher
from ..constants import constants
from ..helpers import validate_util, campaign_util
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..logger import VWOLogger

# Took reference from StackOverflow(https://stackoverflow.com/) to:
# convert signed to unsigned integer in python from StackOverflow
# Author - Duncan (https://stackoverflow.com/users/107660/duncan)
# Source - https://stackoverflow.com/a/20766900/2494535
U_MAX_32_BIT = 0xFFFFFFFF
FILE = FileNameEnum.Core.Bucketer

# min and max range of bucket value
MIN_BUCKET_VALUE = 1
MAX_BUCKET_VALUE = 10000


class Bucketer(object):
    """Class consisting the core bucketing/distribution logic for
    the visitors"""

    def __init__(self):
        """Initializes bucketer with vwo common logger"""
        self.logger = VWOLogger.getInstance()

    def get_allocated_item(self, items, bucket_value):
        """Returns an allocation item(variation/campaign) by checking the Start and End
        Bucket Allocations of each item

        Args:
            items (list): list of item(variation/campaign)
            bucket_value (int): the bucket value of the user

        Returns:
            (dict|None): item(variation/campaign) allotted to the user or None if not
        """
        for item in items:
            if item.get("allocation_range_start") <= bucket_value <= item.get("allocation_range_end"):
                return item

        variations_log_string = ""
        for item in items:
            variations_log_string += str(item) + "\n"

        # log for None item
        self.logger.log(
            LogLevelEnum.ERROR,
            "tmpLog::bucketer::get_allocated_item() - Variation is None for bucket_value=" + str(bucket_value) + '. Variations details - ' + variations_log_string,
        )

        return None

    def get_bucket_value_for_user(self, user_seed, user_id, max_value, multiplier=1, disable_logs=False):
        """Returns Bucket Value of the user by hashing the userId with murmur hash and scaling it down.

        Args:
            user_id (string): the unique ID assigned to User
            max_value(int): maximum value that can be alloted to the bucket value
            multiplier(int): value for distributing ranges slightly
            disable_logs (bool): disable logs if True

        Returns:
            int: the bucket value allotted to User
            (between 1 to MAX_TRAFFIC_PERCENT)
        """

        # calculate valid bucket value
        hash_value = Hasher.hash(user_seed, constants.SEED_VALUE) & U_MAX_32_BIT
        ratio = hash_value / (2**32)
        multiplied_value = (max_value * ratio + 1) * multiplier
        bucket_value = int(multiplied_value)

        # set bucket value to the min/max value if outside ranges
        if bucket_value > MAX_BUCKET_VALUE:
            bucket_value = MAX_BUCKET_VALUE
        elif bucket_value < MIN_BUCKET_VALUE:
            bucket_value = MIN_BUCKET_VALUE

        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.USER_HASH_BUCKET_VALUE.format(
                file=FILE, hash_value=hash_value, bucket_value=bucket_value, user_id=user_id
            ),
            disable_logs,
        )
        return bucket_value

    def is_user_part_of_campaign(self, user_id, campaign, is_new_bucketing_enabled, disable_logs=False):
        """Calculates if the provided user_id should become part of the campaign or not

        Args:
            user_id (strings): the unique ID assigned to a user
            campaign (dict): for getting traffic allotted to the campaign
            disable_logs (bool): disable logs if True

        Returns:
            bool: if User is a part of Campaign or not
        """

        if not validate_util.is_valid_value(user_id):
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.INVALID_USER_ID.format(
                    file=FILE, user_id=user_id, method="is_user_part_of_campaign"
                ),
            )
            return False

        if not campaign:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.INVALID_CAMPAIGN.format(file=FILE, method="is_user_part_of_campaign"),
            )
            return False

        traffic_allocation = campaign.get("percentTraffic")

        value_assigned_to_user = self.get_bucket_value_for_user(
            campaign_util.get_bucketing_seed(is_new_bucketing_enabled=is_new_bucketing_enabled, user_id=user_id, campaign=campaign),
            user_id,
            constants.MAX_TRAFFIC_PERCENT,
            disable_logs=disable_logs,
        )
        is_user_part = value_assigned_to_user != 0 and value_assigned_to_user <= traffic_allocation
        self.logger.log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.USER_ELIGIBILITY_FOR_CAMPAIGN.format(
                file=FILE, user_id=user_id, is_user_part=is_user_part
            ),
            disable_logs,
        )
        return is_user_part

    def bucket_user_to_variation(self, user_id, campaign, is_new_bucketing_enabled):
        """Validates the User ID and
            returns Variation into which the User is bucketed in.

        Args:
            user_id (string): the unique ID assigned to User
            campaign (dict): the Campaign of which User is a part of

        Returns:
            (dict|None): variation data into which user is bucketed in
                or None if not
        """

        # set is_new_bucketing_enabled to False if not present
        if not is_new_bucketing_enabled:
            is_new_bucketing_enabled = False

        if not validate_util.is_valid_value(user_id):
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.INVALID_USER_ID.format(
                    file=FILE, user_id=user_id, method="bucket_user_to_variation"
                ),
            )
            return None

        if not campaign:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.INVALID_CAMPAIGN.format(file=FILE, method="bucket_user_to_variation"),
            )
            return None

        # logging for problem with percent traffic
        if campaign.get("percentTraffic") is not None and campaign.get("percentTraffic") == 0:
            log_str = (
                "tmpLog::bucketer::bucket_user_to_variation() - campaign="
                + campaign.get("key")
                + ", userId="
                + str(user_id)
                + ", percentTraffic="
                + str(campaign.get("percentTraffic"))
            )
            self.logger.log(LogLevelEnum.ERROR, log_str)
        elif campaign.get("percentTraffic") is None:
            log_str = (
                "tmpLog::bucketer::bucket_user_to_variation() - campaign="
                + campaign.get("key")
                + ", userId="
                + str(user_id)
                + ", percentTraffic=None"
            )
            self.logger.logger(LogLevelEnum.ERROR, log_str)

        # based on bucketing algo flag, determine bucket value
        if not is_new_bucketing_enabled or campaign.get("isOB"):
            # use old bucketing algo
            normalize = constants.MAX_TRAFFIC_VALUE / campaign.get("percentTraffic")
            multiplier = normalize / 100
            bucket_value = self.get_bucket_value_for_user(
                campaign_util.get_bucketing_seed(user_id=user_id, campaign=campaign, is_new_bucketing_enabled=is_new_bucketing_enabled),
                user_id,
                constants.MAX_TRAFFIC_VALUE,
                multiplier,
            )

            # log old algo
            self.logger.log(LogLevelEnum.DEBUG, "Using Old Algo!")
        else:
            # use new bucketing algo
            multiplier = 1
            bucket_value = self.get_bucket_value_for_user(
                campaign_util.get_bucketing_seed(user_id=user_id, campaign=None, is_new_bucketing_enabled=is_new_bucketing_enabled),
                user_id,
                constants.MAX_TRAFFIC_VALUE,
                multiplier,
            )

            # log new algo
            self.logger.log(LogLevelEnum.DEBUG, "Using New Algo!")

        # get valid bucket value
        """ normalize = constants.MAX_TRAFFIC_VALUE / campaign.get("percentTraffic")
        multiplier = normalize / 100
        bucket_value = self.get_bucket_value_for_user(
            campaign_util.get_bucketing_seed(user_id=user_id, campaign=campaign),
            user_id,
            constants.MAX_TRAFFIC_VALUE,
            multiplier,
        )
        """

        # logging for problem with bucket value
        if bucket_value is not None and (bucket_value < 1 or bucket_value > 10000):
            log_str = (
                "tmpLog::bucketer::bucket_user_to_variation() - campaign="
                + campaign.get("key")
                + ", userId="
                + str(user_id)
                + ", bucket_value="
                + str(bucket_value)
            )
            self.logger.log(LogLevelEnum.ERROR, log_str)
        elif bucket_value is None:
            log_str = (
                "tmpLog::bucketer::bucket_user_to_variation() - campaign="
                + campaign.get("key")
                + +", userId="
                + str(user_id)
                + ", bucket_value=None"
            )
            self.logger.log(LogLevelEnum.ERROR, log_str)

        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.VARIATION_HASH_BUCKET_VALUE.format(
                file=FILE,
                user_id=user_id,
                campaign_key=campaign.get("key"),
                percent_traffic=campaign.get("percentTraffic"),
                bucket_value=bucket_value,
            ),
        )

        return self.get_allocated_item(campaign.get("variations"), bucket_value)
