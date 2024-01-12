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

from vwo.storage.user import UserStorage
import redis
import json


class RedisUserStorage(UserStorage):
    """
    Redis User Storage overrides UserStorage to provide storage in Redis
    """

    def __init__(self, url, user_id, password):
        self.url = url
        self.user_id = user_id
        self.password = password

        try:
            # instantiate redis
            self.redis = redis.Redis(host=url, port=6379, db=0)
        except Exception as e:
            print(e)

    def get(self, user_id, campaign_key):
        """To retrieve the stored variation for the user_id and
        campaign_key

        Args:
            user_id (str): User ID for which data needs to be retrieved.
            campaign_key (str): Campaign key to identify the campaign for
            which stored variation should be retrieved.

        Returns:
            user_data (dict): user-variation mapping
        """
        value = None

        # create the key for this and then get the value from redis
        key = campaign_key + ":" + user_id

        try:
            # get from redis
            value_str = self.redis.get(key)
        except Exception as e:
            print(e)

        # extract the map from the string value stored in redis
        if value_str:
            value = json.loads(value_str)

        return value

    def set(self, user_data):
        """To store the the user variation-mapping

        Args:
            user_data (dict): user-variation mapping
        """
        try:
            # create the key and value for this and set to redis
            key = str(user_data["campaignKey"]) + ":" + str(user_data["userId"])
            value = json.dumps(user_data)

            # set to redis
            self.redis.set(key, value)
        except Exception as e:
            print(e)
