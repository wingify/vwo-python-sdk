import unittest
import random

from ..data.settings_files import SETTINGS_FILES
from vwo.core import variation_decider
from vwo.helpers import campaign_util
from vwo.services import singleton
from vwo import UserStorage


class VariationDeciderTest(unittest.TestCase):

    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES["DUMMY_SETTINGS_FILE"]
        self.dummy_campaign = self.settings_file.get('campaigns')[0]
        self.campaign_key = self.dummy_campaign.get('key')
        campaign_util.set_variation_allocation(self.dummy_campaign)
        self.decisor = variation_decider.VariationDecider(self.settings_file)

    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_init_with_valid_user_storage(self):

        class UPS:
            def set(self, user_data):
                pass

            def get(self, user_id, campaign_key):
                pass

        decisor = variation_decider.VariationDecider(self.settings_file, UPS())
        self.assertIsInstance(decisor.user_storage, UPS)

    def test_init_with_our_user_storage(self):
        decisor = variation_decider.VariationDecider(self.settings_file,
                                                     UserStorage())
        self.assertIsInstance(decisor.user_storage, UserStorage)

    def test_get_variation_allotted_none_userid_passed(self):
        variation = self.decisor.get_variation_allotted(
            None,
            self.dummy_campaign
        )
        self.assertIsNone(variation)

    def test_get_variation_allotted_should_return_true(self):
        user_id = 'Allie'
        # Allie, with above campaign settings, will get hashValue:362121553
        # and bucketValue:1688. So, MUST be a part of campaign as per campaign
        # percentTraffic
        variation = self.decisor.get_variation_allotted(
            user_id,
            self.dummy_campaign
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

    def test_get_variation_allotted_should_return_none(self):
        user_id = 'Lucian'
        # Lucian, with above campaign settings, will get hashValue:2251780191
        # and bucketValue:53. So, MUST be a part of campaign as per campaign
        # percentTraffic
        variation = self.decisor.get_variation_allotted(
            user_id,
            self.dummy_campaign
        )
        self.assertIsNone(variation)

    def test_get_variation_of_campaign_for_user_none_userid_passed(self):
        variation = self.decisor.get_variation_of_campaign_for_user(
            None,
            self.dummy_campaign
        )
        self.assertIsNone(variation)

    def test_get_variation_of_campaign_for_user_none_campaing_passed(self):
        variation = self.decisor.get_variation_of_campaign_for_user(
            self.user_id,
            None
        )
        self.assertIsNone(variation)

    def test_get_variation_of_campaign_for_user_should_return_Control(self):
        user_id = 'Sarah'
        # Sarah, with above campaign settings, will get hashValue:69650962
        # and bucketValue:326. So, MUST be a part of Control, as per campaign
        # settings
        variation = self.decisor.get_variation_of_campaign_for_user(
            user_id,
            self.dummy_campaign
        )
        self.assertEqual(variation.get('name'), 'Control')

    def test_get_variation_of_campaign_for_user_should_return_Variation(self):
        user_id = 'Varun'
        # Varun, with above campaign settings, will get hashValue:2025462540
        # and bucketValue:9433. So, MUST be a part of Variation, as per campaign
        # settings
        variation = self.decisor.get_variation_of_campaign_for_user(
            user_id,
            self.dummy_campaign
        )
        self.assertEqual(variation.get('name'), 'Variation-1')

    def test_get_none_userid_passed(self):
        variation = self.decisor.get_variation(
            None,
            self.dummy_campaign,
            self.campaign_key
        )
        self.assertIsNone(variation)

    def test_get_none_campaing_key_passed(self):
        user_id = 'Sarah'
        variation = self.decisor.get_variation(
            user_id,
            self.dummy_campaign,
            None
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

    def test_get_with_user_storage_(self):
        client_db = {}

        class UPS(UserStorage):
            def get(self, user_id, campaing_test_key):
                return client_db.get(user_id)

            def set(self, user_data):
                client_db[user_data['userId']] = user_data

        decisor = variation_decider.VariationDecider(self.settings_file, UPS())

        # First let decisor compute variation, and store
        user_id = 'Sarah'
        variation = decisor.get_variation(
            user_id,
            self.dummy_campaign,
            self.campaign_key
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

        # Now check whether the decisor is able to retrieve
        # variation for user_storage, no campaign is required
        # for this.
        variation = decisor.get_variation(
            user_id,
            self.dummy_campaign,
            self.campaign_key
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

    def test_get_with_broken_set_in_user_storage(self):
        client_db = {}

        class UPS(UserStorage):
            def get(self, user_id, campaign_key):
                return client_db.get(user_id)

            def set(self):
                pass

        decisor = variation_decider.VariationDecider(self.settings_file, UPS())

        user_id = 'Sarah'
        variation = decisor.get_variation(
            user_id,
            self.dummy_campaign,
            self.campaign_key
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

    def test_get_with_broken_get_in_user_storage(self):
        client_db = {}

        class UPS(UserStorage):
            def get(self):
                # def get(self, user_id): pass works, check later to rectify
                pass

            def set(self, user_data):
                client_db[user_data['userId']] = user_data

        decisor = variation_decider.VariationDecider(self.settings_file, UPS())

        user_id = 'Sarah'
        variation = decisor.get_variation(
            user_id,
            self.dummy_campaign,
            self.campaign_key
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

        variation = decisor.get_variation(
            user_id,
            self.dummy_campaign,
            self.campaign_key
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

    def test_get_with_user_storage_but_no_stored_variation(self):
        client_db = {}

        class UPS(UserStorage):
            def get(self, user_id, campaign_key):
                return client_db.get(user_id)

            def set(self, user_data):
                client_db[user_data['userId']] = user_data

        decisor = variation_decider.VariationDecider(self.settings_file, UPS())

        # First let decisor compute variation, and store
        user_id = 'Sarah'
        variation = decisor.get_variation(
            user_id,
            self.dummy_campaign,
            self.campaign_key
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')

        # Now delete the stored variaion from campaign_bucket_map
        del client_db[user_id]['variationName']
        # Now the decisor is not able to retrieve
        # variation from user_storage.
        variation = decisor.get_variation(
            user_id,
            self.dummy_campaign,
            self.campaign_key
        )
        self.assertEqual(variation.get('id'), '1')
        self.assertEqual(variation.get('name'), 'Control')
