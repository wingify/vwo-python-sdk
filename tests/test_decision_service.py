import unittest
import random
from .data.settings_files import SETTINGS_FILES
from vwo import decision_service
from vwo.helpers import campaign_util


class DecisionTest(unittest.TestCase):

    def setUp(self):

        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES[7]
        self.dummy_campaign = self.settings_file.get('campaigns')[0]
        self.campaign_test_key = self.dummy_campaign.get('key')
        campaign_util.set_variation_allocation(self.dummy_campaign)
        self.decisor = decision_service.DecisionService(self.settings_file)

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
