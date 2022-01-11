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
import json
from vwo.services.segmentor.segment_evaluator import SegmentEvaluator

with open("tests/data/segmentor_test_cases.json") as json_file:
    segmentor_test_cases = json.load(json_file)


class TestUserOperandEvaluatorWithCustomVariables(unittest.TestCase):
    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()
        self.test_cases = segmentor_test_cases.get("user_operand_evaluator_with_custom_variables")

    def test_targeting_safari_returns_true(self):
        test_case = self.test_cases.get("targeting_safari_returns_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_targeting_safari_returns_false(self):
        test_case = self.test_cases.get("targeting_safari_returns_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_targeting_only_safari_for_user_1_returns_true(self):
        test_case = self.test_cases.get("targeting_only_safari_for_user_1_returns_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_targeting_only_safari_for_user_1_returns_false(self):
        test_case = self.test_cases.get("targeting_only_safari_for_user_1_returns_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_targeting_chrome_all_version_with_black_listing_multiple_users_returns_true(self):
        test_case = self.test_cases.get("targeting_chrome_all_version_with_black_listing_multiple_users_returns_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_targeting_chrome_any_version_with_multiple_users_returns_true(self):
        test_case = self.test_cases.get("targeting_chrome_any_version_with_multiple_users_returns_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_targeting_chrome_all_version_with_black_listing_multiple_users_returns_false(self):
        test_case = self.test_cases.get("targeting_chrome_all_version_with_black_listing_multiple_users_returns_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_targeting_chrome_any_version_with_multiple_users_returns_false(self):
        test_case = self.test_cases.get("targeting_chrome_any_version_with_multiple_users_returns_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_black_listing_scrambled_user_using_safari_return_false(self):
        test_case = self.test_cases.get("black_listing_scrambled_user_using_safari_return_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_black_listing_scrambled_user_using_safari_return_true_for_space_difference(self):
        test_case = self.test_cases.get("black_listing_scrambled_user_using_safari_return_true_for_space_difference")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )
