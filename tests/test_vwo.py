import unittest
import json
import random
import logging

import vwo
from .data.settings_files import SETTINGS_FILES
from .data.settings_file_and_user_expectations import USER_EXPECTATIONS
from vwo.services import singleton
from vwo.helpers import validate_util


class VWOTest(unittest.TestCase):

    def set_up(self, config_variant='AB_T_50_W_50_50'):
        self.user_id = str(random.random())
        self.settings_file = \
            json.dumps(SETTINGS_FILES.get(config_variant))

        self.vwo = vwo.VWO(self.settings_file,
                           is_development_mode=True,
                           log_level=0)
        self.campaign_key = config_variant
        try:
            self.goal_identifier = \
                SETTINGS_FILES[config_variant]['campaigns'][0]['goals'][0]['identifier']
        except Exception:
            pass

    def tearDown(self):
        singleton.forgetAllSingletons()

    # Test initialization
    def test_init_vwo_with_invalid_settings_file(self):
        self.set_up('EMPTY_SETTINGS_FILE')
        self.assertIs(self.vwo.is_valid, False)

    # Test get_variation_name
    def test_get_variation_name_invalid_params(self):
        self.set_up()
        self.assertIsNone(self.vwo.get_variation_name(123, 456))

    def test_get_variation_name_invalid_config(self):
        self.set_up('EMPTY_SETTINGS_FILE')
        self.assertIsNone(self.vwo.get_variation_name(self.user_id, 'some_campaign'))

    def test_get_variation_name_with_no_campaign_key_found(self):
        self.set_up('AB_T_50_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.get_variation_name('NO_SUCH_CAMPAIGN_KEY',
                          test['user']), None)

    def test_get_variation_name_wrong_campaign_type_passed(self):
        self.set_up('FR_T_0_W_100')
        result = self.vwo.get_variation_name('FR_T_0_W_100', 'user')
        self.assertIs(result, None)

    def test_get_variation_name_against_campaign_traffic_50_and_split_50_50(self):
        self.set_up('AB_T_50_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation_name(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_name_against_campaign_traffic_100_and_split_50_50(self):
        self.set_up('AB_T_100_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation_name(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_name_against_campaign_traffic_100_and_split_20_80(self):
        self.set_up('AB_T_100_W_20_80')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation_name(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_name_against_campaign_traffic_20_and_split_10_90(self):
        self.set_up('AB_T_20_W_10_90')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation_name(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_name_against_campaign_traffic_100_and_split_0_100(self):
        self.set_up('AB_T_100_W_0_100')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation_name(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_name_against_campaign_traffic_100_and_split_33_x3(self):
        self.set_up('AB_T_100_W_33_33_33')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation_name(self.campaign_key,
                             test['user']), test['variation'])

    # Test activate
    def test_activate_invalid_params(self):
        self.set_up()
        self.assertIsNone(self.vwo.activate(123, 456))

    def test_activate_invalid_config(self):
        self.set_up('EMPTY_SETTINGS_FILE')
        self.assertIsNone(self.vwo.activate(self.user_id, 'some_campaign'))

    def test_activate_with_no_campaign_key_found(self):
        self.set_up('AB_T_50_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.activate('NO_SUCH_CAMPAIGN_KEY',
                          test['user']), None)

    def test_activate_wrong_campaign_type_passed(self):
        self.set_up('FR_T_0_W_100')
        result = self.vwo.activate('FR_T_0_W_100', 'user')
        self.assertIs(result, None)

    def test_activate_against_campaign_traffic_50_and_split_50_50(self):
        self.set_up('AB_T_50_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_against_campaign_traffic_100_and_split_50_50(self):
        self.set_up('AB_T_100_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_against_campaign_traffic_100_and_split_20_80(self):
        self.set_up('AB_T_100_W_20_80')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_against_campaign_traffic_20_and_split_10_90(self):
        self.set_up('AB_T_20_W_10_90')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_against_campaign_traffic_100_and_split_0_100(self):
        self.set_up('AB_T_100_W_0_100')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_against_campaign_traffic_100_and_split_33_x3(self):
        self.set_up('AB_T_100_W_33_33_33')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    # Test track
    def test_track_invalid_params(self):
        self.set_up()
        self.assertIs(self.vwo.track(123, 456, 789), False)

    def test_track_invalid_config(self):
        self.set_up('EMPTY_SETTINGS_FILE')
        self.assertIs(self.vwo.track(self.user_id, 'somecampaign', 'somegoal'),
                      False
                      )

    def test_track_with_no_campaign_key_found(self):
        self.set_up('AB_T_50_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track('NO_SUCH_CAMPAIGN_KEY',
                          test['user'], self.goal_identifier), False)

    def test_track_with_no_goal_identifier_found(self):
        self.set_up('AB_T_50_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          'NO_SUCH_GOAL_IDENTIFIER'), False)

    def test_track_wrong_campaign_type_passed(self):
        self.set_up('FR_T_0_W_100')
        result = self.vwo.track('FR_T_0_W_100', 'user', 'some_goal_identifier')
        self.assertIs(result, False)

    def test_track_against_campaign_traffic_50_and_split_50_50(self):
        self.set_up('AB_T_50_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_100_and_split_50_50_r_int(self):
        # It's goal_type is revenue, so test revenue
        self.set_up('AB_T_100_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier, 23), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_100_and_split_50_50_r_float(self):
        # It's goal_type is revenue, so test revenue
        self.set_up('AB_T_100_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier, 23.3), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_100_and_split_50_50_r_str(self):
        # It's goal_type is revenue, so test revenue
        self.set_up('AB_T_100_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier, '23.3'), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_100_and_split_50_50_no_r(self):
        # It's goal_type is revenue, so test revenue
        self.set_up('AB_T_100_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), False)

    def test_track_against_campaign_traffic_100_and_split_50_50_kwargs(self):
        # It's goal_type is revenue, so test revenue
        self.set_up('AB_T_100_W_50_50')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier, revenue_value=23),
                          test['variation'] is not None)

    def test_track_against_campaign_traffic_100_and_split_20_80(self):
        self.set_up('AB_T_100_W_20_80')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_20_and_split_10_90(self):
        self.set_up('AB_T_20_W_10_90')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_100_and_split_0_100(self):
        self.set_up('AB_T_100_W_0_100')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_100_and_split_33_x3(self):
        self.set_up('AB_T_100_W_33_33_33')
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), test['variation']
                          is not None)
