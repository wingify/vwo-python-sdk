# Copyright 2019-2022 Wingify Software Pvt. Ltd.
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
import json

from vwo.helpers import campaign_util
from ..data.settings_files import SETTINGS_FILES

with open("tests/data/mutually_exclusive_test_cases.json") as mutually_exclusive_test_cases_json:
    mutually_exclusive_test_cases = json.load(mutually_exclusive_test_cases_json)


class CampaignUtilTest(unittest.TestCase):
    def setUp(self):
        self.user_id = str(random.random())
        self.settings_file = SETTINGS_FILES["DUMMY_SETTINGS_FILE"]
        self.dummy_campaign = self.settings_file.get("campaigns")[0]
        self.campaign_key = self.dummy_campaign.get("key")
        self.goal_identifier = self.dummy_campaign.get("goals")[0].get("identifier")  # noqa: 501
        self.variation_name_control = self.dummy_campaign.get("variations")[0].get("name")
        self.variation_name_variation = self.dummy_campaign.get("variations")[1].get("name")
        campaign_util.set_variation_allocation(self.dummy_campaign)

    def test_get_campaign_goal_none_campaign_passed(self):
        result = campaign_util.get_campaign_goal({}, self.goal_identifier)
        self.assertIsNone(result)

    def test_get_campaign_goal_none_goal_passed(self):
        result = campaign_util.get_campaign_goal(self.dummy_campaign, None)
        self.assertIsNone(result)

    def test_get_campaign_goal_wrong_campaign_key_passed(self):
        result = campaign_util.get_campaign_goal({}, self.goal_identifier)
        self.assertIsNone(result)

    def test_get_campaign_variation_wrong_campaign_key_passed(self):
        result = campaign_util.get_campaign_variation({}, self.variation_name_control)
        self.assertIsNone(result)

    def test_get_campaign_variation_wrong_variation_passed(self):
        result = campaign_util.get_campaign_variation(self.dummy_campaign, "SOME_VARIATION")
        self.assertIsNone(result)

    def test_get_campaign_variation_none_campaign_passed(self):
        result = campaign_util.get_campaign_variation({}, self.variation_name_control)
        self.assertIsNone(result)

    def test_get_campaign_variation_none_goal_passed(self):
        result = campaign_util.get_campaign_variation(self.dummy_campaign, None)
        self.assertIsNone(result)

    def test_get_control_variation_return_none(self):
        self.dummy_campaign["variations"][0]["id"] = "3"
        result = campaign_util.get_control_variation(self.dummy_campaign)
        self.assertIsNone(result)
        self.dummy_campaign["variations"][0]["id"] = "1"

    def test_scale_variations_50_to_100(self):
        variations = [{"weight": 50}]
        campaign_util.scale_variations(variations)
        self.assertEquals(variations[0]["weight"], 100)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_90_to_100(self):
        variations = [{"weight": 90}]
        campaign_util.scale_variations(variations)
        self.assertEquals(variations[0]["weight"], 100)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_10_90_to_10_90(self):
        variations = [{"weight": 10}, {"weight": 90}]
        campaign_util.scale_variations(variations)
        self.assertEquals(variations[0]["weight"], 10)
        self.assertEquals(variations[1]["weight"], 90)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_50_50_to_50_50(self):
        variations = [{"weight": 50}, {"weight": 50}]
        campaign_util.scale_variations(variations)
        self.assertEquals(variations[0]["weight"], 50)
        self.assertEquals(variations[1]["weight"], 50)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_10_40_to_20_80(self):
        variations = [{"weight": 10}, {"weight": 40}]
        campaign_util.scale_variations(variations)
        self.assertEquals(variations[0]["weight"], 20)
        self.assertEquals(variations[1]["weight"], 80)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_1_2_to_20_80(self):
        variations = [{"weight": 1}, {"weight": 2}]
        campaign_util.scale_variations(variations)
        self.assertAlmostEquals(variations[0]["weight"], 33.333333333)
        self.assertAlmostEquals(variations[1]["weight"], 66.666666666)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_1_2_3_4_to_10_20_30_40(self):
        variations = [{"weight": 1}, {"weight": 2}, {"weight": 3}, {"weight": 4}]
        campaign_util.scale_variations(variations)
        self.assertEquals(variations[0]["weight"], 10)
        self.assertEquals(variations[1]["weight"], 20)
        self.assertEquals(variations[2]["weight"], 30)
        self.assertEquals(variations[3]["weight"], 40)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_get_allocation_ranges_33_33_33(self):
        variations = [
            {
                "id": 1,
                "name": "Control",
                "changes": {},
                "weight": 33.3333,
                "segments": {"or": [{"custom_variable": {"safari": "true"}}]},
            },
            {
                "id": 2,
                "name": "Variation-1",
                "changes": {},
                "weight": 33.3333,
                "segments": {"or": [{"custom_variable": {"browser": "wildcard(chrome*)"}}]},
            },
            {
                "id": 3,
                "name": "Variation-2",
                "changes": {},
                "weight": 33.3333,
                "segments": {"or": [{"custom_variable": {"chrome": "false"}}]},
            },
        ]
        variation_allocations_ranges_list = campaign_util.get_allocation_ranges(variations)
        self.assertEquals(variation_allocations_ranges_list[0], (1, 3334))
        self.assertEquals(variation_allocations_ranges_list[1], (3335, 6668))
        self.assertEquals(variation_allocations_ranges_list[2], (6669, 10002))

    def test_get_allocation_ranges_10_20_30_40(self):
        items = [{"weight": 10}, {"weight": 20}, {"weight": 30}, {"weight": 40}]
        variation_allocations_ranges_list = campaign_util.get_allocation_ranges(items)
        self.assertEquals(variation_allocations_ranges_list[0], (1, 1000))
        self.assertEquals(variation_allocations_ranges_list[1], (1001, 3000))
        self.assertEquals(variation_allocations_ranges_list[2], (3001, 6000))
        self.assertEquals(variation_allocations_ranges_list[3], (6001, 10000))

    def test_get_allocation_ranges_13_87(self):
        items = [{"weight": 13}, {"weight": 87}]
        variation_allocations_ranges_list = campaign_util.get_allocation_ranges(items)
        self.assertEquals(variation_allocations_ranges_list[0], (1, 1300))
        self.assertEquals(variation_allocations_ranges_list[1], (1301, 10000))

    def test_get_allocation_ranges_1_99(self):
        items = [{"weight": 1}, {"weight": 99}]
        variation_allocations_ranges_list = campaign_util.get_allocation_ranges(items)
        self.assertEquals(variation_allocations_ranges_list[0], (1, 100))
        self.assertEquals(variation_allocations_ranges_list[1], (101, 10000))

    def test_get_allocation_ranges_99_1(self):
        items = [{"weight": 99}, {"weight": 1}]
        variation_allocations_ranges_list = campaign_util.get_allocation_ranges(items)
        self.assertEquals(variation_allocations_ranges_list[0], (1, 9900))
        self.assertEquals(variation_allocations_ranges_list[1], (9901, 10000))

    def test_get_allocation_ranges_0pt1_99pt9(self):
        items = [{"weight": 0.1}, {"weight": 99.9}]
        variation_allocations_ranges_list = campaign_util.get_allocation_ranges(items)
        self.assertEquals(variation_allocations_ranges_list[0], (1, 10))
        self.assertEquals(variation_allocations_ranges_list[1], (11, 10000))

    def test_get_allocation_ranges_0pt01_99pt99(self):
        items = [{"weight": 0.01}, {"weight": 99.99}]
        variation_allocations_ranges_list = campaign_util.get_allocation_ranges(items)
        self.assertEquals(variation_allocations_ranges_list[0], (1, 1))
        self.assertEquals(variation_allocations_ranges_list[1], (2, 10000))

    def test_get_allocation_ranges_0pt001_99pt999(self):
        items = [{"weight": 0.001}, {"weight": 99.999}]
        variation_allocations_ranges_list = campaign_util.get_allocation_ranges(items)
        self.assertEquals(variation_allocations_ranges_list[0], (1, 1))
        self.assertEquals(variation_allocations_ranges_list[1], (2, 10001))

    def test_get_bucketing_range_10(self):
        result = campaign_util._get_bucketing_range(10)
        self.assertEquals(result, 1000)

    def test_get_bucketing_range_1(self):
        result = campaign_util._get_bucketing_range(1)
        self.assertEquals(result, 100)

    def test_get_bucketing_range_1pt_11(self):
        result = campaign_util._get_bucketing_range(1.11)
        self.assertEquals(result, 112)

    def test_get_bucketing_range_99pt99(self):
        result = campaign_util._get_bucketing_range(99.99)
        self.assertEquals(result, 9999)

    def test_get_bucketing_range_205pont9999(self):
        result = campaign_util._get_bucketing_range(205.9999)
        self.assertEquals(result, 10000)

    def test_get_bucketing_range_0(self):
        result = campaign_util._get_bucketing_range(0)
        self.assertEquals(result, 0)

    def test_get_bucketing_range_0pt1(self):
        result = campaign_util._get_bucketing_range(0.1)
        self.assertEquals(result, 10)

    def test_get_bucketing_range_0pt11(self):
        result = campaign_util._get_bucketing_range(0.11)
        self.assertEquals(result, 11)

    def test_get_bucketing_range_0pt111(self):
        result = campaign_util._get_bucketing_range(0.111)
        self.assertEquals(result, 12)

    def test_get_bucketing_range_0pt1111(self):
        result = campaign_util._get_bucketing_range(0.1111)
        self.assertEquals(result, 12)

    def test_scale_variations_0_weight(self):
        variations = [{"weight": 0}]
        campaign_util.scale_variations(variations)
        self.assertEquals(variations[0]["weight"], 100)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_0_0_1_weight(self):
        variations = [{"weight": 0}, {"weight": 0}, {"weight": 1}]
        campaign_util.scale_variations(variations)
        self.assertEquals(variations[0]["weight"], 0)
        self.assertEquals(variations[1]["weight"], 0)
        self.assertEquals(variations[2]["weight"], 100)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_0_0_weight(self):
        variations = [{"weight": 0}, {"weight": 0}]
        campaign_util.scale_variations(variations)
        self.assertEquals(variations[0]["weight"], 50)
        self.assertEquals(variations[1]["weight"], 50)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_0pt1_weight(self):
        variations = [{"weight": 0.1}]
        campaign_util.scale_variations(variations)
        self.assertEquals(variations[0]["weight"], 100)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_0pt1_0pt1_0pt1_weight(self):
        variations = [{"weight": 0.1}, {"weight": 0.1}, {"weight": 0.1}]
        campaign_util.scale_variations(variations)
        self.assertAlmostEquals(variations[0]["weight"], 33.3333333)
        self.assertAlmostEquals(variations[1]["weight"], 33.3333333)
        self.assertAlmostEquals(variations[2]["weight"], 33.3333333)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_0pt01_0pt01_0pt01_weight(self):
        variations = [{"weight": 0.01}, {"weight": 0.01}, {"weight": 0.01}]
        campaign_util.scale_variations(variations)
        self.assertAlmostEquals(variations[0]["weight"], 33.3333333)
        self.assertAlmostEquals(variations[1]["weight"], 33.3333333)
        self.assertAlmostEquals(variations[2]["weight"], 33.3333333)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_0pt001_0pt01_0pt1_weight(self):
        variations = [{"weight": 0.001}, {"weight": 0.01}, {"weight": 0.1}]
        campaign_util.scale_variations(variations)
        self.assertAlmostEquals(variations[0]["weight"], 0.9009009009009009)
        self.assertAlmostEquals(variations[1]["weight"], 9.00900900900901)
        self.assertAlmostEquals(variations[2]["weight"], 90.09009009009009)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_10pt234_33pt456_44pt444_weight(self):
        variations = [{"weight": 10.234}, {"weight": 33.456}, {"weight": 44.444}]
        campaign_util.scale_variations(variations)
        self.assertAlmostEquals(variations[0]["weight"], 11.611863752921685)
        self.assertAlmostEquals(variations[1]["weight"], 37.96037851453468)
        self.assertAlmostEquals(variations[2]["weight"], 50.42775773254362)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_10pt234_33pt456_44pt444_0ppt1_0pt_1weight(self):
        variations = [{"weight": 10.234}, {"weight": 33.456}, {"weight": 44.444}, {"weight": 0.1}, {"weight": 0.1}]
        campaign_util.scale_variations(variations)
        self.assertAlmostEquals(variations[0]["weight"], 11.585572939072158)
        self.assertAlmostEquals(variations[1]["weight"], 37.874431136368784)
        self.assertAlmostEquals(variations[2]["weight"], 50.313582538999704)
        self.assertAlmostEquals(variations[3]["weight"], 0.11320669277967714)
        self.assertAlmostEquals(variations[4]["weight"], 0.11320669277967714)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_scale_variations_1pt123435_20pt7623_60_5pt123123_2pt12342_2pt24234_8pt213weight(self):
        variations = [
            {"weight": 1.123435},
            {"weight": 20.7623},
            {"weight": 60},
            {"weight": 5.123123},
            {"weight": 2.12342},
            {"weight": 2.24234},
            {"weight": 8.213},
        ]
        campaign_util.scale_variations(variations)
        self.assertAlmostEquals(variations[0]["weight"], 1.1280870278471768)
        self.assertAlmostEquals(variations[1]["weight"], 20.848274531478403)
        self.assertAlmostEquals(variations[2]["weight"], 60.24845377866153)
        self.assertAlmostEquals(variations[3]["weight"], 5.144337321131629)
        self.assertAlmostEquals(variations[4]["weight"], 2.1322128620447574)
        self.assertAlmostEquals(variations[5]["weight"], 2.2516252974340647)
        self.assertAlmostEquals(variations[6]["weight"], 8.24700918140245)
        self.assertAlmostEqual(100, sum(variation["weight"] for variation in variations))

    def test_set_variation_allocation(self):
        campaign = SETTINGS_FILES.get("FT_T_0_W_10_20_30_40")["campaigns"][0]
        campaign_util.set_variation_allocation(campaign)
        variation_allocation_ranges_list = campaign_util.get_allocation_ranges(campaign.get("variations"))
        for i, variation in enumerate(campaign.get("variations")):
            self.assertEquals(variation.get("allocation_range_start"), variation_allocation_ranges_list[i][0])
            self.assertEquals(variation.get("allocation_range_end"), variation_allocation_ranges_list[i][1])

    def test_is_part_of_group(self):
        settings_file = mutually_exclusive_test_cases.get("commonSettingsFile")
        self.assertEqual(campaign_util.is_part_of_group(settings_file, 1), True)
        self.assertEqual(campaign_util.is_part_of_group(settings_file, 5), False)

    def test_get_group_campaigns(self):
        settings_file = mutually_exclusive_test_cases.get("commonSettingsFile")

        campaigns = [settings_file["campaigns"][0], settings_file["campaigns"][1], settings_file["campaigns"][2]]
        self.assertListEqual(campaign_util.get_group_campaigns(settings_file, 1), campaigns)

    def test_get_group_campaigns_invalid_group_id(self):
        settings_file = mutually_exclusive_test_cases.get("commonSettingsFile")
        self.assertListEqual(campaign_util.get_group_campaigns(settings_file, -1), [])
