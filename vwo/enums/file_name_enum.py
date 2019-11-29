# Copyright 2019 Wingify Software Pvt. Ltd.
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

    VWO_PATH = 'vwo/'
    HELPERS_PATH = 'vwo/helpers/'
    SERVICES_PATH = 'vwo/services/'
    CORE_PATH = 'vwo/core/'
    EVENT_PATH = 'vwo/event/'
    LOGGER_PATH = 'logger/'

    VWO = VWO_PATH + 'vwo'

    CampaignUtil = HELPERS_PATH + 'campaign_util'
    Functionutil = HELPERS_PATH + 'generic_util'
    UuidUtil = HELPERS_PATH + 'uuid_util'
    ValidateUtil = HELPERS_PATH + 'validate_util'
    FeatureUtil = HELPERS_PATH + 'feature_util'
    CustomDimensionsUtil = HELPERS_PATH + 'custom_dimensions_util'

    SettingsFileManager = SERVICES_PATH + 'settings_file_manager'
    SegmentEvaluator = SERVICES_PATH + 'segment_evaluator'

    Bucketer = CORE_PATH + 'bucketer'
    VariationDecider = CORE_PATH + 'variation_decider'

    ImpressionUtil = EVENT_PATH + 'impression_util'
    EventDispatcher = EVENT_PATH + 'event_dispatcher'

    LoggerManager = LOGGER_PATH + 'logger_manager'
