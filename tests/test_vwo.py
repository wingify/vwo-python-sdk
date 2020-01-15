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
import logging
import mock
import sys

import vwo
from .data.settings_files import SETTINGS_FILES
from .config import config
TEST_LOG_LEVEL = config.TEST_LOG_LEVEL


class VWOTest(unittest.TestCase):

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

    # Test initialization
    def test_vwo_init_with_invalid_settings_file(self):
        self.set_up('EMPTY_SETTINGS_FILE')
        self.assertIs(self.vwo.is_valid, False)

    def test_vwo_initialized_with_provided_log_level_DEBUG(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('AB_T_50_W_50_50')), log_level=vwo.LogLevels.DEBUG)
        self.assertEquals(vwo_instance.logger.logger.level, logging.DEBUG)

    def test_vwo_initialized_with_provided_log_level_WARNING(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('AB_T_50_W_50_50')), log_level=vwo.LogLevels.WARNING)
        self.assertEquals(vwo_instance.logger.logger.level, logging.WARNING)

    def test_vwo_initialized_with_provided_log_level_50(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('AB_T_50_W_50_50')), log_level=50)
        self.assertEquals(vwo_instance.logger.logger.level, 50)

    def test_vwo_initialized_with_no_logger_no_log_level(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('AB_T_50_W_50_50')))
        self.assertEquals(vwo_instance.logger.logger.level, 40)

    def test_vwo_initialized_with_logger_as_false(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('AB_T_50_W_50_50')), logger=False)
        self.assertEquals(vwo_instance.logger.logger.level, 40)

    def test_vwo_initialized_with_loglevel_as_false(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('AB_T_50_W_50_50')), log_level=False)
        self.assertEquals(vwo_instance.logger.logger.level, 40)

    def test_vwo_initialized_with_loglevel_as_anythoing_bad(self):
        vwo_instance = vwo.VWO(json.dumps(SETTINGS_FILES.get('AB_T_50_W_50_50')), log_level='{}')
        self.assertEquals(vwo_instance.logger.logger.level, 40)

    def test_vwo_initialized_with_custom_logger(self):
        class CustomLogger:
            def log(self, level, message):
                print(level, message)
        if sys.version_info[0] < 3:
            builtin_module_name = '__builtin__'
        else:
            builtin_module_name = 'builtins'
        with mock.patch(builtin_module_name + '.print') as mock_print:
            vwo.VWO(json.dumps(SETTINGS_FILES.get('AB_T_50_W_50_50')), logger=CustomLogger())
            mock_print.assert_called()
