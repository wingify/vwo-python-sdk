import unittest
import json
import vwo
from .data.settings_files import SETTINGS_FILES
from .data.settings_file_and_user_expectations import USER_EXPECTATIONS

DEV_TEST = 'DEV_TEST_{}'


class VWOTest(unittest.TestCase):

    def set_up(self, config_variant=1):
        self.settings_file = \
            json.dumps(SETTINGS_FILES.get(config_variant))

        self.vwo = vwo.VWO(self.settings_file,
                           is_development_mode=True,
                           logger=vwo.logger.DefaultLogger(100))
        self.campaign_key = DEV_TEST.format(config_variant)
        self.goal_identifier = \
            SETTINGS_FILES[config_variant]['campaigns'][0]['goals'][0]['identifier']  # noqa: E501

    # Test get_variation
    def test_get_variation_with_no_campaign_key_found(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.get_variation('NO_SUCH_CAMPAIGN_KEY',
                          test['user']), None)

    def test_get_variation_against_campaign_traffic_50_and_split_50_50(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_against_campaign_traffic_100_and_split_50_50(self):
        self.set_up(2)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_against_campaign_traffic_100_and_split_20_80(self):
        self.set_up(3)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_against_campaign_traffic_20_and_split_10_90(self):
        self.set_up(4)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_against_campaign_traffic_100_and_split_0_100(self):
        self.set_up(5)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_against_campaign_traffic_100_and_split_33_x3(self):
        self.set_up(6)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    # Test activate
    def test_activate_with_no_campaign_key_found(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.activate('NO_SUCH_CAMPAIGN_KEY',
                          test['user']), None)

    def test_activate_against_campaign_traffic_50_and_split_50_50(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_against_campaign_traffic_100_and_split_50_50(self):
        self.set_up(2)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_against_campaign_traffic_100_and_split_20_80(self):
        self.set_up(3)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_against_campaign_traffic_20_and_split_10_90(self):
        self.set_up(4)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_against_campaign_traffic_100_and_split_0_100(self):
        self.set_up(5)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_against_campaign_traffic_100_and_split_33_x3(self):
        self.set_up(6)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    # Test track
    def test_track_with_no_campaign_key_found(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track('NO_SUCH_CAMPAIGN_KEY',
                          test['user'], self.goal_identifier), False)

    def test_track_with_no_goal_identifier_found(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          'NO_SUCH_GOAL_IDENTIFIER'), False)

    def test_track_against_campaign_traffic_50_and_split_50_50(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_100_and_split_50_50(self):
        self.set_up(2)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_100_and_split_20_80(self):
        self.set_up(3)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_20_and_split_10_90(self):
        self.set_up(4)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_100_and_split_0_100(self):
        self.set_up(5)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), test['variation']
                          is not None)

    def test_track_against_campaign_traffic_100_and_split_33_x3(self):
        self.set_up(6)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'],
                          self.goal_identifier), test['variation']
                          is not None)
