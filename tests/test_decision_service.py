import unittest
import random

from .data.settings_files import SETTINGS_FILES
from vwo import decision_service
from vwo.helpers import campaign_util, singleton
from vwo import UserProfileService


class DecisionTest(unittest.TestCase):

    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES[7]
        self.dummy_campaign = self.settings_file.get('campaigns')[0]
        self.campaign_test_key = self.dummy_campaign.get('key')
        campaign_util.set_variation_allocation(self.dummy_campaign)
        self.decisor = decision_service.DecisionService(self.settings_file)

    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_init_with_valid_user_profile(self):

        class UPS:
            def save(self, user_id):
                pass

            def lookup(self, user_profile_obj):
                pass

        decisor = decision_service.DecisionService(self.settings_file, UPS())
        self.assertIsInstance(decisor.user_profile_service, UPS)

    def test_init_with_our_user_profile(self):
        decisor = decision_service.DecisionService(self.settings_file,
                                                   UserProfileService())
        self.assertIsInstance(decisor.user_profile_service, UserProfileService)

    def test_get_variation_allotted_none_campaign_passed(self):
        variation_id, variation_name = self.decisor.get_variation_allotted(
            self.user_id,
            None
        )
        self.assertIsNone(variation_id)
        self.assertIsNone(variation_name)

    def test_get_variation_allotted_none_userid_passed(self):
        variation_id, variation_name = self.decisor.get_variation_allotted(
            None,
            self.dummy_campaign
        )
        self.assertIsNone(variation_id)
        self.assertIsNone(variation_name)

    def test_get_variation_allotted_should_return_true(self):
        user_id = 'Allie'
        # Allie, with above campaign settings, will get hashValue:362121553
        # and bucketValue:1688. So, MUST be a part of campaign as per campaign
        # percentTraffic
        variation_id, variation_name = self.decisor.get_variation_allotted(
            user_id,
            self.dummy_campaign
        )
        self.assertEqual(variation_id, '1')
        self.assertEqual(variation_name, 'Control')

    def test_get_variation_allotted_should_return_false(self):
        user_id = 'Lucian'
        # Lucian, with above campaign settings, will get hashValue:2251780191
        # and bucketValue:53. So, MUST be a part of campaign as per campaign
        # percentTraffic
        variation_id, variation_name = self.decisor.get_variation_allotted(
            user_id,
            self.dummy_campaign
        )
        self.assertIsNone(variation_id)
        self.assertIsNone(variation_name)

    def test_get_variation_of_campaign_for_user_none_userid_passed(self):
        variation_id, variation_name = self.decisor.get_variation_of_campaign_for_user(  # noqa: E501
            None,
            self.dummy_campaign
        )
        self.assertIsNone(variation_id)
        self.assertIsNone(variation_name)

    def test_get_variation_of_campaign_for_user_none_campaing_passed(self):
        variation_id, variation_name = self.decisor.get_variation_of_campaign_for_user(  # noqa: E501
            self.user_id,
            None
        )
        self.assertIsNone(variation_id)
        self.assertIsNone(variation_name)

    def test_get_variation_of_campaign_for_user_should_return_Control(self):
        user_id = 'Sarah'
        # Sarah, with above campaign settings, will get hashValue:69650962
        # and bucketValue:326. So, MUST be a part of Control, as per campaign
        # settings
        variation_id, variation_name = self.decisor.get_variation_of_campaign_for_user(  # noqa: E501
            user_id,
            self.dummy_campaign
        )
        self.assertEqual(variation_name, 'Control')

    def test_get_variation_of_campaign_for_user_should_return_Variation(self):
        user_id = 'Varun'
        # Varun, with above campaign settings, will get hashValue:2025462540
        # and bucketValue:9433. So, MUST be a part of Variation, as per campaign
        # settings
        variation_id, variation_name = self.decisor.get_variation_of_campaign_for_user(  # noqa: E501
            user_id,
            self.dummy_campaign
        )
        self.assertEqual(variation_name, 'Variation-1')

    def test_get_none_userid_passed(self):
        variation_id, variation_name = self.decisor.get(
            None,
            self.dummy_campaign,
            self.campaign_test_key
        )
        self.assertIsNone(variation_id)
        self.assertIsNone(variation_name)

    def test_get_none_campaign_passed(self):
        variation_id, variation_name = self.decisor.get(
            self.user_id,
            None,
            self.campaign_test_key
        )
        self.assertIsNone(variation_id)
        self.assertIsNone(variation_name)

    def test_get_none_campaing_key_passed(self):
        user_id = 'Sarah'
        variation_id, variation_name = self.decisor.get(
            user_id,
            self.dummy_campaign,
            None
        )
        self.assertEqual(variation_id, '1')
        self.assertEqual(variation_name, 'Control')

    def test_get_with_user_profile_(self):
        client_db = {}

        class UPS(UserProfileService):
            def lookup(self, user_id):
                return client_db.get(user_id)

            def save(self, user_profile_obj):
                client_db[user_profile_obj['userId']] = user_profile_obj

        decisor = decision_service.DecisionService(self.settings_file, UPS())

        # First let decisor compute vairation, and store
        user_id = 'Sarah'
        variation_id, variation_name = decisor.get(
            user_id,
            self.dummy_campaign,
            self.campaign_test_key
        )
        self.assertEqual(variation_id, '1')
        self.assertEqual(variation_name, 'Control')

        # Now check whether the decisor is able to retrieve
        # variation for user_profile, no campaign is required
        # for this.
        variation_id, variation_name = decisor.get(
            user_id,
            None,
            self.campaign_test_key
        )
        self.assertEqual(variation_id, '1')
        self.assertEqual(variation_name, 'Control')

    def test_get_with_broken_save_in_user_profile(self):
        client_db = {}

        class UPS(UserProfileService):
            def lookup(self, user_id):
                return client_db.get(user_id)

            def save(self):
                pass

        decisor = decision_service.DecisionService(self.settings_file, UPS())

        user_id = 'Sarah'
        variation_id, variation_name = decisor.get(
            user_id,
            self.dummy_campaign,
            self.campaign_test_key
        )
        self.assertEqual(variation_id, '1')
        self.assertEqual(variation_name, 'Control')

    def test_get_with_broken_lookup_in_user_profile(self):
        client_db = {}

        class UPS(UserProfileService):
            def lookup(self):
                # def lookup(self, user_id): pass works, check later to rectify
                pass

            def save(self, user_profile_obj):
                client_db[user_profile_obj['userId']] = user_profile_obj

        decisor = decision_service.DecisionService(self.settings_file, UPS())

        user_id = 'Sarah'
        variation_id, variation_name = decisor.get(
            user_id,
            self.dummy_campaign,
            self.campaign_test_key
        )
        self.assertEqual(variation_id, '1')
        self.assertEqual(variation_name, 'Control')

        variation_id, variation_name = decisor.get(
            user_id,
            self.dummy_campaign,
            self.campaign_test_key
        )
        self.assertEqual(variation_id, '1')
        self.assertEqual(variation_name, 'Control')

    def test_get_with_user_profile_but_no_stored_variation(self):
        client_db = {}

        class UPS(UserProfileService):
            def lookup(self, user_id):
                return client_db.get(user_id)

            def save(self, user_profile_obj):
                client_db[user_profile_obj['userId']] = user_profile_obj

        decisor = decision_service.DecisionService(self.settings_file, UPS())

        # First let decisor compute vairation, and store
        user_id = 'Sarah'
        variation_id, variation_name = decisor.get(
            user_id,
            self.dummy_campaign,
            self.campaign_test_key
        )
        self.assertEqual(variation_id, '1')
        self.assertEqual(variation_name, 'Control')

        # Now delete the stored variaion from campaign_bucket_map
        del client_db[user_id]['campaignBucketMap']['UNIQUE_KEY']
        # Now the decisor is not able to retrieve
        # variation from user_profile.
        variation_id, variation_name = decisor.get(
            user_id,
            self.dummy_campaign,
            self.campaign_test_key
        )
        self.assertEqual(variation_id, '1')
        self.assertEqual(variation_name, 'Control')
