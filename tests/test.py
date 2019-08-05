import unittest
import json
import vwo
from data.settings_files import SETTINGS_FILES
from data.settings_file_and_user_expectations import USER_EXPECTATIONS

DEV_TEST = 'DEV_TEST_{}'


class IndexTestCase(unittest.TestCase):

  def set_up(self, config_variant):
    self.settings_file = json.dumps(
        SETTINGS_FILES.get(
            config_variant
        )
    )
    self.vwo = vwo.VWO(self.settings_file)
    self.campaign_key = DEV_TEST.format(config_variant)

  def test_get_variation_1(self):
    self.set_up(1)
    for test in USER_EXPECTATIONS[self.campaign_key]:
      self.assertEqual(
          self.vwo.get_variation(
              self.campaign_key, test['user']), test['variation']
      )

  def test_get_variation_2(self):
    self.set_up(2)
    for test in USER_EXPECTATIONS[self.campaign_key]:
      self.assertEqual(
          self.vwo.get_variation(
              self.campaign_key, test['user']), test['variation']
      )

  def test_get_variation_3(self):
    self.set_up(3)
    for test in USER_EXPECTATIONS[self.campaign_key]:
      self.assertEqual(
          self.vwo.get_variation(
              self.campaign_key, test['user']), test['variation']
      )

  def test_get_variation_4(self):
    self.set_up(4)
    for test in USER_EXPECTATIONS[self.campaign_key]:
      self.assertEqual(
          self.vwo.get_variation(
              self.campaign_key, test['user']), test['variation']
      )

  def test_get_variation_5(self):
    self.set_up(5)
    for test in USER_EXPECTATIONS[self.campaign_key]:
      self.assertEqual(
          self.vwo.get_variation(
              self.campaign_key, test['user']), test['variation']
      )

  def test_get_variation_6(self):
    self.set_up(6)
    for test in USER_EXPECTATIONS[self.campaign_key]:
      self.assertEqual(
          self.vwo.get_variation(
              self.campaign_key, test['user']), test['variation']
      )


suite = unittest.TestLoader().loadTestsFromTestCase(IndexTestCase)

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
