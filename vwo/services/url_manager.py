# Copyright 2019-2022 Wingify Software Pvt. Ltd.
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

from ..constants import constants
from ..helpers import validate_util


class UrlManager(object):
    """
  Construct and process URL as per requirements
  """

    def __init__(self):
        """
    Initializes UrlManager with settings
    """

        self.collection_prefix = None

    def set_config(self, config={}):
        """
    Set URL configuration

    Args:
      config (dict)
    """

        self.config = config
        self.collection_prefix = None

        collection_prefix_value = config.get("collection_prefix")
        if collection_prefix_value and validate_util.is_valid_string(collection_prefix_value):
            self.collection_prefix = collection_prefix_value

    def get_base_url(self):
        base_url = constants.ENDPOINTS.BASE_URL

        if self.collection_prefix is not None:
            return base_url + "/" + self.collection_prefix

        return base_url


url_manager = UrlManager()
