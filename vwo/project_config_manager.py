import json
from .helpers.enums import LogMessageEnum, FileNameEnum, LogLevelEnum
from .helpers import campaign_util
from .logger import Logger


class ProjectConfigManager(object):
    """ Representation of the VWO settings file. """

    def __init__(self, settings_file):
        """ ProjectConfigManager init method to load and set project config data.

        Args:
            settings_file (dict): Dict object
                representing the project settings_file.
        """
        self.settings_file = json.loads(settings_file)
        self.logger = Logger()

    # PUBLIC METHODS

    def process_settings_file(self):
        """ Processes the settings_file, assigns variation allocation range """

        settings_file = self.settings_file
        for campaign in settings_file.get('campaigns'):
            campaign_util.set_variation_allocation(campaign)
        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.SETTINGS_FILE_PROCESSED.format(
                file=FileNameEnum.ProjectConfigManager
            )
        )

    def get_settings_file(self):
        """ Retrieves settings file """

        return self.settings_file
