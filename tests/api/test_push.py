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

from __future__ import print_function
import unittest
import json
import random
import mock

import vwo
from ..data.settings_files import SETTINGS_FILES

from ..config.config import TEST_LOG_LEVEL


class PushTest(unittest.TestCase):

    def set_up(self, config_variant='AB_T_50_W_50_50'):
        self.user_id = str(random.random())
        self.settings_file = \
            json.dumps(SETTINGS_FILES.get(config_variant))

        self.vwo = vwo.VWO(self.settings_file,
                           is_development_mode=True,
                           log_level=TEST_LOG_LEVEL)
        self.campaign_key = config_variant
        try:
            self.goal_identifier = \
                SETTINGS_FILES[config_variant]['campaigns'][0]['goals'][0]['identifier']
        except Exception:
            pass

    def test_push_raises_exception(self):
        with mock.patch('vwo.helpers.validate_util.is_valid_string', side_effect=Exception('Test')):
            self.set_up()
            self.assertIs(False, self.vwo.push('SOME_CAMPAIGN',
                                               'VARIABLE_KEY',
                                               'USER_ID'))

    def test_push_corrupted_settings_file(self):
        vwo_instace = vwo.VWO({}, log_level=TEST_LOG_LEVEL)
        self.assertIs(False, vwo_instace.push("1234", '12435t4', '12343'))

    def test_push_true(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('DUMMY_SETTINGS_FILE')), log_level=50,
                               is_development_mode=True)
        self.assertIs(True, vwo_instance.push('browser', 'chrome', '12345'))

    def test_push_int_value_false(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('DUMMY_SETTINGS_FILE')), log_level=50,
                               is_development_mode=True)
        self.assertIs(False, vwo_instance.push('browser', 1, '12345'))

    def test_push_longer_than_255_value_false(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('DUMMY_SETTINGS_FILE')), log_level=50,
                               is_development_mode=True)
        self.assertIs(False, vwo_instance.push('browser', 'a' * 256, '12345'))

    def test_push_exact_255_value_true(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('DUMMY_SETTINGS_FILE')), log_level=50,
                               is_development_mode=True)
        self.assertIs(True, vwo_instance.push('browser', 'a' * 255, '12345'))

    def test_push_longer_than_255_key_false(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('DUMMY_SETTINGS_FILE')), log_level=50,
                               is_development_mode=True)
        self.assertIs(False, vwo_instance.push('a' * 256, 'browser', '12345'))

    def test_push_exact_255_key_true(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('DUMMY_SETTINGS_FILE')), log_level=50,
                               is_development_mode=True)
        self.assertIs(True, vwo_instance.push('a' * 255, 'browser', '12345'))
