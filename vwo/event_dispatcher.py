""" Module for dispatching events to the server """

import requests
from .helpers.enums import LogMessageEnum, FileNameEnum, LogLevelEnum
from .logger import Logger

EXCLUDE_KEYS = ['url']


class EventDispatcher(object):
    """ Class having event dispatching capabilities,
        uses requests internally
    """

    def __init__(self, is_development_mode=False):
        """ Initialize the dispatcher with logger

        Args:
            is_development_mode: To specify whether the request
            to our server should be made or not.
        """
        self.logger = Logger()
        self.is_development_mode = is_development_mode

    def dispatch(self, properties):
        """ Dispatch the event being represented in the properties object.

        Args:
            properties (dict): Object holding information about
            he request to be dispatched to the VWO backend.

        Returns:
            bool: True for success, false for failure
        """
        if self.is_development_mode:
            return True

        modified_properties = {
            key: properties[key] for key in properties if key not in EXCLUDE_KEYS  # noqa:E501
        }
        try:
            resp = requests.get(properties.get('url'),
                                params=modified_properties
                                )
            if resp.status_code == 200:
                self.logger.log(
                    LogLevelEnum.INFO,
                    LogMessageEnum.INFO_MESSAGES.IMPRESSION_SUCCESS.format(
                        file=FileNameEnum.EventDispatcher,
                        end_point=properties.get('url'),
                        campaign_id=properties.get('experiment_id'),
                        user_id=properties.get('uId'),
                        account_id=properties.get('account_id'),
                        variation_id=properties.get('combination')
                    )
                )
                return True
            else:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.IMPRESSION_FAILED.format(
                        file=FileNameEnum.EventDispatcher,
                        end_point=properties.get('url')
                    )
                )
        except Exception:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.IMPRESSION_FAILED.format(
                    file=FileNameEnum.EventDispatcher,
                    end_point=resp.url
                )
            )
        return False
