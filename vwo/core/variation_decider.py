import copy
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..helpers import validate_util, campaign_util
from ..logger.logger_manager import VWOLogger
from .bucketer import Bucketer

FILE = FileNameEnum.VariationDecider


class VariationDecider(object):
    """ Class responsible for deciding the variation for a visitor """

    def __init__(self, settings_file, user_storage=None):
        """ Initializes VariationDecider with settings_file,
            UserStorage and logger.

        Args:
            settings_file (dict): Settings file of the project.
            user_storage: Class instance having the capabilty of
                get and set.
        """
        self.logger = VWOLogger.getInstance()
        self.user_storage = None
        # Check if user_storage provided is valid or not
        if validate_util.is_valid_service(user_storage,
                                          'user_storage'
                                          ):
            self.user_storage = user_storage
        self.bucketer = Bucketer()
        self.settings_file = settings_file

    def get_variation(self, user_id, campaign, campaign_key):
        """ Returns variation for the user for required campaign
            First looksup in the UPS, if user_storage_data is found,
                return from there
            Else, calculates the variation with helper method

        Args:
            user_id (string): the unique ID assigned to User
            campaign (dict): campaign in which user is participating
            campaign_key (string): the unique ID of the campaign passed

        Returns:
            ({variation_id, variation_name}|None): Tuple of
            variation_id and variation_name if variation alloted, else None
        """
        user_campaign_map = self._get_user_storage_data(user_id, campaign_key)  # noqa:E501
        if type(user_campaign_map) is dict:
            variation = self._get_stored_variation(user_id,
                                                   campaign_key,
                                                   user_campaign_map
                                                   )

            if variation:
                self.logger.log(
                    LogLevelEnum.INFO,
                    LogMessageEnum.INFO_MESSAGES.GOT_STORED_VARIATION.format(
                        file=FILE,
                        campaign_key=campaign_key,
                        user_id=user_id,
                        variation_name=variation.get('name')
                    )
                )
                return variation

        variation = self.get_variation_allotted(user_id,
                                                campaign
                                                )

        if variation and variation.get('name'):
            self._set_user_storage_data(user_id,
                                        campaign_key,
                                        variation.get('name'))
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.VARIATION_ALLOCATED.format(
                    file=FILE,
                    campaign_key=campaign_key,
                    user_id=user_id,
                    variation_name=variation.get('name'),
                    campaign_type=campaign.get('type')
                )
            )
        else:
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.NO_VARIATION_ALLOCATED.format(
                    file=FILE,
                    campaign_key=campaign_key,
                    user_id=user_id,
                    campaign_type=campaign.get('type')
                )
            )
        return variation

    def get_variation_allotted(self, user_id, campaign):
        """ Returns the Variation Allotted to User

        Args:
            user_id (string): the unique ID assigned to User
            campaign (dict): campaign bro

        Returns:
            dict: Variation object allotted to User
        """

        if not validate_util.is_valid_value(user_id):
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.INVALID_USER_ID.format(
                    file=FILE,
                    user_id=user_id,
                    method='get_variation_alloted'
                )
            )
            return None

        if self.bucketer.is_user_part_of_campaign(user_id, campaign):
            variation = self.get_variation_of_campaign_for_user(user_id, campaign)
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.GOT_VARIATION_FOR_USER.format(
                    file=FILE,
                    variation_name=variation.get('name'),
                    user_id=user_id,
                    campaign_key=campaign.get('key'),
                    method='get_variation_allotted',
                    campaign_type=campaign.get('type')
                )
            )
            return variation
        else:
            # not part of campaign
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.USER_NOT_PART_OF_CAMPAIGN.format(
                    file=FILE,
                    user_id=user_id,
                    campaign_key=campaign.get('key'),
                    method='get_variation_allotted',
                    campaign_type=campaign.get('type')
                )
            )
        return None

    def get_variation_of_campaign_for_user(self, user_id, campaign):
        """ Assigns random variation ID to a particular user
            depending on the PercentTraffic.
            Makes user a part of campaign if user's included in Traffic.

        Args:
            user_id (string): the unique ID assigned to a user
            campaign (dict): the Campaign of which user is to be made a part of

        Returns:
            (dict|None): Variation allotted to User
        """
        if not campaign:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.INVALID_CAMPAIGN.format(
                    file=FILE,
                    method='get_variation_of_campaign_for_user'
                )
            )
            return None

        variation = self.bucketer.bucket_user_to_variation(user_id, campaign)

        if variation and variation.get('name'):
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.GOT_VARIATION_FOR_USER.format(
                    file=FILE,
                    variation_name=variation.get('name'),
                    user_id=user_id,
                    campaign_key=campaign.get('key'),
                    campaign_type=campaign.get('type')
                )
            )
            return variation

        self.logger.log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.USER_GOT_NO_VARIATION.format(
                file=FILE,
                user_id=user_id,
                campaign_key=campaign.get('key'),
                campaign_type=campaign.get('type')
            )
        )
        return None

    # Private helper methods for UserStorage

    def _get_stored_variation(self,
                              user_id,
                              campaign_key,
                              user_campaign_map
                              ):
        """ If UserStorage is provided and variation was stored,
        get the stored variation

        Args:
            user_id (string): user_id
            campaign_key (string): campaign identified
            user_campaign_map (dict):
                BucketMap consisting of stored user variation

        Returns:
            (Object|None): if found then variation settings object
                otherwise None
        """

        if user_campaign_map.get('campaignTestKey') == campaign_key:
            variation_name = user_campaign_map.get('variationName')
            if variation_name:
                self.logger.log(
                    LogLevelEnum.DEBUG,
                    LogMessageEnum.DEBUG_MESSAGES.GETTING_STORED_VARIATION.format(
                        file=FILE,
                        campaign_key=campaign_key,
                        user_id=user_id,
                        variation_name=variation_name
                    )
                )
                campaign = campaign_util.get_campaign(self.settings_file,
                                                      campaign_key)
                return campaign_util.get_campaign_variation(campaign,
                                                            variation_name
                                                            )

        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.NO_STORED_VARIATION.format(
                file=FILE,
                campaign_key=campaign_key,
                user_id=user_id
            )
        )
        return None

    def _get_user_storage_data(self, user_id, campaign_key):
        """ Get the UserStorageData after looking up into get method
        being provided via UserStorage

        Args:
            user_id (string): Unique user identifier

        Returns:
            dict: user_storage_data data
        """

        if not self.user_storage:
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.NO_user_storage_get.format(
                    file=FILE
                )
            )
            return False
        try:
            user_campaign_map = self.user_storage.get(user_id, campaign_key)
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.LOOKING_UP_user_storage.format(
                    file=FILE,
                    user_id=user_id
                )
            )
            return copy.deepcopy(user_campaign_map)
        except Exception:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.LOOK_UP_user_storage_FAILED.format(
                    file=FILE,
                    user_id=user_id
                )
            )
            return False

    def _set_user_storage_data(self, user_id, campaign_key, variation_name):
        """ If UserStorage is provided and variation was stored,
        set the assigned variation
            It creates bucket and then stores.

        Args:
            user_id (string): Unique user identifier
            campaign_key (string): Unique campaign identifier
            variation_name (string): variation identifier

        Returns:
            bool: true if found otherwise false
        """

        if not self.user_storage:
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.NO_user_storage_set.format(
                    file=FILE
                )
            )
            return False

        new_user_campaign_map = {
            "userId": user_id,
            "campaignTestKey": campaign_key,
            "variationName": variation_name
        }
        try:
            self.user_storage.set(new_user_campaign_map)
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.SAVING_DATA_user_storage.format(
                    file=FILE,
                    user_id=user_id
                )
            )
            return True
        except Exception:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.set_user_storage_FAILED.format(
                    file=FILE,
                    user_id=user_id
                )
            )
            return False
