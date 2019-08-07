# flake8: noqa

import unittest
import json
import vwo
from data.settings_files import SETTINGS_FILES
from data.settings_file_and_user_expectations import USER_EXPECTATIONS
from data import test_util

DEV_TEST = 'DEV_TEST_{}'


class IndexTestCase(unittest.TestCase):

    def set_up(self, config_variant=1):
        self.settings_file = \
            json.dumps(SETTINGS_FILES.get(config_variant))

        self.vwo = vwo.VWO(self.settings_file,
                           is_development_mode=True,
                           logger=vwo.logger.DefaultLogger(100))
        self.campaign_key = DEV_TEST.format(config_variant)
        self.goal_identifier = \
            SETTINGS_FILES[config_variant]['campaigns'][0]['goals'
                ][0]['identifier']

    def test_get_variation_1(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_2(self):
        self.set_up(2)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_3(self):
        self.set_up(3)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_4(self):
        self.set_up(4)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_5(self):
        self.set_up(5)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    def test_get_variation_6(self):
        self.set_up(6)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.get_variation(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_1(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_2(self):
        self.set_up(2)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_3(self):
        self.set_up(3)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_4(self):
        self.set_up(4)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_5(self):
        self.set_up(5)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_activate_6(self):
        self.set_up(6)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertEqual(self.vwo.activate(self.campaign_key,
                             test['user']), test['variation'])

    def test_track_no_campaign_key_found(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track('NO_SUCH_CAMPAIGN_KEY',
                          test['user'], self.goal_identifier), False)

    def test_track_no_goal_identifier_passed(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'
                          ], 'NO_SUCH_GOAL_IDENTIFIER'), False)

    def test_track_to_be_true_1(self):
        self.set_up(1)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'
                          ], self.goal_identifier), test['variation']
                          is not None)

    def test_track_to_be_true_2(self):
        self.set_up(2)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'
                          ], self.goal_identifier), test['variation']
                          is not None)

    def test_track_to_be_true_3(self):
        self.set_up(3)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'
                          ], self.goal_identifier), test['variation']
                          is not None)

    def test_track_to_be_true_4(self):
        self.set_up(4)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'
                          ], self.goal_identifier), test['variation']
                          is not None)

    def test_track_to_be_true_5(self):
        self.set_up(5)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'
                          ], self.goal_identifier), test['variation']
                          is not None)

    def test_track_to_be_true_6(self):
        self.set_up(6)
        for test in USER_EXPECTATIONS[self.campaign_key]:
            self.assertIs(self.vwo.track(self.campaign_key, test['user'
                          ], self.goal_identifier), test['variation']
                          is not None)


suite = unittest.TestLoader().loadTestsFromTestCase(IndexTestCase)

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
