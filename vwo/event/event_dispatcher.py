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

import threading
from ..http.connection import Connection
from ..services.usage_stats_manager import UsageStats
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..logger import VWOLogger
from ..constants import constants

FILE = FileNameEnum.Event.EventDispatcher


class EventDispatcher(object):
    """Class having request making/event dispatching capabilities to our servers"""

    def __init__(self, is_development_mode=False, batch_event_settings=None, sdk_key=None):
        """Initialize the dispatcher with logger

        Args:
            is_development_mode: To specify whether the request
            to our server should be made or not.
        """
        self.logger = VWOLogger.getInstance()
        self.is_development_mode = is_development_mode
        self.connection = Connection()

        self.sdk_key = sdk_key
        self.sdk_v = constants.SDK_VERSION
        self.sdk = constants.SDK_NAME
        self.account_id = None
        self.queue = None
        self.queue_metadata = {}
        self.timer = None

        self.event_batching = False
        self.events_per_request = constants.BATCH_EVENTS.DEFAULT_EVENTS_PER_REQUEST
        self.request_time_interval = constants.BATCH_EVENTS.DEFAULT_REQUEST_TIME_INTERVAL
        self.flush_callback = None

        if batch_event_settings:
            self.event_batching = True
            self.queue = []

            if batch_event_settings.get(constants.BATCH_EVENTS.EVENTS_PER_REQUEST):
                self.events_per_request = batch_event_settings.get(constants.BATCH_EVENTS.EVENTS_PER_REQUEST)

            if batch_event_settings.get(constants.BATCH_EVENTS.REQUEST_TIME_INTERVAL):
                self.request_time_interval = batch_event_settings.get(constants.BATCH_EVENTS.REQUEST_TIME_INTERVAL)

            if batch_event_settings.get(constants.BATCH_EVENTS.FLUSH_CALLBACK):
                self.flush_callback = batch_event_settings.get(constants.BATCH_EVENTS.FLUSH_CALLBACK)

    def dispatch_events(self, params, impression):
        """This method checks for development mode, if it is False then it sends the impression
        to our servers at events endpoint, else return True without sending the impression.

        Args:
            params (dict): Dictionaty objet containing query params for the call
            impression (dict): Dictionary object containing the information of the impression

        Returns:
            bool: True if impression is successfully received by our servers, else false
        """
        url = constants.HTTPS_PROTOCOL + constants.ENDPOINTS.BASE_URL + constants.ENDPOINTS.EVENTS
        headers = {"User-Agent": constants.SDK_NAME}

        if self.is_development_mode:
            result = True
        else:
            resp = self.connection.post(url, params=params, data=impression, headers=headers)
            result = resp.get("status_code") == 200

        if result is True:
            self.logger.log(
                LogLevelEnum.INFO,
                LogMessageEnum.INFO_MESSAGES.IMPRESSION_SUCCESS_FOR_EVENT_ARCH.format(
                    file=FILE, event=params.get("en"), account_id=params.get("a")
                ),
            )
        else:
            self.logger.log(
                LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.IMPRESSION_FAILED.format(file=FILE, end_point=url)
            )

        return result

    def dispatch(self, impression):
        """This method checks for development mode, if it is False then it sends the impression
        to our servers using a vwo.http.connection.Connection object, else return True without
        sending the impression.

        Args:
            impression (dict): Dictionary object containing the information of the impression

        Returns:
            bool: True if impression is successfully received by our servers, else false
        """
        url = impression.pop("url")
        if self.is_development_mode:
            result = True
        else:
            result = False
            if self.event_batching is False:
                # sync API call
                resp = self.connection.get(url, params=impression)
                result = resp.get("status_code") == 200
            else:
                result = self.async_dispatch(url, impression)

        if result is True:
            if self.event_batching is True:
                self.logger.log(
                    LogLevelEnum.INFO,
                    LogMessageEnum.INFO_MESSAGES.IMPRESSION_SUCCESS_QUEUE.format(
                        file=FILE, end_point=url, queue_length=len(self.queue), queue_metadata=self.queue_metadata
                    ),
                )
            else:
                self.logger.log(
                    LogLevelEnum.INFO, LogMessageEnum.INFO_MESSAGES.IMPRESSION_SUCCESS.format(file=FILE, end_point=url)
                )
            return True
        else:
            if self.event_batching is True:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.IMPRESSION_FAILED_QUEUE.format(file=FILE, end_point=url),
                )
            else:
                self.logger.log(
                    LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.IMPRESSION_FAILED.format(file=FILE, end_point=url)
                )
            return False

    def async_dispatch(self, url, impression):
        """
        This method pushes impression in queue after modifying the payload

        Args:
            url (string): VWO's url for syncing an impression
            impression (dict): Dictionary object containing the information of the impression
        Returns:
            bool: True if impression is successfully pushed in queue, else false
        """
        try:
            # build payload
            payload = self.build_event_payload(url, impression)
            # push in queue
            self.queue.append(payload)
            self.update_queue_metadata(url=url)
            # flush queue periodically
            if len(self.queue) == 1:
                self.timer = threading.Timer(self.request_time_interval, self.flush_queue)
                self.timer.start()
            # flush queue when full
            if len(self.queue) >= self.events_per_request:
                self.flush_queue()
            return True
        except Exception:
            self.logger.log(
                LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.IMPRESSION_FAILED.format(file=FILE, end_point=url)
            )
            return False

    def build_event_payload(self, url, impression):
        """
        This method builds payload from url and impression.
        It can then be used in bulk api for an event

        Args:
            url (string): VWO's url for syncing an impression
            impression (dict): Dictionary object containing the information of the impression
        Returns:
            payload (dict): Dictionary object containing the information computed from url and impression
        """
        if self.account_id is None:
            self.account_id = impression.get("account_id")

        url_split = url.split("/")
        event_name = url_split[-1]

        payload = {"u": impression.get("u"), "sId": impression.get("sId")}

        if event_name == constants.EVENTS.TRACK_USER:
            payload.update({"c": impression.get("combination"), "e": impression.get("experiment_id"), "eT": 1})
        elif event_name == constants.EVENTS.TRACK_GOAL:
            payload.update(
                {
                    "c": impression.get("combination"),
                    "e": impression.get("experiment_id"),
                    "g": impression.get("goal_id"),
                    "eT": 2,
                }
            )
            if impression.get("r") is not None:
                payload.update(r=impression.get("r"))
        elif event_name == constants.EVENTS.PUSH:
            payload.update({"t": impression.get("tags"), "eT": 3})

        return payload

    def spawn_thread_to_sync(self, events):
        """
        Spawns a thread to sync events to VWO servers

        Args:
            events (list): List of events to be synced to VWO servers
        """
        sync_thread = threading.Thread(target=self.sync_with_vwo, args=(events,))
        sync_thread.start()

    def sync_with_vwo(self, events):
        url = constants.HTTPS_PROTOCOL + constants.ENDPOINTS.BASE_URL
        url = url + constants.ENDPOINTS.BATCH_EVENTS
        queue_length = len(events)
        try:
            query_params = {"a": self.account_id, "sdk": self.sdk, "sdk-v": self.sdk_v, "env": self.sdk_key}
            post_data = {"ev": events}
            query_params.update(UsageStats.get_usage_stats())
            headers = {"Authorization": self.sdk_key}
            resp = self.connection.post(url, params=query_params, data=post_data, headers=headers)
            status_code = resp.get("status_code")

            if status_code == 200:
                self.logger.log(
                    LogLevelEnum.INFO,
                    LogMessageEnum.INFO_MESSAGES.IMPRESSION_SUCCESS.format(
                        file=FILE, end_point=url, account_id=self.account_id
                    ),
                )
            elif status_code == 413:
                self.logger.log(
                    LogLevelEnum.ERROR,
                    LogMessageEnum.ERROR_MESSAGES.BATCH_EVENT_LIMIT_EXCEEDED.format(
                        file=FILE, end_point=url, events_per_request=queue_length, account_id=self.account_id
                    ),
                )
            else:
                self.logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.BULK_NOT_PROCESSED.format(file=FILE))
            if self.flush_callback:
                self.flush_callback(None, events)
        except Exception as err:
            self.logger.log(LogLevelEnum.ERROR, LogMessageEnum.ERROR_MESSAGES.BULK_NOT_PROCESSED.format(file=FILE))
            if self.flush_callback:
                self.flush_callback(err, events)

    def flush_queue(self, manual=False, mode="async"):
        """
        Flush_queue

        Args:
            manual(bool): Informs if the function was triggered manually by user or not
            mode(string): In sync mode, function makes a synchronous call before exiting
                In async mode, function spawns a thread to sync to VWO and exits
        """
        if self.event_batching is False:
            return

        events = self.queue
        no_of_events = len(events)
        queue_metadata = self.queue_metadata

        if no_of_events < 1:
            return

        self.logger.log(
            LogLevelEnum.DEBUG,
            LogMessageEnum.DEBUG_MESSAGES.BEFORE_FLUSHING.format(
                file=FILE,
                manually="manually" if manual else "",
                length=no_of_events,
                timer="Timer will be cleared and registered again" if manual else "",
                queue_metadata=queue_metadata,
            ),
        )

        # stop timer
        if self.timer:
            self.timer.cancel()

        # flush queue
        self.queue = []
        self.queue_metadata = {}

        self.logger.log(
            LogLevelEnum.INFO,
            LogMessageEnum.INFO_MESSAGES.AFTER_FLUSHING.format(
                file=FILE, length=no_of_events, manually="manually" if manual else "", queue_metadata=queue_metadata
            ),
        )

        if mode == "async":
            self.spawn_thread_to_sync(events=events)
        else:
            self.sync_with_vwo(events=events)

    def update_queue_metadata(self, url):
        url_split = url.split("/")
        event_name = url_split[-1]
        if self.queue_metadata.get(event_name) is None:
            self.queue_metadata[event_name] = 0
        self.queue_metadata[event_name] += 1
