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


class LogMessageEnum:
    """ Classobj encapsulating various logging messages """

    class DEBUG_MESSAGES:
        """ Classobj encapsulating various DEBUG messages """

        LOG_LEVEL_SET = "({file}): [API_NAME] Log level set to {level}"
        SET_DEVELOPMENT_MODE = "({file}): [API_NAME] DEVELOPMENT mode is ON"
        VALID_CONFIGURATION = "({file}): [API_NAME] SDK configuration and account settings are valid."
        CUSTOM_LOGGER_USED = "({file}): [API_NAME] Custom logger used"
        LOGGING_LOGGER_INSTANCE_USED = "({file}): [API_NAME] Python logging module's logger instantiated"
        SDK_INITIALIZED = "({file}): [API_NAME] SDK properly initialzed"
        SETTINGS_FILE_PROCESSED = "({file}): [API_NAME] Settings file processed"
        NO_STORED_VARIATION = "({file}): [API_NAME] No stored variation for user_id:{user_id} for campaign_key:{campaign_key} found in UserStorage"
        NO_USER_STORAGE_GET = "({file}): [API_NAME] No UserStorage to get data"
        NO_USER_STORAGE_SET = "({file}): [API_NAME] No UserStorage to set data"
        GETTING_STORED_VARIATION = "({file}): [API_NAME] Got stored variation for user_id:{user_id} of campaign_key:{campaign_key} as variation: {variation_name} found in UserStorage"
        USER_HASH_BUCKET_VALUE = (
            "({file}): [API_NAME] user_id:{user_id} having hash:{hash_value} got bucketValue:{bucket_value}"
        )
        VARIATION_HASH_BUCKET_VALUE = "({file}): [API_NAME] user_id:{user_id} for campaign_key:{campaign_key} having percent traffic:{percent_traffic} got bucket value:{bucket_value}"
        GOT_VARIATION_FOR_USER = "({file}): [API_NAME] user_id:{user_id} for campaign_key:{campaign_key} type: {campaign_type} got variation_name:{variation_name} inside method:{method}"
        USER_NOT_PART_OF_CAMPAIGN = "({file}): [API_NAME] user_id:{user_id} for campaign_key:{campaign_key} type: {campaign_type} did not become part of campaign method:{method}"
        UUID_FOR_USER = (
            "({file}): [API_NAME] Uuid generated for user_id:{user_id} and account_id:{account_id} is {desired_uuid}"
        )
        IMPRESSION_FOR_TRACK_USER = "({file}): [API_NAME] Impression built for track-user - {properties}"
        IMPRESSION_FOR_TRACK_GOAL = "({file}): [API_NAME] Impression built for track-goal - {properties}"

        PARAMS_FOR_PUSH_CALL = "({file}): [API_NAME] Params for push call - {properties}"

        NO_VARIABLES = "({file}): [API_NAME] For user_id:{user_id} of campaign: {campaign_key} variables are not passed for {segmentation_type}"
        SEGMENTATION_SKIPPED = "({file}): [API_NAME] For user_id:{user_id} of campaign_key: {campaign_key} segments are missing, hence skipping segmentation {variation_status}"
        SEGMENTATION_STATUS = "({file}): [API_NAME] For user_id: {user_id} of campaign_key:{campaign_key} with variables:{variables} {status} {segmentation_type} {variation_status}"

        WHITELISTING_SKIPPED = (
            "({file}): [API_NAME] For user_id:{user_id} of campaign:{campaign_key}, whitelisting is skipped"
        )

        BEFORE_FLUSHING = "({file}): Flushing events queue {manually} having {length} events. {timer}, queue summary: {queue_metadata}"
        CAMPAIGN_NOT_ACTIVATED = "({file}): Campaign:{campaign_key} for User ID:{user_id} is not yet activated for API:{api_method}. Use activate API to activate A/B test or isFeatureEnabled API to activate Feature Test."

    class INFO_MESSAGES:
        """ Classobj encapsulating various INFO messages """

        VARIATION_RANGE_ALLOCATION = "({file}): [API_NAME] campaign_key:{campaign_key} having variations:{variation_name} with weight:{variation_weight} got range as: ( {start} - {end} ))"
        VARIATION_ALLOCATED = "({file}): [API_NAME] user_id:{user_id} of campaign_key:{campaign_key} type: {campaign_type} got variation: {variation_name}"
        FORCED_VARIATION_ALLOCATED = "({file}): [API_NAME] user_id:{user_id} of campaign_key:{campaign_key} type: {campaign_type} got forced-variation: {variation_name}"
        LOOKING_UP_USER_STORAGE = "({file}): [API_NAME] Looked into UserStorage for user_id:{user_id} successful"
        SAVING_DATA_USER_STORAGE_STATUS = "({file}): [API_NAME] Saving into UserStorage for user_id:{user_id} {status}"
        GOT_STORED_VARIATION = "({file}): [API_NAME] Got stored variation:{variation_name} of campaign_key:{campaign_key} for user_id:{user_id} from UserStorage"
        NO_VARIATION_ALLOCATED = "({file}): [API_NAME] user_id:{user_id} of campaign_key:{campaign_key} type: {campaign_type} did not get any variation"
        USER_ELIGIBILITY_FOR_CAMPAIGN = "({file}): [API_NAME] Is user_id:{user_id} part of campaign? {is_user_part}"
        GOT_VARIATION_FOR_USER = "({file}): [API_NAME] user_id:{user_id} for campaign_key:{campaign_key} type: {campaign_type} got variation_name:{variation_name}"
        USER_GOT_NO_VARIATION = "({file}): [API_NAME] user_id:{user_id} for campaign_key:{campaign_key} type: {campaign_type} did not allot any variation"
        IMPRESSION_SUCCESS = "({file}): [API_NAME] Impression event - {end_point} was successfully received by VWO"
        IMPRESSION_SUCCESS_QUEUE = "({file}): [API_NAME] Impression event - {end_point} was successfully pushed in queue, current queue length : {queue_length}, queue summary: {queue_metadata}"
        MAIN_KEYS_FOR_IMPRESSION = "({file}): [API_NAME] Having main keys: account_id:{account_id} campaignId:{campaign_id} and variation_id:{variation_id}"
        MAIN_KEYS_FOR_PUSH_API = "({file}): [API_NAME] Having main keys: account_id:{account_id} u:{u} and tags:{tags}"
        INVALID_VARIATION_KEY = (
            "({file}): [API_NAME] variation was not assigned to user_id:{user_id} for campaign_key:{campaign_key}"
        )
        RETRY_FAILED_IMPRESSION_AFTER_DELAY = "({file}): [API_NAME] Failed impression event for {end_point} will be retried after {retry_timeout} milliseconds delay"

        USER_IN_FEATURE_ROLLOUT = "({file}): [API_NAME] User ID:{user_id} is in feature rollout:{campaign_key}"
        USER_NOT_IN_FEATURE_ROLLOUT = "({file}): [API_NAME] User ID:{user_id} is NOT in feature rollout:{campaign_key}"
        FEATURE_ENABLED_FOR_USER = (
            "({file}): [API_NAME] Feature having feature-key:{feature_key} for user ID:{user_id} is enabled"
        )
        FEATURE_NOT_ENABLED_FOR_USER = (
            "({file}): [API_NAME] Feature having feature-key:{feature_key} for user ID:{user_id} is not enabled"
        )

        VARIABLE_FOUND = "({file}): [API_NAME] Value for variable:{variable_key} of campaign_key:{campaign_key} and campaign type: {campaign_type} is:{variable_value} for user:{user_id}"

        SEGMENTATION_STATUS = "({file}): [API_NAME] user_id:{user_id} of campaign_key:{campaign_key} with variables: {variables} {status} {segmentation_type} {variation_status}"

        GOAL_ALREADY_TRACKED = "({file}): [API_NAME] Goal:{goal_identifier} of Campaign:{campaign_key} for User ID:{user_id} has already been tracked earlier. Skipping now. Check docs on how to force tracking for returning visitors."
        USER_ALREADY_TRACKED = "({file}): [API_NAME] User ID:{user_id} for Campaign:{campaign_key} has already been tracked earlier for '{api_method}' API. Skipping now"
        SETTINGS_FILE_UPDATED = "({file}): [API_NAME] vwo_sdk_instance is updated with the latest settings_file"
        SETTINGS_FILE_NOT_UPDATED = "({file}): [API_NAME] settings_file fetched are same as earlier fetched settings"

        BULK_IMPRESSION_SUCCESS = (
            "({file}): Impression event - {end_point} was successfully received by VWO having account_id:{account_id}"
        )

        AFTER_FLUSHING = (
            "({file}): Events queue having {length} events has been flushed {manually}, queue summary: {queue_metadata}"
        )
        CAMPAIGN_NOT_ACTIVATED = "({file}): Activate the campaign:{campaign_key} for User ID:{user_id} to {reason}."

    class WARNING_MESSAGES:
        """ Classobj encapsulating various WARNING messages """

    class ERROR_MESSAGES:
        """ Classobj encapsulating various ERROR messages """

        LAUNCH_API_INVALID_PARAMS = (
            "({file}): [API_NAME] Params passed to the launch API are not correct. Please refer the docs.."
        )
        ACTIVATE_API_INVALID_PARAMS = "({file}): [API_NAME] API got bad parameters. It expects campaign_key(String) as first and user_id(String) as second argument, custom_variables(dict) for pre-segmentation, variation_targeting_variables(dict) for white-listing and should_track_returning_user(bool) for tracking returning users can be passed via kwargs"
        API_CONFIG_CORRUPTED = "({file}): [API_NAME] API has corrupted configuration"
        GET_VARIATION_NAME_API_INVALID_PARAMS = "({file}): [API_NAME] API got bad parameters. It expects campaign_key(String) as first and user_id(String) as second argument, custom_variables(dict) for pre-segmentation and variation_targeting_variables(dict) for white-listing can be passed via kwargs"
        TRACK_API_INVALID_PARAMS = "({file}): [API_NAME] API got bad parameters. It expects campaign_key(String or Array of Strings or None) as first user_id(String) as second and goal_identifier(String/Number) as third argument. revenue_value(Float/Number/String) can be passed through kwargs and is required for revenue goal only. custom_variables(dict) for pre-segmentation and variation_targeting_variables(dict) for white-listing can be passed via kwargs"
        TRACK_API_GOAL_NOT_FOUND = "({file}): [API_NAME] Goal:{goal_identifier} not found for campaign_key:{campaign_key} and user_id:{user_id}"
        TRACK_API_REVENUE_NOT_PASSED_FOR_REVENUE_GOAL = "({file}): [API_NAME] Revenue value should be passed for revenue goal:{goal_identifier} for campaign_key:{campaign_key} and user_id:{user_id}"
        TRACK_API_VARIATION_NOT_FOUND = (
            "({file}): [API_NAME] variation not found for campaign_key:{campaign_key} and user_id:{user_id}"
        )
        CAMPAIGN_NOT_RUNNING = (
            "({file}): [API_NAME] campaign_key:{campaign_key} is not RUNNING. Please verify from VWO App"
        )
        LOOK_UP_USER_STORAGE_FAILED = "({file}): [API_NAME] Looking data from UserStorage failed for user_id:{user_id}"
        SET_USER_STORAGE_FAILED = "({file}): [API_NAME] Error while saving data into UserStorage for user_id:{user_id}. Error message: {error_message}"
        INVALID_CAMPAIGN = "({file}): [API_NAME] Invalid campaign passed to {method} of this file"
        INVALID_USER_ID = "({file}): [API_NAME] Invalid user_id:{user_id} passed to {method} of this file"
        IMPRESSION_FAILED = "({file}): [API_NAME] Impression event could not be sent to VWO - {end_point}"
        IMPRESSION_FAILED_QUEUE = "({file}): [API_NAME] Impression event could not be pushed in queue - {end_point}"
        CUSTOM_LOGGER_MISCONFIGURED = "({file}): [API_NAME] Custom logger is provided but seems to have misconfigured. {extra_info} Please check the API Docs. Using default logger."

        INVALID_API = "({file}): [API_NAME] API is not valid for user ID: {user_id} in campaign ID: {campaign_key} having campaign type: {campaign_type}."
        IS_FEATURE_ENABLED_API_INVALID_PARAMS = "({file}): [API_NAME] API got bad parameters. It expects campaign_key(String) as first and user_id(String) as second argument, custom_variables(dict) for pre-segmentation, variation_targeting_variables(dict) for white-listing and should_track_returning_user(bool) for tracking returning users can be passed via kwargs"
        GET_FEATURE_VARIABLE_VALUE_API_INVALID_PARAMS = "({file}): [API_NAME] API got bad parameters. It expects campaign_key(String) as first, variable_key(string) as second and user_id(String) as third argument, custom_variables(dict) for pre-segmentation and variation_targeting_variables(dict) for white-listing can be passed via kwargs"

        VARIABLE_NOT_FOUND = "({file}): [API_NAME] Variable {variable_key} not found for campaign {campaign_key} and type {campaign_type} for user ID {user_id}"
        UNABLE_TO_TYPE_CAST = (
            "({file}): [API_NAME] Unable to typecast value: {value} of type: {of_type} to type: {variable_type}."
        )

        USER_NOT_IN_CAMPAIGN = "({file}): [API_NAME] user_id:{user_id} did not become part of campaign_key:{campaign_key} and campaign type:{campaign_type}"
        API_NOT_WORKING = (
            "({file}): [API_NAME] API not working, exception caught: {exception}. Please contact VWO Support for help."
        )

        SEGMENTATION_ERROR = "({file}): [API_NAME] Error while segmenting the user_id:{user_id} of campaign_key:{campaign_key} with variables:{variables}{variation_status}. Error message: {error_message}"

        PUSH_API_INVALID_PARAMS = "({file}): [API_NAME] API got bad parameters. It expects tag_key(String) as first and tag_value(String) as second argument and user_id(String) as third argument"
        TAG_VALUE_LENGTH_EXCEEDED = "({file}): [API_NAME] The length of tag_value:{tag_value} and user_id: {user_id} can not be greater than 255"
        TAG_KEY_LENGTH_EXCEEDED = (
            "({file}): [API_NAME] The length of tag_key:{tag_key} and user_id: {user_id} can not be greater than 255"
        )
        NO_CAMPAIGN_FOUND = (
            "({file}): [API_NAME] No campaign found for goal_identifier:{goal_identifier}. Please verify from VWO app."
        )

        BULK_NOT_PROCESSED = (
            "({file}): Batch events couldn't be received by VWO. Calling Flush Callback with error and data."
        )

        BATCH_EVENT_LIMIT_EXCEEDED = "({file}): Impression event - {end_point} failed due to exceeding payload size. Parameter events_per_request in batch_events config in launch API has value:{events_per_request} for accountId:{account_id}. Please read the official documentation for knowing the size limits."
        INVALID_SETTINGS_FILE = (
            "({file}): [API_NAME] settings_file fetched is not proper for the account_id: {account_id}."
        )

        EVENT_BATCHING_NOT_OBJECT = "({file}): Batch event settings are not of type object"
        EVENT_BATCHING_INSUFFICIENT = (
            "({file}): Atleast one from events_per_request and request_time_interval must be provided"
        )
        EVENTS_PER_REQUEST_INVALID = "({file}): events_per_request should be an integer"
        REQUEST_TIME_INTERVAL_INVALID = "({file}): request_time_interval should be a number"
        EVENTS_PER_REQUEST_OUT_OF_BOUNDS = "({file}): events_per_request should be >= {min_value} and <= {max_value}"
        REQUEST_TIME_INTERVAL_OUT_OF_BOUNDS = "({file}): request_time_interval should be >= {min_value}"
        FLUSH_CALLBACK_INVALID = "({file}): flush_callback is not callable"
        INTEGRATIONS_SERVICE_CALLBACK_INVALID = "({file}): Integrations service callback is not callable"
        INTEGRATIONS_SERVICE_CALLBACK_EXECUTION_ERROR = (
            "({file}): Error while executing integrations service callback. Error message: {error_message}"
        )
