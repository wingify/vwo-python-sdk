# Copyright 2019-2020 Wingify Software Pvt. Ltd.
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
import random
import copy
from ..data.settings_files import SETTINGS_FILES
from vwo.core.variation_decider import VariationDecider
from vwo.helpers import campaign_util
from vwo.services import singleton
from vwo import UserStorage


class ClientUserStorage:
    def __init__(self):
        self.storage = {}

    def get(self, user_id, campaign_key):
        return self.storage.get((user_id, campaign_key))

    def set(self, user_data):
        self.storage[(user_data.get('userId'), user_data.get('campaignKey'))] = user_data


class VariationDeciderTest(unittest.TestCase):

    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES["DUMMY_SETTINGS_FILE"]
        self.dummy_campaign = self.settings_file.get('campaigns')[0]
        self.campaign_key = self.dummy_campaign.get('key')
        campaign_util.set_variation_allocation(self.dummy_campaign)
        self.variation_decider = VariationDecider()
        self.user_storage = ClientUserStorage()

    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_init_with_valid_user_storage(self):

        class US:
            def set(self, user_data):
                pass

            def get(self, user_id, campaign_key):
                pass

        variation_decider = VariationDecider(US())
        self.assertIsInstance(variation_decider.user_storage, US)

    def test_init_with_our_user_storage(self):
        variation_decider = VariationDecider(UserStorage())
        self.assertIsInstance(variation_decider.user_storage, UserStorage)

    def test_get_with_user_storage_(self):
        client_db = {}

        class US(UserStorage):
            def get(self, user_id, _campaign_key):
                return client_db.get(user_id)

            def set(self, user_data):
                client_db[user_data['userId']] = user_data

        variation_decider = VariationDecider(US())

        # First let variation_decider compute variation, and store
        user_id = 'Sarah'
        variation = variation_decider.get_variation(
            user_id,
            self.dummy_campaign,
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

        # Now check whether the variation_decider is able to retrieve
        # variation for user_storage, no campaign is required
        # for this.
        variation = variation_decider.get_variation(
            user_id,
            self.dummy_campaign,
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

    def test_get_with_broken_set_in_user_storage(self):
        client_db = {}

        class US(UserStorage):
            def get(self, user_id, campaign_key):
                return client_db.get(user_id)

            def set(self):
                pass

        variation_decider = VariationDecider(US())

        user_id = 'Sarah'
        variation = variation_decider.get_variation(
            user_id,
            self.dummy_campaign,
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

    def test_get_with_broken_get_in_user_storage(self):
        client_db = {}

        class US(UserStorage):
            def get(self):
                # def get(self, user_id): pass works, check later to rectify
                pass

            def set(self, user_data):
                client_db[user_data['userId']] = user_data

        variation_decider = VariationDecider(US())

        user_id = 'Sarah'
        variation = variation_decider.get_variation(
            user_id,
            self.dummy_campaign,
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

        variation = variation_decider.get_variation(
            user_id,
            self.dummy_campaign,
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

    def test_get_variation_from_user_storage_no_get(self):
        variation_decider = VariationDecider()
        variation = variation_decider.get_variation_from_user_storage('Sarah', {'campaign_key': 'AB_BA'})
        self.assertIsNone(variation)

    def test_get_variation_from_user_storage_return_variation(self):
        client_storage = ClientUserStorage()
        variation_decider = VariationDecider(user_storage=client_storage)
        campaign = self.settings_file['campaigns'][0]
        variation = campaign['variations'][0]
        set_status = variation_decider._set_user_storage_data('Sarah', campaign.get('key'), variation.get('name'))
        self.assertIs(set_status, True)
        result_variation = variation_decider.get_variation_from_user_storage('Sarah', campaign)
        self.assertEquals(result_variation.get('name'), variation.get('name'))

    def test_find_targeted_variation_returns_None(self):
        variation_decider = VariationDecider()
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = settings_file['campaigns'][0]
        false_variation_targeting_variables = {
            'chrome': 'true',
            'safari': 'false',
            'browser': 'firefox 106.69'
        }
        result_variation = variation_decider.find_targeted_variation('Sarah',
                                                                     campaign,
                                                                     false_variation_targeting_variables)
        self.assertIsNone(result_variation)

    def test_find_targeted_variation_returns_control(self):
        variation_decider = VariationDecider()
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = settings_file['campaigns'][0]
        true_variation_targeting_variables = {
            'chrome': 'false',
            'safari': 'true',
            'browser': 'chrome 107.107'
        }
        result_variation = variation_decider.find_targeted_variation('Sarah',
                                                                     campaign,
                                                                     true_variation_targeting_variables)
        self.assertEquals('Control', result_variation.get('name'))

    def test_evaluate_pre_segmentation_fails(self):
        variation_decider = VariationDecider()
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = settings_file['campaigns'][0]
        false_custom_variables = {
            'contains_vwo': 'legends say that vwo is the best',
            'regex_for_no_zeros': 1223123,
            'regex_for_all_letters': 'dsfASF',
            'regex_for_small_letters': 'sadfksjdf',
            'regex_real_number': 12321.2242,
            'regex_for_zeros': 0,
            'is_equal_to': '!equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'this    is    regex',
            'starts_with': 'starts_with_variable'
        }
        status = variation_decider.evaluate_pre_segmentation('Sarah', campaign, false_custom_variables)
        self.assertEquals(status, False)

    def test_evaluate_pre_segmentation_passes(self):
        variation_decider = VariationDecider()
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = settings_file['campaigns'][0]
        true_custom_variables = {
            'contains_vwo': 'legends say that vwo is the best',
            'regex_for_no_zeros': 1223123,
            'regex_for_all_letters': 'dsfASF',
            'regex_for_small_letters': 'sadfksjdf',
            'regex_real_number': 12321.2242,
            'regex_for_zeros': 0,
            'is_equal_to': 'equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'this    is    regex',
            'starts_with': 'starts_with_variable'
        }
        status = variation_decider.evaluate_pre_segmentation('Sarah', campaign, true_custom_variables)
        self.assertEquals(status, True)

    def test_get_white_listed_variations_list_returns_empty_list_all_fails(self):
        variation_decider = VariationDecider()
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = settings_file['campaigns'][0]
        false_variation_targeting_variables = {
            'chrome': 'true',
            'safari': 'false',
            'browser': 'firefox 106.69'
        }
        variation_list = variation_decider._get_white_listed_variations_list('Sarah',
                                                                             campaign,
                                                                             false_variation_targeting_variables)
        self.assertFalse(variation_list)

    def test_get_white_listed_variations_list_returns_empty_list_control_empty_segments(self):
        variation_decider = VariationDecider()
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = copy.deepcopy(settings_file['campaigns'][0])
        campaign['variations'][0]['segments'] = {}
        false_variation_targeting_variables = {
            'chrome': 'true',
            'safari': 'false',
            'browser': 'firefox 106.69'
        }
        variation_list = variation_decider._get_white_listed_variations_list('Sarah',
                                                                             campaign,
                                                                             false_variation_targeting_variables)
        self.assertFalse(variation_list)

    def test_get_white_listed_variations_list_returns_variation_1_list_variation_1_whitelisting_pass(self):
        variation_decider = VariationDecider()
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = copy.deepcopy(settings_file['campaigns'][0])
        campaign['variations'][1]['segments'] = {
            "or": [
                {
                    "custom_variable": {
                        "browser": 'wildcard(firefox*)'
                    }
                }
            ]
        }
        false_variation_targeting_variables = {
            'chrome': 'true',
            'safari': 'false',
            'browser': 'firefox 106.69'
        }
        variation_list = variation_decider._get_white_listed_variations_list('Sarah',
                                                                             campaign,
                                                                             false_variation_targeting_variables)
        self.assertTrue(variation_list)
        self.assertEquals(variation_list[0].get('name'), 'Variation-1')

    def test_get_white_listed_variations_list_returns_all_variation_list_whitelisting_passes_for_all(self):
        variation_decider = VariationDecider()
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = copy.deepcopy(settings_file['campaigns'][0])
        true_variation_targeting_variables = {
            'chrome': 'false',
            'safari': 'true',
            'browser': 'chrome 107.107'
        }
        variation_list = variation_decider._get_white_listed_variations_list('Sarah',
                                                                             campaign,
                                                                             true_variation_targeting_variables)
        self.assertTrue(variation_list)
        self.assertEquals(variation_list[0].get('name'), 'Control')
        self.assertEquals(variation_list[1].get('name'), 'Variation-1')
        self.assertEquals(variation_list[2].get('name'), 'Variation-2')

    def test_is_user_part_of_campaign_true(self):
        variation_decider = VariationDecider()
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = copy.deepcopy(settings_file['campaigns'][0])
        status = variation_decider.is_user_part_of_campaign('Sarah', campaign)
        self.assertTrue(status)

    def test_is_user_part_of_campaign_false(self):
        variation_decider = VariationDecider()
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = copy.deepcopy(settings_file['campaigns'][0])
        campaign['percentTraffic'] = 1
        status = variation_decider.is_user_part_of_campaign('Sarah', campaign)
        self.assertFalse(status)

    def test_set_user_storage_data_return_true(self):
        client_storage = ClientUserStorage()
        variation_decider = VariationDecider(user_storage=client_storage)
        campaign = self.settings_file['campaigns'][0]
        variation = campaign['variations'][0]
        set_status = variation_decider._set_user_storage_data('Sarah', campaign.get('key'), variation.get('name'))
        self.assertIs(set_status, True)

    def test_get_user_storage_data_true(self):
        client_storage = ClientUserStorage()
        variation_decider = VariationDecider(user_storage=client_storage)
        user_storage_data = {'userId': 'Sarah', 'campaignKey': 'FEATURE_TEST_1', 'variationName': 'DESIGN_4'}
        client_storage.set(user_storage_data)
        result_user_storage_data = variation_decider._get_user_storage_data('Sarah', 'FEATURE_TEST_1')
        self.assertDictEqual(result_user_storage_data, user_storage_data)

    def test_get_user_storage_data_false_different_campaign(self):
        client_storage = ClientUserStorage()
        variation_decider = VariationDecider(user_storage=client_storage)
        user_storage_data = {'userId': 'Sarah', 'campaignKey': 'FEATURE_TEST_2', 'variationName': 'DESIGN_4'}
        client_storage.set(user_storage_data)
        result_user_storage_data = variation_decider._get_user_storage_data('Sarah', 'FEATURE_TEST_1')
        self.assertIsNone(result_user_storage_data)

    def test_get_variation_from_user_storage_returns_none_as_garbage_variation_name(self):
        client_storage = ClientUserStorage()
        variation_decider = VariationDecider(user_storage=client_storage)
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = settings_file['campaigns'][0]
        user_storage_data = {'userId': 'Sarah', 'campaignKey': 'FEATURE_TEST_2', 'variationName': 'None'}
        client_storage.set(user_storage_data)
        result_variation = variation_decider.get_variation_from_user_storage('Sarah', campaign)
        self.assertIsNone(result_variation)

    def test_get_variation_from_user_storage_returns_control(self):
        client_storage = ClientUserStorage()
        variation_decider = VariationDecider(user_storage=client_storage)
        settings_file = SETTINGS_FILES.get('FT_100_W_33_33_33_WS_WW')
        campaign = settings_file['campaigns'][0]
        user_storage_data = {
            'userId': 'Sarah',
            'campaignKey': campaign['key'],
            'variationName': campaign['variations'][0]['name']
        }
        client_storage.set(user_storage_data)
        result_variation = variation_decider.get_variation_from_user_storage('Sarah', campaign)
        self.assertEquals(result_variation['name'], campaign['variations'][0]['name'])

    def test_set_get_user_storage_data(self):
        user_storage = ClientUserStorage()
        variation_decider = VariationDecider(user_storage)
        variation_decider._set_user_storage_data('user_id', 'campaign_key', 'variation_name')
        self.assertEquals(user_storage.storage.get(('user_id', 'campaign_key')),
                          variation_decider._get_user_storage_data('user_id', 'campaign_key'))

    def test_set_user_storage_data(self):
        user_storage = ClientUserStorage()
        variation_decider = VariationDecider(user_storage)
        variation_decider._set_user_storage_data('user_id', 'campaign_key_1', 'variation_name_1')
        variation_decider._set_user_storage_data('user_id', 'campaign_key_2', 'variation_name_2')
        self.assertEquals(user_storage.storage.get(('user_id', 'campaign_key_1')),
                          variation_decider._get_user_storage_data('user_id', 'campaign_key_1'))
        self.assertEquals(user_storage.storage.get(('user_id', 'campaign_key_2')),
                          variation_decider._get_user_storage_data('user_id', 'campaign_key_2'))
