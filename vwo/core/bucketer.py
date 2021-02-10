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

from __future__ import division
import mmh3 as Hasher
from ..constants import constants
from ..helpers import validate_util
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


class Bucketer(object):
    """ Class consisting the core bucketing/distribution logic for
    the visitors """

    def __init__(self):
        """ Initializes bucketer with vwo common logger """
        self.logger = VWOLogger.getInstance()

    def get_variation(self, variations, bucket_value):
        """ Returns the Variation by checking the Start and End
        Bucket Allocations of each Variation

        Args:
            variations (list): list of variations
            bucket_value (int): the bucket value of the user

        Returns:
            (dict|None): variation data allotted to the user or None if not
        """
        for variation in variations:
            if variation.get("start_variation_allocation") <= bucket_value <= variation.get("end_variation_allocation"):
                return variation
        return None

    def get_bucket_value_for_user(self, user_id, max_value, multiplier=1):
        """ Returns Bucket Value of the user by hashing the userId with murmur hash and scaling it down.

        Args:
            user_id (string): the unique ID assigned to User
            max_value(int): maximum value that can be alloted to the bucket value
            multiplier(int): value for distributing ranges slightly
        Returns:
            int: the bucket value allotted to User
            (between 1 to MAX_TRAFFIC_PERCENT)
        """

        hash_value = Hasher.hash(user_id, constants.SEED_VALUE) & U_MAX_32_BIT
        ratio = hash_value / (2 ** 32)
        multiplied_value = (max_value * ratio + 1) * multiplier
        bucket_value = int(multiplied_value)

        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.USER_HASH_BUCKET_VALUE.format(
                file=FILE, hash_value=hash_value, bucket_value=bucket_value, user_id=user_id
            ),
        )
        return bucket_value

    def is_user_part_of_campaign(self, user_id, campaign):
        """ Calculates if the provided user_id should become part of the campaign or not

        Args:
            user_id (strings): the unique ID assigned to a user
            campaign (dict): for getting traffic allotted to the campaign

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

        value_assigned_to_user = self.get_bucket_value_for_user(user_id, constants.MAX_TRAFFIC_PERCENT)
        is_user_part = value_assigned_to_user != 0 and value_assigned_to_user <= traffic_allocation
        self.logger.log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.USER_ELIGIBILITY_FOR_CAMPAIGN.format(
                file=FILE, user_id=user_id, is_user_part=is_user_part
            ),
        )
        return is_user_part

    def bucket_user_to_variation(self, user_id, campaign):
        """ Validates the User ID and
            returns Variation into which the User is bucketed in.

        Args:
            user_id (string): the unique ID assigned to User
            campaign (dict): the Campaign of which User is a part of

        Returns:
            (dict|None): variation data into which user is bucketed in
                or None if not
        """

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

        normalize = constants.MAX_TRAFFIC_VALUE / campaign.get("percentTraffic")
        multiplier = normalize / 100
        bucket_value = self.get_bucket_value_for_user(user_id, constants.MAX_TRAFFIC_VALUE, multiplier)

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
        return self.get_variation(campaign.get("variations"), bucket_value)
