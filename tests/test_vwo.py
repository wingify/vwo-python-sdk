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

    def test_get_variation_name_against_campaign_traffic_75_and_split_10_TIMES_10(self):
        self.set_up('T_75_W_10_TIMES_10')
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

    # Test is_feature_enabled on Feature_rollout
    def test_is_feature_enabled_wrong_campaign_key_passed(self):
        self.set_up('FR_T_0_W_100')
        result = self.vwo.is_feature_enabled('not_a_campaign_key', 'user')
        self.assertIs(result, False)

    def test_is_feature_enabled_wrong_campaign_type_passed(self):
        self.set_up('AB_T_50_W_50_50')
        result = self.vwo.is_feature_enabled('AB_T_50_W_50_50', 'user')
        self.assertIs(result, False)

    def test_is_feature_enabled_invalid_config(self):
        self.set_up('EMPTY_SETTINGS_FILE')
        self.assertIs(
            self.vwo.is_feature_enabled(
                self.user_id,
                'some_campaign'
            ),
            False
        )

    def test_is_feature_enabled_wrong_parmas_passed(self):
        self.set_up('FR_T_0_W_100')
        self.assertIs(self.vwo.is_feature_enabled(123, 456), False)

    def test_is_feature_enabled_FR_W_0(self):
        self.set_up('FR_T_0_W_100')
        for test in USER_EXPECTATIONS.get('T_0_W_10_20_30_40'):
            self.assertIs(
                self.vwo.is_feature_enabled('FR_T_0_W_100', test['user']),
                test['variation'] is not None
            )

    def test_is_feature_enabled_FR_W_25(self):
        self.set_up('FR_T_25_W_100')
        for test in USER_EXPECTATIONS.get('T_25_W_10_20_30_40'):
            self.assertIs(
                self.vwo.is_feature_enabled('FR_T_25_W_100', test['user']),
                test['variation'] is not None
            )

    def test_is_feature_enabled_FR_W_50(self):
        self.set_up('FR_T_50_W_100')
        for test in USER_EXPECTATIONS.get('T_50_W_10_20_30_40'):
            self.assertIs(
                self.vwo.is_feature_enabled('FR_T_50_W_100', test['user']),
                test['variation'] is not None
            )

    def test_is_feature_enabled_FR_W_75(self):
        self.set_up('FR_T_75_W_100')
        for test in USER_EXPECTATIONS.get('T_75_W_10_20_30_40'):
            self.assertIs(
                self.vwo.is_feature_enabled('FR_T_75_W_100', test['user']),
                test['variation'] is not None
            )

    def test_is_feature_enabled_FR_W_100(self):
        self.set_up('FR_T_100_W_100')
        for test in USER_EXPECTATIONS.get('T_100_W_10_20_30_40'):
            self.assertIs(
                self.vwo.is_feature_enabled('FR_T_100_W_100', test['user']),
                test['variation'] is not None
            )

    def test_is_feature_enabled_FT_T_75_W_10_20_30_40(self):
        self.set_up('FT_T_75_W_10_20_30_40')
        for test in USER_EXPECTATIONS['T_75_W_10_20_30_40']:
            self.assertIs(
                self.vwo.is_feature_enabled('FT_T_75_W_10_20_30_40', test['user']),
                test['variation'] is not None
            )

    # Test get_feature_variable_value from rollout
    def test_get_feature_variable_value_boolean_from_rollout(self):
        self.set_up('FR_T_75_W_100')
        BOOLEAN_VARIABLE = USER_EXPECTATIONS['ROLLOUT_VARIABLES']['BOOLEAN_VARIABLE']
        for test in USER_EXPECTATIONS.get('T_75_W_10_20_30_40'):
            result = self.vwo.get_feature_variable_value(
                'FR_T_75_W_100',
                'BOOLEAN_VARIABLE',
                test['user']
            )
            if result:
                self.assertEquals(result, BOOLEAN_VARIABLE)

    # Test get_feature_variable_value from rollout
    def test_get_feature_variable_value_type_string_from_rollout(self):
        self.set_up('FR_T_75_W_100')
        STRING_VARIABLE = USER_EXPECTATIONS['ROLLOUT_VARIABLES']['STRING_VARIABLE']
        for test in USER_EXPECTATIONS.get('T_75_W_10_20_30_40'):
            result = self.vwo.get_feature_variable_value(
                'FR_T_75_W_100',
                'STRING_VARIABLE',
                test['user']
            )
            if result:
                self.assertEquals(result, STRING_VARIABLE)

    # Test get_feature_variable_value from rollout
    def test_get_feature_variable_value_type_boolean_from_rollout(self):
        self.set_up('FR_T_75_W_100')
        DOUBLE_VARIABLE = USER_EXPECTATIONS['ROLLOUT_VARIABLES']['DOUBLE_VARIABLE']
        for test in USER_EXPECTATIONS.get('T_75_W_10_20_30_40'):
            result = self.vwo.get_feature_variable_value(
                'FR_T_75_W_100',
                'DOUBLE_VARIABLE',
                test['user']
            )
            if result:
                self.assertEquals(result, DOUBLE_VARIABLE)

    # Test get_feature_variable_value from rollout
    def test_get_feature_variable_value_type_integer_from_rollout(self):
        self.set_up('FR_T_75_W_100')
        INTEGER_VARIABLE = USER_EXPECTATIONS['ROLLOUT_VARIABLES']['INTEGER_VARIABLE']
        for test in USER_EXPECTATIONS.get('T_75_W_10_20_30_40'):
            result = self.vwo.get_feature_variable_value(
                'FR_T_75_W_100',
                'INTEGER_VARIABLE',
                test['user']
            )
            if result:
                self.assertEquals(result, INTEGER_VARIABLE)

    # Test get_feature_variable_value from feature test from different feature splits
    def test_get_feature_variable_value_type_string_from_feature_test_t_0(self):
        self.set_up('FT_T_0_W_10_20_30_40')
        STRING_VARIABLE = USER_EXPECTATIONS['STRING_VARIABLE']
        for test in USER_EXPECTATIONS.get('T_0_W_10_20_30_40'):
            result = self.vwo.get_feature_variable_value(
                'FT_T_0_W_10_20_30_40',
                'STRING_VARIABLE',
                test['user']
            )
            if result:
                self.assertEquals(result, STRING_VARIABLE[test['variation']])

    def test_get_feature_variable_value_type_string_from_feature_test_t_25(self):
        self.set_up('FT_T_25_W_10_20_30_40')
        STRING_VARIABLE = USER_EXPECTATIONS['STRING_VARIABLE']
        for test in USER_EXPECTATIONS.get('T_25_W_10_20_30_40'):
            result = self.vwo.get_feature_variable_value(
                'FT_T_25_W_10_20_30_40',
                'STRING_VARIABLE',
                test['user']
            )
            if result:
                self.assertEquals(result, STRING_VARIABLE[test['variation']])

    def test_get_feature_variable_value_type_string_from_feature_test_t_50(self):
        self.set_up('FT_T_50_W_10_20_30_40')
        STRING_VARIABLE = USER_EXPECTATIONS['STRING_VARIABLE']
        for test in USER_EXPECTATIONS.get('T_50_W_10_20_30_40'):
            result = self.vwo.get_feature_variable_value(
                'FT_T_50_W_10_20_30_40',
                'STRING_VARIABLE',
                test['user']
            )
            if result:
                self.assertEquals(result, STRING_VARIABLE[test['variation']])

    def test_get_feature_variable_value_type_string_from_feature_test_t_75(self):
        self.set_up('FT_T_75_W_10_20_30_40')
        STRING_VARIABLE = USER_EXPECTATIONS['STRING_VARIABLE']
        for test in USER_EXPECTATIONS.get('T_75_W_10_20_30_40'):
            result = self.vwo.get_feature_variable_value(
                'FT_T_75_W_10_20_30_40',
                'STRING_VARIABLE',
                test['user']
            )
            if result:
                self.assertEquals(result, STRING_VARIABLE[test['variation']])

    def test_get_feature_variable_value_type_string_from_feature_test_t_100(self):
        self.set_up('FT_T_100_W_10_20_30_40')
        STRING_VARIABLE = USER_EXPECTATIONS['STRING_VARIABLE']
        for test in USER_EXPECTATIONS.get('T_100_W_10_20_30_40'):
            result = self.vwo.get_feature_variable_value(
                'FT_T_100_W_10_20_30_40',
                'STRING_VARIABLE',
                test['user']
            )
            if result:
                self.assertEquals(result, STRING_VARIABLE[test['variation']])

    def test_get_feature_variable_value_type_string_from_feature_test_t_100_isFeatureEnalbed(self):
        # isFeatureEnalbed is False for variation-1 and variation-3,
        # should return variable from Control
        self.set_up('FT_T_100_W_10_20_30_40_IFEF')
        STRING_VARIABLE = USER_EXPECTATIONS['STRING_VARIABLE']
        for test in USER_EXPECTATIONS.get('T_100_W_10_20_30_40'):
            result = self.vwo.get_feature_variable_value(
                'FT_T_100_W_10_20_30_40_IFEF',
                'STRING_VARIABLE',
                test['user']
            )
            variation_name = test['variation']
            if variation_name in ['Variation-1', 'Variation-3']:
                variation_name = 'Control'
            if result:
                self.assertEquals(result, STRING_VARIABLE[variation_name])

    def test_get_feature_variable_wrong_variable_types(self):
        self.set_up('FR_WRONG_VARIABLE_TYPE')
        tests = [
            ("STRING_TO_INTEGER", 123, "integer", int),
            ("STRING_TO_FLOAT", 123.456, "double", float),
            ("BOOLEAN_TO_STRING", "True", "string", str),
            ("INTEGER_TO_STRING", "24", "string", str),
            ("INTEGER_TO_FLOAT", 24.0, "double", float),
            ("FLOAT_TO_STRING", "24.24", "string", str),
            ("FLOAT_TO_INTEGER", 24, "integer", int),
        ]
        for test in tests:
            result = self.vwo.get_feature_variable_value(
                'FR_WRONG_VARIABLE_TYPE',
                test[0],
                'Zin'
            )
            self.assertEquals(result, test[1])
            self.assertTrue(type(result) is test[3])

    # Testing private method _get_feature_variable

    def test_get_feature_variable_wrong_variable_types_return_none(self):
        self.set_up('FR_WRONG_VARIABLE_TYPE')
        tests = [
            ("WRONG_BOOLEAN", None, "boolean", None),
        ]
        for test in tests:
            result = self.vwo.get_feature_variable_value(
                'FR_WRONG_VARIABLE_TYPE',
                test[0],
                'Zin'
            )
            self.assertEquals(result, test[1])

    def test_get_feature_variable_invalid_params(self):
        self.set_up('FR_T_100_W_100')
        self.assertIsNone(self.vwo.get_feature_variable_value(123,
                                                              456,
                                                              789))

    def test_get_feature_variable_invalid_config(self):
        self.set_up('EMPTY_SETTINGS_FILE')
        self.assertIsNone(
            self.vwo.get_feature_variable_value(
                'campaign_key',
                'variable_key',
                'user_id'
            )
        )

    def test_get_feature_variable_invalid_campaing_key(self):
        self.set_up('FR_T_100_W_100')
        self.assertIsNone(
            self.vwo.get_feature_variable_value(
                'not_a_campaign',
                'STRING_VARIABLE',
                'Zin'
            )
        )

    def test_get_feature_variable_invalid_campaing_type(self):
        self.set_up('AB_T_50_W_50_50')
        self.assertIsNone(
            self.vwo.get_feature_variable_value(
                'AB_T_50_W_50_50',
                'STRING_VARIABLE',
                'Zin'
            )
        )

    # test each api raises exception

    def test_activate_raises_exception(self):
        def mock_is_valid_string():
            return None
        is_valid_string, validate_util.is_valid_string = \
            validate_util.is_valid_string, mock_is_valid_string
        self.set_up()
        self.assertIs(None, self.vwo.activate('SOME_CAMPAIGN', 'USER'))
        validate_util.is_valid_string = is_valid_string

    def test_get_variation_name_raises_exception(self):
        def mock_is_valid_string():
            return None
        is_valid_string, validate_util.is_valid_string = \
            validate_util.is_valid_string, mock_is_valid_string
        self.set_up()
        self.assertIs(None, self.vwo.get_variation_name('SOME_CAMPAIGN', 'USER'))
        validate_util.is_valid_string = is_valid_string

    def test_track_raises_exception(self):
        def mock_is_valid_string():
            return None
        is_valid_string, validate_util.is_valid_string = \
            validate_util.is_valid_string, mock_is_valid_string
        self.set_up()
        self.assertIs(None, self.vwo.track('SOME_CAMPAIGN', 'USER', 'GOAL'))
        validate_util.is_valid_string = is_valid_string

    def test_is_feature_enabled_raises_exception(self):
        def mock_is_valid_string():
            return None
        is_valid_string, validate_util.is_valid_string = \
            validate_util.is_valid_string, mock_is_valid_string
        self.set_up()
        self.assertIs(None, self.vwo.is_feature_enabled('SOME_CAMPAIGN', 'USER'))
        validate_util.is_valid_string = is_valid_string

    def test_get_feature_variable_raises_exception(self):
        def mock_is_valid_string():
            return None
        is_valid_string, validate_util.is_valid_string = \
            validate_util.is_valid_string, mock_is_valid_string
        self.set_up()
        self.assertIs(None, self.vwo.get_feature_variable_value('SOME_CAMPAIGN',
                                                                'VARIABLE_KEY',
                                                                'USER_ID'))
        validate_util.is_valid_string = is_valid_string

    def test_vwo_initialized_with_provided_log_level_DEBUG(self):
        vwo_instance = vwo.VWO(SETTINGS_FILES.get('AB_T_50_W_50_50'), log_level=vwo.LogLevels.DEBUG)
        self.assertEquals(vwo_instance.logger.logger.level, logging.DEBUG)

    def test_vwo_initialized_with_provided_log_level_WARNING(self):
        vwo_instance = vwo.VWO(SETTINGS_FILES.get('AB_T_50_W_50_50'), log_level=vwo.LogLevels.WARNING)
        self.assertEquals(vwo_instance.logger.logger.level, logging.WARNING)

    def test_vwo_initialized_with_provided_log_level_50(self):
        vwo_instance = vwo.VWO(SETTINGS_FILES.get('AB_T_50_W_50_50'), log_level=50)
        self.assertEquals(vwo_instance.logger.logger.level, 50)
