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

import unittest
from vwo.services.url_manager import url_manager
from vwo.constants import constants


class UrlManagerTest(unittest.TestCase):
    def test_url_manager_get_base_url(self):
        url_manager.set_config()
        self.assertEquals(url_manager.get_base_url(), constants.ENDPOINTS.BASE_URL)

    def test_url_manager_get_base_url_with_prefix(self):
        collection_prefix = "eu"
        url_manager.set_config({"collection_prefix": collection_prefix})

        self.assertEquals(url_manager.get_base_url(), constants.ENDPOINTS.BASE_URL + "/" + collection_prefix)

        # reset the prefix
        url_manager.set_config()
