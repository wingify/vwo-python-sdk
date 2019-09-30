from ..http.connection import Connection
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..logger.logger_manager import VWOLogger


class EventDispatcher(object):
    """ Class having request making/event dispatching capabilities to our servers"""

    def __init__(self, is_development_mode=False):
        """ Initialize the dispatcher with logger

        Args:
            is_development_mode: To specify whether the request
            to our server should be made or not.
        """
        self.logger = VWOLogger.getInstance()
        self.is_development_mode = is_development_mode
        self.connection = Connection()
        self.EXCLUDE_KEYS = ['url']

    def dispatch(self, impression):
        """ Dispatch the event represented by the impression object.

        Args:
            event (dict): Object holding information about
            he request to be dispatched to the VWO backend.

        Returns:
            bool: True for success, false for failure
        """
        if self.is_development_mode:
            return True

        modified_event = {
            key: impression[key] for key in impression if key not in self.EXCLUDE_KEYS
        }
        resp = self.connection.get(impression.get('url'),
                                   params=modified_event
                                   )
        if resp.get('status_code') == 200:
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.IMPRESSION_SUCCESS.format(
                    file=FileNameEnum.EventDispatcher,
                    end_point=impression.get('url'),
                    campaign_id=impression.get('experiment_id'),
                    user_id=impression.get('uId'),
                    account_id=impression.get('account_id'),
                    variation_id=impression.get('combination')
                )
            )
            return True
        else:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.IMPRESSION_FAILED.format(
                    file=FileNameEnum.EventDispatcher,
                    end_point=impression.get('url')
                )
            )
            return False
