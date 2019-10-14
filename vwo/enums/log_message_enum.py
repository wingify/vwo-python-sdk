# flake8: noqa

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
        NO_STORED_VARIATION = '({file}): No stored variation for UserId:{user_id} for Campaign:{campaign_key} found in UserStorage'
        NO_user_storage_get = '({file}): No UserStorage to look for stored data'
        NO_user_storage_set = '({file}): No UserStorage to set data'
        GETTING_STORED_VARIATION = '({file}): Got stored variation for UserId:{user_id} of Campaign:{campaign_key} as Variation: {variation_name} found in UserStorage'
        CHECK_USER_ELIGIBILITY_FOR_CAMPAIGN = '({file}): campaign:{campaign_key} having traffic allocation:{traffic_allocation} assigned value:{traffic_allocation} to userId:{user_id}'
        USER_HASH_BUCKET_VALUE = '({file}): userId:{user_id} having hash:{hash_value} got bucketValue:{bucket_value}'
        VARIATION_HASH_BUCKET_VALUE = '({file}): userId:{user_id} for campaign:{campaign_key} having percent traffic:{percent_traffic} got hash-value:{hash_value} and bucket value:{bucket_value}'
        GOT_VARIATION_FOR_USER = '({file}): userId:{user_id} for campaign:{campaign_key} type: {campaign_type} got variationName:{variation_name} inside method:{method}'
        USER_NOT_PART_OF_CAMPAIGN = '({file}): userId:{user_id} for campaign:{campaign_key} type: {campaign_type} did not become part of campaign method:{method}'
        UUID_FOR_USER = '({file}): Uuid generated for userId:{user_id} and accountId:{account_id} is {desired_uuid}'
        IMPRESSION_FOR_TRACK_USER = '({file}): Impression built for track-user - {properties}'
        IMPRESSION_FOR_TRACK_GOAL = '({file}): Impression built for track-goal - {properties}'

    class INFO_MESSAGES:
        """ Classobj encapsulating various INFO messages """

        VARIATION_RANGE_ALLOCATION = '({file}): Campaign:{campaign_key} having variations:{variation_name} with weight:{variation_weight} got range as: ( {start} - {end} ))'
        VARIATION_ALLOCATED = '({file}): UserId:{user_id} of Campaign:{campaign_key} type: {campaign_type} got variation: {variation_name}'
        LOOKING_UP_user_storage = '({file}): Looked into UserStorage for userId:{user_id} successful'
        SAVING_DATA_user_storage = '({file}): Saving into UserStorage for userId:{user_id} successful'
        GOT_STORED_VARIATION = '({file}): Got stored variation:{variation_name} of campaign:{campaign_key} for userId:{user_id} from UserStorage'
        NO_VARIATION_ALLOCATED = '({file}): UserId:{user_id} of Campaign:{campaign_key} type: {campaign_type} did not get any variation'
        USER_ELIGIBILITY_FOR_CAMPAIGN = '({file}): Is userId:{user_id} part of campaign? {is_user_part}'
        AUDIENCE_CONDITION_NOT_MET = '({file}): userId:{user_id} does not become part of campaign because of not meeting audience conditions'
        GOT_VARIATION_FOR_USER = '({file}): userId:{user_id} for campaign:{campaign_key} type: {campaign_type} got variationName:{variation_name}'
        USER_GOT_NO_VARIATION = '({file}): userId:{user_id} for campaign:{campaign_key} type: {campaign_type} did not allot any variation'
        IMPRESSION_SUCCESS = '({file}): Impression event - {end_point} was successfully received by VWO having main keys: accountId:{account_id} userId:{user_id} campaignId:{campaign_id} and variationId:{variation_id}'
        INVALID_VARIATION_KEY = '({file}): Variation was not assigned to userId:{user_id} for campaign:{campaign_key}'
        RETRY_FAILED_IMPRESSION_AFTER_DELAY = '({file}): Failed impression event for {end_point} will be retried after {retry_timeout} milliseconds delay'

        USER_IN_FEATURE_ROLLOUT = '({file}): User ID:{user_id} is in feature rollout:{campaign_key}'
        USER_NOT_IN_FEATURE_ROLLOUT = '({file}): User ID:{user_id} is NOT in feature rollout:{campaign_key}'
        FEATURE_ENABLED_FOR_USER = '({file}): Feature having feature-key:{feature_key} for user ID:{user_id} is enabled'
        FEATURE_NOT_ENABLED_FOR_USER = '({file}): Feature having feature-key:{feature_key} for user ID:{user_id} is not enabled'

        VARIABLE_FOUND = '({file}): Value for variable:{variable_key} of campaign:{campaign_key} and campaign type: {campaign_type} is:{variable_value} for user:{user_id}'
        USER_IN_CAMPAIGN = '({file}): userId:{user_id} did become part of campaign:{campaign_key} and campaign type:{campaign_type} having variation {variation_name}'

    class WARNING_MESSAGES:
        """ Classobj encapsulating various WARNING messages """

    class ERROR_MESSAGES:
        """ Classobj encapsulating various ERROR messages """

        PROJECT_CONFIG_CORRUPTED = '({file}): config passed to createInstance is not a valid JSON object.'
        INVALID_CONFIGURATION = '({file}): SDK configuration or account settings or both is/are not valid.'
        SETTINGS_FILE_CORRUPTED = '({file}): Settings file is corrupted. Please contact VWO Support for help.'
        ACTIVATE_API_MISSING_PARAMS = '({file}): "activate" API got bad parameters. It expects campaignKey(String) as first and userId(String) as second argument'
        ACTIVATE_API_CONFIG_CORRUPTED = '({file}): "activate" API has corrupted configuration'
        GET_VARIATION_NAME_API_MISSING_PARAMS = '({file}): "getVariationName" API got bad parameters. It expects campaignKey(String) as first and userId(String) as second argument'
        GET_VARIATION_NAME_API_CONFIG_CORRUPTED = '({file}): "getVariationName" API has corrupted configuration'
        TRACK_API_MISSING_PARAMS = '({file}): "track" API got bad parameters. It expects campaignKey(String) as first userId(String) as second and goalIdentifier(String/Number) as third argument. Fourth is revenueValue(Float/Number/String) and is required for revenue goal only.'
        TRACK_API_CONFIG_CORRUPTED = '({file}): "track" API has corrupted configuration'
        TRACK_API_GOAL_NOT_FOUND = '({file}): Goal:{goal_identifier} not found for campaign:{campaign_key} and userId:{user_id}'
        TRACK_API_REVENUE_NOT_PASSED_FOR_REVENUE_GOAL = '({file}): Revenue value should be passed for revenue goal:{goal_identifier} for campaign:{campaign_key} and userId:{user_id}'
        TRACK_API_VARIATION_NOT_FOUND = '({file}): Variation not found for campaign:{campaign_key} and userId:{user_id}'
        CAMPAIGN_NOT_RUNNING = '({file}): API used:{api_name} - Campaign:{campaign_key} is not RUNNING. Please verify from VWO App'
        LOOK_UP_user_storage_FAILED = '({file}): Looking data from UserStorage failed for userId:{user_id}'
        set_user_storage_FAILED = '({file}): Saving data into UserStorage failed for userId:{user_id}'
        INVALID_CAMPAIGN = '({file}): Invalid campaign passed to {method} of this file'
        INVALID_USER_ID = '({file}): Invalid userId:{user_id} passed to {method} of this file'
        IMPRESSION_FAILED = '({file}): Impression event could not be sent to VWO - {end_point}'
        CUSTOM_LOGGER_MISCONFIGURED = '({file}): Custom logger is provided but seems to have misconfigured. {extra_info} Please check the API Docs. Using default logger.'

        INVALID_API = '({file}): {api_name} API is not valid for user ID: {user_id} in campaign ID: {campaign_key} having campaign type: {campaign_type}.'
        IS_FEATURE_ENABLED_API_MISSING_PARAMS = '({file}): "is_feature_enabled" API got bad parameters. It expects campaign_key(String) as first and user_id(String) as second argument'
        IS_FEATURE_ENABLED_API_CONFIG_CORRUPTED = '({file}): "is_feature_enabled" API has corrupted configuration'
        GET_FEATURE_VARIABLE_CONFIG_CORRUPTED = '({file}): "get_feature_variable_type" API has corrupted configuration'
        GET_FEATURE_VARIABLE_MISSING_PARAMS = '({file}): "get_feature_variable" API got bad parameters. It expects campaign_key(String) as first, variable_key(string) as second and user_id(String) as third argument'

        VARIABLE_NOT_FOUND = '({file}): Variable {variable_key} not found for campaing {campaign_key} and type {campaign_type} for user ID {user_id}'
        UNABLE_TO_TYPE_CAST = '({file}): Unable to typecast value: {value} of type: {of_type} to type: {variable_type}.'
        VARIABLE_REQUESTED_WITH_WRONG_TYPE = '({file}): Got variable type:{got_variable_type}, but expected variable is of type:{expected_variable_type}. Please read docs and use correct API. Returning None.'

        USER_NOT_IN_CAMPAIGN = '({file}): userId:{user_id} did not become part of campaign:{campaign_key} and campaign type:{campaign_type}'
        API_NOT_WORKING = '({file}): API: {api_name} not working, exception caught: {exception}. Please contact VWO Support for help.'
