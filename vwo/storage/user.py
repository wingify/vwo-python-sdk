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


class UserStorage(object):
    """ UserStorage Class is used to store user-variation mapping.
    Override this class to implement your own functionality.
    SDK will ensure to use this while bucketing a user into a variation."""

    def get(self, user_id, campaign_key):
        """ To retrieve the stored variation for the user_id and
        campaign_key

        Args:
            user_id (str): User ID for which data needs to be retrieved.
            campaign_key (str): Campaign key to identify the campaign for
            which stored variation should be retrieved.

        Returns:
            user_data (dict): user-variation mapping
        """
        pass

    def set(self, user_data):
        """ To store the the user variation-mapping

        Args:
            user_data (dict): user-variation mapping
        """
        pass
