import unittest
import random

from vwo.helpers import singleton, campaign_util
from ..data.settings_files import SETTINGS_FILES


class CampaingTest(unittest.TestCase):

    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES[7]
        self.dummy_campaign = self.settings_file.get('campaigns')[0]
        self.campaign_test_key = self.dummy_campaign.get('key')
        self.goal_identifier = self.dummy_campaign.get('goals')[0].get('identifier')  # noqa: 501
        self.variation_name_control = \
            self.dummy_campaign.get('variations')[0].get('name')
        self.variation_name_variation = \
            self.dummy_campaign.get('variations')[1].get('name')
        campaign_util.set_variation_allocation(self.dummy_campaign)

    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_get_campaign_goal_invalid_settings_file(self):
        result = campaign_util.get_campaign_goal({},
                                                 self.campaign_test_key,
                                                 self.goal_identifier)
        self.assertIsNone(result)

    def test_get_campaign_goal_none_campaing_passed(self):
        result = campaign_util.get_campaign_goal(self.settings_file,
                                                 None,
                                                 self.goal_identifier)
        self.assertIsNone(result)

    def test_get_campaign_goal_none_goal_passed(self):
        result = campaign_util.get_campaign_goal(self.settings_file,
                                                 self.campaign_test_key,
                                                 None)
        self.assertIsNone(result)

    def test_get_campaign_goal_wrong_campaign_key_passed(self):
        result = campaign_util.get_campaign_goal(self.settings_file,
                                                 'SOMETHING',
                                                 self.goal_identifier)
        self.assertIsNone(result)

    def test_get_campaign_variation_wrong_campaign_key_passed(self):
        result = \
            campaign_util.get_campaign_variation(self.settings_file,
                                                 'SOMETHING',
                                                 self.variation_name_control)
        self.assertIsNone(result)

    def test_get_campaign_variation_wrong_variation_passed(self):
        result = \
            campaign_util.get_campaign_variation(self.settings_file,
                                                 self.campaign_test_key,
                                                 'SOME_VARIATION')
        self.assertIsNone(result)

    def test_get_campaign_variation_invalid_settings_file(self):
        result = campaign_util.get_campaign_variation({},
                                                      self.campaign_test_key,
                                                      self.variation_name_control)  # noqa: 501
        self.assertIsNone(result)

    def test_get_campaign_variation_none_campaing_passed(self):
        result = \
            campaign_util.get_campaign_variation(self.settings_file,
                                                 None,
                                                 self.variation_name_control)
        self.assertIsNone(result)

    def test_get_campaign_variation_none_goal_passed(self):
        result = \
            campaign_util.get_campaign_variation(self.settings_file,
                                                 self.campaign_test_key,
                                                 None)
        self.assertIsNone(result)
