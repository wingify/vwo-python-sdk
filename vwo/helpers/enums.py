# noqa: E501

""" Constants for logging errors and location of respective files of the project """
import logging


class FileNameEnum:
    """ Classobj encapsulating locations various files of the SDK """

    VWO_PATH = 'vwo'
    HELPERS_PATH = 'vwo/helpers'

    VWO = VWO_PATH + '/vwo'
    BucketingService = VWO_PATH + '/bucketing_service'
    DecisionService = VWO_PATH + '/decision_service'
    EventDispatcher = VWO_PATH + '/event_dispatcher'
    Logger = VWO_PATH + '/logger'
    ProjectConfigManager = VWO_PATH + '/project_config_manager'

    CampaignUtil = HELPERS_PATH + '/campaign_util'
    Functionutil = HELPERS_PATH + '/function_util'
    ImpressionUtil = HELPERS_PATH + '/impression_util'
    UuidUtil = HELPERS_PATH + '/uuid_util'
    ValidateUtil = HELPERS_PATH + '/validate_util'


class LogMessageEnum:
    """ Classobj encapsulating various logging messages """

    class DEBUG_MESSAGES:
        """ Classobj encapsulating various DEBUG messages """

        LOG_LEVEL_SET = '({file}): Log level set to {level}'
        SET_COLORED_LOG = '({file}): Colored log set to {value}'
        SET_DEVELOPMENT_MODE = '({file}): DEVELOPMENT mode is ON'
        VALID_CONFIGURATION = '({file}): SDK configuration and account settings are valid.'
        CUSTOM_LOGGER_USED = '({file}): Custom logger used'
        SDK_INITIALIZED = '({file}): SDK properly initialzed'
        SETTINGS_FILE_PROCESSED = '({file}): Settings file processed'
        NO_STORED_VARIATION = '({file}): No stored variation for UserId:{user_id} for Campaign:{campaign_test_key} found in UserProfileService'
        NO_USER_PROFILE_SERVICE_LOOKUP = '({file}): No UserProfileService to look for stored data'
        NO_USER_PROFILE_SERVICE_SAVE = '({file}): No UserProfileService to save data'
        GETTING_STORED_VARIATION = '({file}): Got stored variation for UserId:{user_id} of Campaign:{campaign_test_key} as Variation: {variation_name} found in UserProfileService'
        CHECK_USER_ELIGIBILITY_FOR_CAMPAIGN = '({file}): campaign:{campaign_test_key} having traffic allocation:{traffic_allocation} assigned value:{traffic_allocation} to userId:{user_id}'
        USER_HASH_BUCKET_VALUE = '({file}): userId:{user_id} having hash:{hash_value} got bucketValue:{bucket_value}'
        VARIATION_HASH_BUCKET_VALUE = '({file}): userId:{user_id} for campaign:{campaign_test_key} having percent traffic:{percent_traffic} got hash-value:{hash_value} and bucket value:{bucket_value}'
        GOT_VARIATION_FOR_USER = '({file}): userId:{user_id} for campaign:{campaign_test_key} got variationName:{variation_name} inside method:{method}'
        USER_NOT_PART_OF_CAMPAIGN = '({file}): userId:{user_id} for campaign:{campaign_test_key} did not become part of campaign method:{method}'
        UUID_FOR_USER = '({file}): Uuid generated for userId:{user_id} and accountId:{account_id} is {desired_uuid}'
        IMPRESSION_FOR_TRACK_USER = '({file}): Impression built for track-user - {properties}'
        IMPRESSION_FOR_TRACK_GOAL = '({file}): Impression built for track-goal - {properties}'

    class INFO_MESSAGES:
        """ Classobj encapsulating various INFO messages """

        VARIATION_RANGE_ALLOCATION = '({file}): Campaign:{campaign_test_key} having variations:{variation_name} with weight:{variation_weight} got range as: ( {start} - {end} ))'
        VARIATION_ALLOCATED = '({file}): UserId:{user_id} of Campaign:{campaign_test_key} got variation: {variation_name}'
        LOOKING_UP_USER_PROFILE_SERVICE = '({file}): Looked into UserProfileService for userId:{user_id} successful'
        SAVING_DATA_USER_PROFILE_SERVICE = '({file}): Saving into UserProfileService for userId:{user_id} successful'
        GOT_STORED_VARIATION = '({file}): Got stored variation:{variation_name} of campaign:{campaign_test_key} for userId:{user_id} from UserProfileService'
        NO_VARIATION_ALLOCATED = '({file}): UserId:{user_id} of Campaign:{campaign_test_key} did not get any variation'
        USER_ELIGIBILITY_FOR_CAMPAIGN = '({file}): Is userId:{user_id} part of campaign? {is_user_part}'
        AUDIENCE_CONDITION_NOT_MET = '({file}): userId:{user_id} does not become part of campaign because of not meeting audience conditions'
        GOT_VARIATION_FOR_USER = '({file}): userId:{user_id} for campaign:{campaign_test_key} got variationName:{variation_name}'
        USER_GOT_NO_VARIATION = '({file}): userId:{user_id} for campaign:{campaign_test_key} did not allot any variation'
        IMPRESSION_SUCCESS = '({file}): Impression event - {end_point} was successfully received by VWO having main keys: accountId:{account_id} userId:{user_id} campaignId:{campaign_id} and vairationId:{variation_id}'
        INVALID_VARIATION_KEY = '({file}): Variation was not assigned to userId:{user_id} for campaign:{campaign_test_key}'
        RETRY_FAILED_IMPRESSION_AFTER_DELAY = '({file}): Failed impression event for {end_point} will be retried after {retry_timeout} milliseconds delay'

    class WARNING_MESSAGES:
        """ Classobj encapsulating various WARNING messages """

        pass

    class ERROR_MESSAGES:
        """ Classobj encapsulating various ERROR messages """

        PROJECT_CONFIG_CORRUPTED = '({file}): config passed to createInstance is not a valid JSON object.'
        INVALID_CONFIGURATION = '({file}): SDK configuration or account settings or both is/are not valid.'
        SETTINGS_FILE_CORRUPTED = '({file}): Settings file is corrupted. Please contact VWO Support for help.'
        ACTIVATE_API_MISSING_PARAMS = '({file}): "activate" API got bad parameters. It expects campaignTestKey(String) as first and userId(String) as second argument'
        ACTIVATE_API_CONFIG_CORRUPTED = '({file}): "activate" API has corrupted configuration'
        GET_VARIATION_API_MISSING_PARAMS = '({file}): "getVariation" API got bad parameters. It expects campaignTestKey(String) as first and userId(String) as second argument'
        GET_VARIATION_API_CONFIG_CORRUPTED = '({file}): "getVariation" API has corrupted configuration'
        TRACK_API_MISSING_PARAMS = '({file}): "track" API got bad parameters. It expects campaignTestKey(String) as first userId(String) as second and goalIdentifier(String/Number) as third argument. Fourth is revenueValue(Float/Number/String) and is required for revenue goal only.'
        TRACK_API_CONFIG_CORRUPTED = '({file}): "track" API has corrupted configuration'
        TRACK_API_GOAL_NOT_FOUND = '({file}): Goal {goal} not found for campaign:{campaign_test_key} and userId:{user_id}'
        TRACK_API_VARIATION_NOT_FOUND = '({file}): Variation not found for campaign:{campaign_test_key} and userId:{user_id}'
        CAMPAIGN_NOT_RUNNING = '({file}): API used:{api} - Campaign:{campaign_test_key} is not RUNNING. Please verify from VWO App'
        LOOK_UP_USER_PROFILE_SERVICE_FAILED = '({file}): Looking data from UserProfileService failed for userId:{user_id}'
        SAVE_USER_PROFILE_SERVICE_FAILED = '({file}): Saving data into UserProfileService failed for userId:{user_id}'
        INVALID_CAMPAIGN = '({file}): Invalid campaign passed to {method} of this file'
        INVALID_USER_ID = '({file}): Invalid userId:{user_id} passed to {method} of this file'
        IMPRESSION_FAILED = '({file}): Impression event could not be sent to VWO - {end_point}'
        CUSTOM_LOGGER_MISCONFIGURED = '({file}): Custom logger is provided but seems to have misconfigured. {extra_info} Please check the API Docs. Using default logger.'


class LogLevelEnum:
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
