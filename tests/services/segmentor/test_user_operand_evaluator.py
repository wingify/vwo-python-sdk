# Copyright 2019-2020 Wingify Software Pvt. Ltd.
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


class TestUserOperandEvaluator(unittest.TestCase):
    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()
        self.test_cases = segmentor_test_cases.get("user_operand_evaluator")

    def test_single_equal_return_true(self):
        test_case = self.test_cases.get("single_equal_return_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_single_equal_return_false(self):
        test_case = self.test_cases.get("single_equal_return_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_equal_return_true(self):
        test_case = self.test_cases.get("multiple_equal_return_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_equal_return_false(self):
        test_case = self.test_cases.get("multiple_equal_return_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_single_not_equal_return_true(self):
        test_case = self.test_cases.get("single_not_equal_return_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_single_not_equal_return_false(self):
        test_case = self.test_cases.get("single_not_equal_return_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_not_equal_return_true(self):
        test_case = self.test_cases.get("multiple_not_equal_return_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_not_equal_return_false(self):
        test_case = self.test_cases.get("multiple_not_equal_return_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_single_not_equal_return_true_uneven_spaces(self):
        test_case = self.test_cases.get("single_not_equal_return_true_uneven_spaces")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_single_not_equal_return_false_uneven_spaces(self):
        test_case = self.test_cases.get("single_not_equal_return_false_uneven_spaces")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_not_equal_return_true_uneven_spaces(self):
        test_case = self.test_cases.get("multiple_not_equal_return_true_uneven_spaces")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_not_equal_return_false_uneven_spaces(self):
        test_case = self.test_cases.get("multiple_not_equal_return_false_uneven_spaces")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_single_not_equal_return_true_spaces_in_user_id(self):
        test_case = self.test_cases.get("single_not_equal_return_true_spaces_in_user_id")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_single_not_equal_return_false_spaces_in_user_id(self):
        test_case = self.test_cases.get("single_not_equal_return_false_spaces_in_user_id")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_not_equal_return_true_spaces_in_user_id(self):
        test_case = self.test_cases.get("multiple_not_equal_return_true_spaces_in_user_id")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_not_equal_return_false_spaces_in_user_id(self):
        test_case = self.test_cases.get("multiple_not_equal_return_false_spaces_in_user_id")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("variation_targeting_variables")),
            test_case.get("expectation"),
        )
