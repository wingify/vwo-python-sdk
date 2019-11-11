import unittest
import random

from vwo.services import singleton
from vwo.helpers import campaign_util
from ..data.settings_files import SETTINGS_FILES


class CampaingUtilTest(unittest.TestCase):

    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES["DUMMY_SETTINGS_FILE"]
        self.dummy_campaign = self.settings_file.get('campaigns')[0]
        self.campaign_key = self.dummy_campaign.get('key')
        self.goal_identifier = self.dummy_campaign.get('goals')[0].get('identifier')  # noqa: 501
        self.variation_name_control = \
            self.dummy_campaign.get('variations')[0].get('name')
        self.variation_name_variation = \
            self.dummy_campaign.get('variations')[1].get('name')
        campaign_util.set_variation_allocation(self.dummy_campaign)

    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_get_campaign_goal_none_campaing_passed(self):
        result = campaign_util.get_campaign_goal({},
                                                 self.goal_identifier)
        self.assertIsNone(result)

    def test_get_campaign_goal_none_goal_passed(self):
        result = campaign_util.get_campaign_goal(self.dummy_campaign,
                                                 None)
        self.assertIsNone(result)

    def test_get_campaign_goal_wrong_campaign_key_passed(self):
        result = campaign_util.get_campaign_goal({},
                                                 self.goal_identifier)
        self.assertIsNone(result)

    def test_get_campaign_variation_wrong_campaign_key_passed(self):
        result = \
            campaign_util.get_campaign_variation({},
                                                 self.variation_name_control)
        self.assertIsNone(result)

    def test_get_campaign_variation_wrong_variation_passed(self):
        result = \
            campaign_util.get_campaign_variation(self.dummy_campaign,
                                                 'SOME_VARIATION')
        self.assertIsNone(result)

    def test_get_campaign_variation_none_campaing_passed(self):
        result = \
            campaign_util.get_campaign_variation({},
                                                 self.variation_name_control)
        self.assertIsNone(result)

    def test_get_campaign_variation_none_goal_passed(self):
        result = \
            campaign_util.get_campaign_variation(self.dummy_campaign,
                                                 None)
        self.assertIsNone(result)

    def test_get_control_variation_return_none(self):
        self.dummy_campaign['variations'][0]['id'] = '3'
        result = \
            campaign_util.get_control_variation(self.dummy_campaign)
        self.assertIsNone(result)
        self.dummy_campaign['variations'][0]['id'] = '1'
