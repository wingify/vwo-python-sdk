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


class FileNameEnum:
    """ Classobj encapsulating locations various files of the SDK """

    class Vwo:
        VWO_PATH = "vwo/"
        VWO = VWO_PATH + "vwo"

    class Api:
        API_PATH = "vwo/api/"
        Activate = API_PATH + "activate"
        GetVariationName = API_PATH + "get_variation_name"
        Track = API_PATH + "track"
        IsFeatureEnabled = API_PATH + "is_feature_enabled"
        GetFeatureVariableValue = API_PATH + "get_feature_variable_value"
        Push = API_PATH + "push"
        Launch = API_PATH + "launch"
        FlushEvents = API_PATH + "flush_events"
        GetAndUpdateSettingsFile = API_PATH + "get_and_update_settings_file"

    class Core:
        CORE_PATH = "vwo/core/"
        Bucketer = CORE_PATH + "bucketer"
        VariationDecider = CORE_PATH + "variation_decider"

    class Event:
        EVENT_PATH = "vwo/event/"
        EventDispatcher = EVENT_PATH + "event_dispatcher"

    class Helpers:
        HELPERS_PATH = "vwo/helpers/"
        CampaignUtil = HELPERS_PATH + "campaign_util"
        CustomDimensionsUtil = HELPERS_PATH + "custom_dimensions_util"
        FeatureUtil = HELPERS_PATH + "feature_util"
        GenericUtil = HELPERS_PATH + "generic_util"
        ImpressionUtil = HELPERS_PATH + "impression_util"
        UuidUtil = HELPERS_PATH + "uuid_util"
        ValidateUtil = HELPERS_PATH + "validate_util"

    class Logger:
        LOGGER_PATH = "vwo/logger/"
        LoggerManager = LOGGER_PATH + "logger_manager"

    class Services:
        SERVICES_PATH = "vwo/services/"
        SettingsFileManager = SERVICES_PATH + "settings_file_manager"
        SegmentEvaluator = SERVICES_PATH + "segment_evaluator"
        HooksManager = SERVICES_PATH + "hooks_manager"
