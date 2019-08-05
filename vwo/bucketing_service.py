""" Module encapsulating bucketing logic """

from __future__ import division
import mmh3 as Hasher
from .helpers import constants
from .helpers import validate_util
from .helpers.enums import LogMessageEnum, FileNameEnum, LogLevelEnum
from .logger import Logger


class Bucketer(object):
    """ Bucketer class encapsulating bucketing logic """

    def __init__(self):
        """ Initializes bucketer with project common logger

        Args:
            logger (object): Common project logger
        """
        self.logger = Logger()

    def _generate_bucket_value(self, hash_value, max_value, multiplier=1):
        """ Generates Bucket Value of the User by hashing the User ID by murmurHash
            and scaling it down.

        Args:
            hash_value (int): hashValue generated after hashing
            max_value (int): the value up-to which hashValue needs to be scaled
            multiplier (int): multiplier

        Returns:
            int: bucket Value of the User
        """

        ratio = hash_value / (2**32)
        multiplied_value = (max_value * ratio + 1) * multiplier
        return int(multiplied_value)

    def _get_variation(self, campaign, bucket_value):
        """ Returns the Variation by checking the Start and End
        Bucket Allocations of each Variation

        Args:
            campaign (dict): which contains the variations
            bucket_value (int): the bucket Value of the user

        Returns:
            (dict|None): variation data allotted to the user or None if not
        """
        for variation in campaign.get('variations'):
            if variation.get('start_variation_allocation') <= bucket_value <= variation.get('end_variation_allocation'):  # noqa:E501
                return variation
        return None

    def _get_bucket_value_for_user(self, user_id):
        """ Validates the User ID and generates Bucket Value of the
        User by hashing the userId by murmurHash and scaling it down.

        Args:
            user_id (string): the unique ID assigned to User

        Returns:
            int: the bucket Value allotted to User
            (between 1 to $this->$MAX_TRAFFIC_PERCENT)
        """

        if not validate_util.is_valid_value(user_id):
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.INVALID_USER_ID.format(
                    file=FileNameEnum.BucketingService,
                    user_id=user_id,
                    method='_get_bucket_value_for_user'
                )
            )
            return 0
        hash_value = Hasher.hash(user_id, constants.SEED_VALUE, signed=False)
        bucket_value = self._generate_bucket_value(hash_value,
                                                   constants.MAX_TRAFFIC_PERCENT
                                                   )

        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.USER_HASH_BUCKET_VALUE.format(
                file=FileNameEnum.BucketingService,
                hash_value=hash_value,
                bucket_value=bucket_value,
                user_id=user_id
            )
        )
        return bucket_value

    def is_user_part_of_campaign(self, user_id, campaign):
        """ Calculate if this user should become part of the campaign or not

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
                    file=FileNameEnum.BucketingService,
                    user_id=user_id,
                    method='is_user_part_of_campaign'
                )
            )
            return False

        if not campaign:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.INVALID_CAMPAIGN.format(
                    file=FileNameEnum.BucketingService,
                    method='is_user_part_of_campaign'
                )
            )
            return False

        traffic_allocation = campaign.get('percentTraffic')

        value_assigned_to_user = self._get_bucket_value_for_user(user_id)
        is_user_part = value_assigned_to_user != 0 and value_assigned_to_user <= traffic_allocation  # noqa: E501
        self.logger.log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.USER_ELIGIBILITY_FOR_CAMPAIGN.format(
                file=FileNameEnum.BucketingService,
                user_id=user_id,
                is_user_part=is_user_part
            )
        )
        return is_user_part

    def bucket_user_to_variation(self, user_id, campaign):
        """ Validates the User ID and
            generates Variation into which the User is bucketed in.

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
                    file=FileNameEnum.BucketingService,
                    user_id=user_id,
                    method='bucket_user_to_variation'
                )
            )
            return None

        if not campaign:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.INVALID_CAMPAIGN.format(
                    file=FileNameEnum.BucketingService,
                    method='is_user_part_of_campaign'
                )
            )
            return None

        hash_value = Hasher.hash(user_id, constants.SEED_VALUE, signed=False)
        normalize = constants.MAX_TRAFFIC_VALUE / campaign.get('percentTraffic')
        multiplier = normalize / 100
        bucket_value = self._generate_bucket_value(hash_value,
                                                   constants.MAX_TRAFFIC_VALUE,
                                                   multiplier
                                                   )

        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.VARIATION_HASH_BUCKET_VALUE.format(
                file=FileNameEnum.BucketingService,
                user_id=user_id,
                campaign_test_key=campaign.get('key'),
                percent_traffic=campaign.get('percentTraffic'),
                bucket_value=bucket_value,
                hash_value=hash_value
            )
        )
        return self._get_variation(campaign, bucket_value)
