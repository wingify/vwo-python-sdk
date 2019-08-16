import unittest
import random

from vwo import bucketing_service
from vwo.helpers import campaign_util, singleton
from .data.settings_files import SETTINGS_FILES


class BucketingTest(unittest.TestCase):

    def setUp(self):

        self.user_id = str(random.random())
        self.dummy_campaign = {
            'goals': [
                {
                    'identifier': 'GOAL_NEW',
                    'id': 203,
                    'type': 'CUSTOM_GOAL'
                }
            ],
            'variations': [
                {
                    'id': '1',
                    'name': 'Control',
                    'weight': 40
                },
                {
                    'id': '2',
                    'name': 'Variation-1',
                    'weight': 60
                }
            ],
            'id': 22,
            'percentTraffic': 50,
            'key': 'UNIQUE_KEY',
            'status': 'RUNNING',
            'type': 'VISUAL_AB'
        }
        campaign_util.set_variation_allocation(self.dummy_campaign)
        self.bucketer = bucketing_service.Bucketer()

    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_user_part_of_campaign_none_campaign_passed(self):
        result = self.bucketer.is_user_part_of_campaign(self.user_id, None)
        self.assertIs(result, False)

    def test_user_part_of_campaign_none_userid_passed(self):
        result = self.bucketer.is_user_part_of_campaign(None,
                                                        self.dummy_campaign
                                                        )
        self.assertIs(result, False)

    def test_user_part_of_campaign_should_return_true(self):
        user_id = 'Bob'
        # Bob, with above campaign settings, will get hashValue:2033809345 and
        # bucketValue:48. So, MUST be a part of campaign as per campaign
        # percentTraffic
        result = self.bucketer.is_user_part_of_campaign(user_id,
                                                        self.dummy_campaign
                                                        )
        self.assertIs(result, True)

    def test_user_part_of_campaign_should_return_false(self):
        user_id = 'Lucian'
        # Lucian, with above campaign settings, will get hashValue:2251780191
        # and bucketValue:53. So, must NOT be a part of campaign as per campaign
        # percentTraffic
        result = self.bucketer.is_user_part_of_campaign(user_id,
                                                        self.dummy_campaign
                                                        )
        self.assertIs(result, False)

    def test_bucket_user_to_variation_none_campaign_passed(self):
        result = self.bucketer.bucket_user_to_variation(self.user_id, None)
        self.assertIsNone(result)

    def test_bucket_user_to_variation_none_userid_passed(self):
        result = self.bucketer.bucket_user_to_variation(None,
                                                        self.dummy_campaign
                                                        )
        self.assertIsNone(result)

    def test_bucket_user_to_variation_return_control(self):
        user_id = 'Sarah'
        # Sarah, with above campaign settings, will get hashValue:69650962 and
        # bucketValue:326. So, MUST be a part of Control, as per campaign
        # settings
        result = self.bucketer.bucket_user_to_variation(user_id,
                                                        self.dummy_campaign
                                                        )
        self.assertEqual(result.get('name'), 'Control')

    def test_bucket_user_to_variation_return_varitaion_1(self):
        user_id = 'Varun'
        # Varun, with above campaign settings, will get hashValue:69650962 and
        # bucketValue:326. So, MUST be a part of Variation-1, as per campaign
        # settings
        result = self.bucketer.bucket_user_to_variation(user_id,
                                                        self.dummy_campaign
                                                        )
        self.assertEqual(result.get('name'), 'Variation-1')

    def test_get_variation_return_none(self):
        campaign = SETTINGS_FILES[1].get('campaigns')[0]
        campaign_util.set_variation_allocation(campaign)
        result = self.bucketer._get_variation(campaign,
                                              10001
                                              )
        self.assertIsNone(result)
