import copy
from .helpers.enums import LogMessageEnum, FileNameEnum, LogLevelEnum
from .bucketing_service import Bucketer
from .helpers import validate_util, campaign_util
from .logger import Logger

FILE = FileNameEnum.DecisionService


class DecisionService(object):
    """ Class encapsulating all decision related capabilities. """

    def __init__(self, settings_file, user_profile_service=None):
        """ Initializes DecisionService with settings_file,
            UserProfileService and logger.

        Args:
            settings_file (dict): Settings file of the project.
            user_profile_service: Class instance having the capabilty of
                lookup and save.
        """
        self.logger = Logger.getInstance()
        self.user_profile_service = None
        # Check if user_profile_service provided is valid or not
        if validate_util.is_valid_utility(user_profile_service,
                                          'user_profile_service'
                                          ):
            self.user_profile_service = user_profile_service
        self.bucketer = Bucketer()
        self.settings_file = settings_file

    def get(self, user_id, campaign, campaign_test_key):
        """ Returns variation for the user for required campaign
            First looksup in the UPS, if user_profile is found,
                return from there
            Else, calculates the variation with helper method

        Args:
            user_id (string): the unique ID assigned to User
            campaign (dict): campaign in which user is participating
            campaign_test_key (string): the unique ID of the campaign passed

        Returns:
            ({variation_id, variation_name}|None): Tuple of
            variation_id and variation_name if variation alloted, else None
        """
        campaign_bucket_map = self._resolve_campaign_bucket_map(user_id, campaign_test_key)  # noqa:E501
        if type(campaign_bucket_map) is dict:
            variation = self._get_stored_variation(user_id,
                                                   campaign_test_key,
                                                   campaign_bucket_map
                                                   )

            if variation:
                self.logger.log(
                    LogLevelEnum.INFO,
                    LogMessageEnum.INFO_MESSAGES.GOT_STORED_VARIATION.format(
                        file=FILE,
                        campaign_test_key=campaign_test_key,
                        user_id=user_id,
                        variation_name=variation.get('name')
                    )
                )
                return variation.get('id'), variation.get('name')

        variation_id, variation_name = self.get_variation_allotted(user_id,
                                                                   campaign
                                                                   )

        if variation_name:
            self._save_user_profile(user_id, campaign_test_key, variation_name)
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.VARIATION_ALLOCATED.format(
                    file=FILE,
                    campaign_test_key=campaign_test_key,
                    user_id=user_id,
                    variation_name=variation_name
                )
            )
        else:
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.NO_VARIATION_ALLOCATED.format(
                    file=FILE,
                    campaign_test_key=campaign_test_key,
                    user_id=user_id
                )
            )
        return variation_id, variation_name

    def get_variation_allotted(self, user_id, campaign):
        """ Returns the Variation Allotted to User

        Args:
            user_id (string): the unique ID assigned to User
            campaign (dict): campaign bro

        Returns:
            dict: Variation object allotted to User
        """

        variation_id = None
        variation_name = None
        if not validate_util.is_valid_value(user_id):
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.INVALID_USER_ID.format(
                    file=FILE,
                    user_id=user_id,
                    method='get_variation_alloted'
                )
            )
            return variation_id, variation_name

        if self.bucketer.is_user_part_of_campaign(user_id, campaign):
            variation_id, variation_name = self.get_variation_of_campaign_for_user(user_id, campaign)  # noqa:E501
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.GOT_VARIATION_FOR_USER.format(
                    file=FILE,
                    variation_name=variation_name,
                    user_id=user_id,
                    campaign_test_key=campaign.get('key'),
                    method='get_variation_allotted'
                )
            )
        else:
            # not part of campaign
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.USER_NOT_PART_OF_CAMPAIGN.format(  # noqa:E501
                    file=FILE,
                    user_id=user_id,
                    campaign_test_key=None,
                    method='get_variation_allotted'
                )
            )
        return variation_id, variation_name

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
            return None, None

        variation = self.bucketer.bucket_user_to_variation(user_id, campaign)

        if variation and variation.get('name'):
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.GOT_VARIATION_FOR_USER.format(
                    file=FILE,
                    variation_name=variation.get('name'),
                    user_id=user_id,
                    campaign_test_key=campaign.get('key')
                )
            )
            return variation.get('id'), variation.get('name')

        self.logger.log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.USER_GOT_NO_VARIATION.format(
                file=FILE,
                user_id=user_id,
                campaign_test_key=campaign.get('key')
            )
        )
        return None, None

    # Private helper methods for UserProfileService

    def _get_stored_variation(self,
                              user_id,
                              campaign_test_key,
                              campaign_bucket_map
                              ):
        """ If userProfileService is provided and variation was stored,
        get the stored variation

        Args:
            user_id (string): user_id
            campaign_test_key (string): campaign identified
            campaign_bucket_map (dict):
                BucketMap consisting of stored user variation

        Returns:
            (Object|None): if found then variation settings object
                otherwise None
        """

        if campaign_bucket_map.get(campaign_test_key):
            decision = campaign_bucket_map.get(campaign_test_key)
            variation_name = decision.get('variationName')
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.GETTING_STORED_VARIATION.format(
                    file=FILE,
                    campaign_test_key=campaign_test_key,
                    user_id=user_id,
                    variation_name=variation_name
                )
            )
            return campaign_util.get_campaign_variation(self.settings_file,
                                                        campaign_test_key,
                                                        variation_name
                                                        )

        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.NO_STORED_VARIATION.format(
                file=FILE,
                campaign_test_key=campaign_test_key,
                user_id=user_id
            )
        )
        return None

    def _resolve_campaign_bucket_map(self, user_id, campaign_test_key):
        """ Returns the campaign bucket map corresponding to the user_id

        Args:
            user_id (string): Unique user identifier

        Returns:
            dict: data
        """

        user_data = self._get_user_profile(user_id, campaign_test_key)
        campaign_bucket_map = {}
        if user_data:
            campaign_bucket_map = user_data.get('campaignBucketMap')
        return copy.deepcopy(campaign_bucket_map)

    def _get_user_profile(self, user_id, campaign_test_key):
        """ Get the UserProfileData after looking up into lookup method
        being provided via UserProfileService

        Args:
            user_id (string): Unique user identifier

        Returns:
            dict: user_profile data
        """

        if not self.user_profile_service:
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.NO_USER_PROFILE_SERVICE_LOOKUP.format(  # noqa:E501
                    file=FILE
                )
            )
            return False
        try:
            data = self.user_profile_service.lookup(user_id, campaign_test_key)
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.LOOKING_UP_USER_PROFILE_SERVICE.format(  # noqa:E501
                    file=FILE,
                    user_id=user_id
                )
            )
            return data
        except Exception:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.LOOK_UP_USER_PROFILE_SERVICE_FAILED.format(  # noqa:E501
                    file=FILE,
                    user_id=user_id
                )
            )
            return False

    def _save_user_profile(self, user_id, campaign_test_key, variation_name):
        """ If userProfileService is provided and variation was stored,
        save the assigned variation
            It creates bucket and then stores.

        Args:
            user_id (string): Unique user identifier
            campaign_test_key (string): Unique campaign identifier
            variation_name (string): variation identifier

        Returns:
            bool: true if found otherwise false
        """

        if not self.user_profile_service:
            self.logger.log(
                LogLevelEnum.DEBUG,
                LogMessageEnum.DEBUG_MESSAGES.NO_USER_PROFILE_SERVICE_SAVE.format(  # noqa:E501
                    file=FILE
                )
            )
            return False
        try:
            new_campaign_bucket_map = {
                campaign_test_key: {
                    'variationName': variation_name
                }
            }
            self.user_profile_service.save(
                dict(
                    userId=user_id,
                    campaignBucketMap=new_campaign_bucket_map
                )
            )
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.SAVING_DATA_USER_PROFILE_SERVICE.format(  # noqa:E501
                    file=FILE,
                    user_id=user_id
                )
            )
            return True
        except Exception:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.SAVE_USER_PROFILE_SERVICE_FAILED.format(  # noqa:E501
                    file=FILE,
                    user_id=user_id
                )
            )
            return False
