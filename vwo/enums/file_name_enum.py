class FileNameEnum:
    """ Classobj encapsulating locations various files of the SDK """

    VWO_PATH = 'vwo/'
    UTILS_PATH = 'vwo/utils/'
    SERVICES_PATH = 'vwo/services/'
    CORE_PATH = 'vwo/core/'
    EVENT_PATH = 'vwo/event/'
    LOGGER_PATH = 'logger/'

    VWO = VWO_PATH + 'vwo'

    CampaignUtil = UTILS_PATH + 'campaign_util'
    Functionutil = UTILS_PATH + 'function_util'
    UuidUtil = UTILS_PATH + 'uuid_util'
    ValidateUtil = UTILS_PATH + 'validate_util'
    FeatureUtil = UTILS_PATH + 'feature_util'

    SettingsFileManager = SERVICES_PATH + 'settings_file_manager'

    Bucketer = CORE_PATH + 'bucketer'
    VariationDecider = CORE_PATH + 'variation_decider'

    ImpressionUtil = EVENT_PATH + 'impression_util'
    EventDispatcher = EVENT_PATH + 'event_dispatcher'

    LoggerManager = LOGGER_PATH + 'logger_manager'
