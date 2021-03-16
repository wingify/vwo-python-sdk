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

from __future__ import print_function
import unittest
import json
import mock

import vwo
from vwo.constants import constants
from vwo.helpers import uuid_util
from vwo.services import hooks_manager
from vwo.services.hooks_manager import HooksManager

from ..data.settings_files import SETTINGS_FILES
from ..config.config import TEST_LOG_LEVEL

TEST_LOG_LEVEL = TEST_LOG_LEVEL

class ClientUserStorage:
  def __init__(self):
    self.storage = {}

  def get(self, user_id, campaign_key):
    return self.storage.get((user_id, campaign_key))

  def set(self, user_data):
    self.storage[(user_data.get("userId"), user_data.get("campaignKey"))] = user_data

class Integrations:
  def __init__(self):
    pass
  
  def callback(self, properties):
    pass

class IntegrationsWithException:
  def __init__(self):
    pass
  
  def callback(self, properties):
    raise Exception("Some Error Occured")

class IntegrationsWithCallbackNotCallable:
  def __init__(self):
    pass
  
  @property
  def callback(self):
    pass

class HooksManagerTest(unittest.TestCase):

  def test_hooks_manager_catch_exceptions(self):
    integrations = IntegrationsWithException()
    hooks_manager = HooksManager(intgerations=integrations)
    with mock.patch("vwo.logger.VWOLogger.VWOLogger.log") as mocked_logger:
      hooks_manager.execute({})
      mocked_logger.assert_called_once()

  def test_hooks_manager_callback_not_callable(self):
    integrations = IntegrationsWithCallbackNotCallable()
    hooks_manager = HooksManager(intgerations=integrations)
    with mock.patch("vwo.logger.VWOLogger.VWOLogger.log") as mocked_logger:
      hooks_manager.execute({})
      mocked_logger.assert_called_once()

  def test_hooks_manager_ab_test(self):
    properties = {
      'campaign_id': 231,
      'campaign_key': "AB_T_100_W_50_50",
      'campaign_type': "VISUAL_AB",
      'custom_variables': None,
      'event': "CAMPAIGN_DECISION",
      'goal_identifier': None,
      'is_forced_variation_enabled': None,
      'sdk_version': constants.SDK_VERSION,
      'source': "activate",
      'user_id': "user",
      'variation_targeting_variables': None,
      'vwo_user_id': uuid_util.generate_for("user", "88888888"),
      'from_user_storage_service': False,
      'is_user_whitelisted': False,
      'variation_id': 2,
      'variation_name': 'Variation-1',
    }

    with mock.patch("vwo.services.hooks_manager.HooksManager.execute") as mocked_hooks_manager_execute:
      vwo_instance = vwo.launch(
        json.dumps(SETTINGS_FILES.get("AB_T_100_W_50_50")),
        is_development_mode=True,
        log_level=40,
        should_track_returning_user=False,
        integrations=Integrations()
      )

      vwo_instance.activate("AB_T_100_W_50_50", "user")
      mocked_hooks_manager_execute.assert_called_once_with(properties)

  def test_hooks_manager_feature_test(self):
    properties = {
      'campaign_id': 22,
      'campaign_key': "FT_T_100_W_10_20_30_40",
      'campaign_type': "FEATURE_TEST",
      'custom_variables': None,
      'event': "CAMPAIGN_DECISION",
      'goal_identifier': None,
      'is_forced_variation_enabled': None,
      'sdk_version': constants.SDK_VERSION,
      'source': "is_feature_enabled",
      'user_id': "user",
      'variation_targeting_variables': None,
      'vwo_user_id': uuid_util.generate_for("user", "123456"),
      'from_user_storage_service': False,
      'is_user_whitelisted': False,
      'is_feature_enabled': True,
      'variation_id': '4',
      'variation_name': 'Variation-3',
    }

    with mock.patch("vwo.services.hooks_manager.HooksManager.execute") as mocked_hooks_manager_execute:
      vwo_instance = vwo.launch(
        json.dumps(SETTINGS_FILES.get("FT_T_100_W_10_20_30_40")),
        is_development_mode=True,
        log_level=40,
        should_track_returning_user=False,
        integrations=Integrations()
      )

      vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user")
      mocked_hooks_manager_execute.assert_called_once_with(properties)

  def test_hooks_manager_feature_rollout(self):
    properties = {
      'campaign_id': 29,
      'campaign_key': "FR_T_100_W_100",
      'campaign_type': "FEATURE_ROLLOUT",
      'custom_variables': None,
      'event': "CAMPAIGN_DECISION",
      'goal_identifier': None,
      'is_forced_variation_enabled': None,
      'sdk_version': constants.SDK_VERSION,
      'source': "is_feature_enabled",
      'user_id': "user",
      'variation_targeting_variables': None,
      'vwo_user_id': uuid_util.generate_for("user", "123456"),
      'from_user_storage_service': False,
      'is_user_whitelisted': False,
      'is_feature_enabled': True,
    }

    with mock.patch("vwo.services.hooks_manager.HooksManager.execute") as mocked_hooks_manager_execute:
      vwo_instance = vwo.launch(
        json.dumps(SETTINGS_FILES.get("FR_T_100_W_100")),
        is_development_mode=True,
        log_level=40,
        should_track_returning_user=False,
        integrations=Integrations()
      )

      vwo_instance.is_feature_enabled("FR_T_100_W_100", "user")
      mocked_hooks_manager_execute.assert_called_once_with(properties)

  def test_hooks_manager_feature_rollout_user_storage_provided(self):
    properties = {
      'campaign_id': 29,
      'campaign_key': "FR_T_100_W_100",
      'campaign_type': "FEATURE_ROLLOUT",
      'custom_variables': None,
      'event': "CAMPAIGN_DECISION",
      'goal_identifier': None,
      'is_forced_variation_enabled': None,
      'sdk_version': constants.SDK_VERSION,
      'source': "is_feature_enabled",
      'user_id': "user",
      'variation_targeting_variables': None,
      'vwo_user_id': uuid_util.generate_for("user", "123456"),
      'from_user_storage_service': True,
      'is_user_whitelisted': False,
      'is_feature_enabled': True,
    }

    vwo_instance = vwo.launch(
      json.dumps(SETTINGS_FILES.get("FR_T_100_W_100")),
      is_development_mode=True,
      log_level=40,
      should_track_returning_user=False,
      user_storage=ClientUserStorage(),
      integrations=Integrations()
    )
    vwo_instance.is_feature_enabled("FR_T_100_W_100", "user")

    with mock.patch("vwo.services.hooks_manager.HooksManager.execute") as mocked_hooks_manager_execute:
      vwo_instance.is_feature_enabled("FR_T_100_W_100", "user")
      mocked_hooks_manager_execute.assert_called_once_with(properties)

  def test_hooks_manager_track_goal(self):
    custom_variables = {"a": 987.1234, "hello": "world"}
    properties = {
      'campaign_id': 174,
      'campaign_key': "T_100_W_50_50_WS",
      'campaign_type': "VISUAL_AB",
      'custom_variables': custom_variables,
      'event': "CAMPAIGN_DECISION",
      'goal_identifier': "ddd",
      'is_forced_variation_enabled': None,
      'sdk_version': constants.SDK_VERSION,
      'source': "track",
      'user_id': "user",
      'variation_targeting_variables': None,
      'vwo_user_id': uuid_util.generate_for("user", "88888888"),
      'from_user_storage_service': False,
      'is_user_whitelisted': False,
      'variation_id': 2,
      'variation_name': 'Variation-1',
    }

    with mock.patch("vwo.services.hooks_manager.HooksManager.execute") as mocked_hooks_manager_execute:
      vwo_instance = vwo.launch(
        json.dumps(SETTINGS_FILES.get("T_100_W_50_50_WS")),
        is_development_mode=True,
        log_level=40,
        should_track_returning_user=False,
        integrations=Integrations()
      )

      vwo_instance.track("T_100_W_50_50_WS", "user", goal_identifier="ddd",custom_variables=custom_variables)
      mocked_hooks_manager_execute.assert_called_once_with(properties)

  def test_hooks_manager_user_storage_provided(self):
    properties = {
      'campaign_id': 22,
      'campaign_key': "FT_T_100_W_10_20_30_40",
      'campaign_type': "FEATURE_TEST",
      'custom_variables': None,
      'event': "CAMPAIGN_DECISION",
      'goal_identifier': None,
      'is_forced_variation_enabled': None,
      'sdk_version': constants.SDK_VERSION,
      'source': "is_feature_enabled",
      'user_id': "user",
      'variation_targeting_variables': None,
      'vwo_user_id': uuid_util.generate_for("user", "123456"),
      'from_user_storage_service': True,
      'is_user_whitelisted': False,
      'is_feature_enabled': True,
      'variation_id': '4',
      'variation_name': 'Variation-3',
    }

    vwo_instance = vwo.launch(
        json.dumps(SETTINGS_FILES.get("FT_T_100_W_10_20_30_40")),
        is_development_mode=True,
        log_level=40,
        should_track_returning_user=False,
        user_storage=ClientUserStorage(),
        integrations=Integrations()
      )

    vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user")
    with mock.patch("vwo.services.hooks_manager.HooksManager.execute") as mocked_hooks_manager_execute:
      vwo_instance.is_feature_enabled("FT_T_100_W_10_20_30_40", "user")
      mocked_hooks_manager_execute.assert_called_once_with(properties)

  def test_hooks_manager_whitelisting_enabled(self):
    variation_targeting_variables = {"chrome": "false", "safari": "true", "browser": "chrome 107.107"}
    properties = {
      'campaign_id': 235,
      'campaign_key': "FT_100_W_33_33_33_WS_WW",
      'campaign_type': "FEATURE_TEST",
      'custom_variables': None,
      'event': "CAMPAIGN_DECISION",
      'goal_identifier': None,
      'is_forced_variation_enabled': True,
      'sdk_version': constants.SDK_VERSION,
      'source': "is_feature_enabled",
      'user_id': "Sarah",
      'variation_targeting_variables': variation_targeting_variables,
      'vwo_user_id': uuid_util.generate_for("Sarah", "88888888"),
      'from_user_storage_service': False,
      'is_user_whitelisted': True,
      'is_feature_enabled': False,
      'variation_id': 1,
      'variation_name': 'Control',
    }

    with mock.patch("vwo.services.hooks_manager.HooksManager.execute") as mocked_hooks_manager_execute:
      vwo_instance = vwo.launch(
        json.dumps(SETTINGS_FILES.get("FT_100_W_33_33_33_WS_WW")),
        is_development_mode=True,
        log_level=40,
        should_track_returning_user=False,
        integrations=Integrations()
      )

      vwo_instance.is_feature_enabled("FT_100_W_33_33_33_WS_WW", "Sarah", variation_targeting_variables=variation_targeting_variables)
      mocked_hooks_manager_execute.assert_called_once_with(properties)

  def test_hooks_manager_custom_variables_provided(self):
    custom_variables = {"a": 987.1234, "hello": "world"}
    properties = {
      'campaign_id': 174,
      'campaign_key': "T_100_W_50_50_WS",
      'campaign_type': "VISUAL_AB",
      'custom_variables': custom_variables,
      'event': "CAMPAIGN_DECISION",
      'goal_identifier': None,
      'is_forced_variation_enabled': None,
      'sdk_version': constants.SDK_VERSION,
      'source': "activate",
      'user_id': "user",
      'variation_targeting_variables': None,
      'vwo_user_id': uuid_util.generate_for("user", "88888888"),
      'from_user_storage_service': False,
      'is_user_whitelisted': False,
      'variation_id': 2,
      'variation_name': 'Variation-1',
    }

    with mock.patch("vwo.services.hooks_manager.HooksManager.execute") as mocked_hooks_manager_execute:
      vwo_instance = vwo.launch(
        json.dumps(SETTINGS_FILES.get("T_100_W_50_50_WS")),
        is_development_mode=True,
        log_level=40,
        should_track_returning_user=False,
        integrations=Integrations()
      )

      vwo_instance.activate("T_100_W_50_50_WS", "user", custom_variables=custom_variables)
      mocked_hooks_manager_execute.assert_called_once_with(properties)
