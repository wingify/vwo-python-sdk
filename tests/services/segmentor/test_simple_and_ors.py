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


class TestSimpleAndOrs(unittest.TestCase):
    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()
        self.test_cases = segmentor_test_cases.get("simple_and_ors")

    def test_single_not_true(self):
        test_case = self.test_cases.get("single_not_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_chain_of_and_nullify_not_true(self):
        test_case = self.test_cases.get("chain_of_and_nullify_not_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_lower_true(self):
        test_case = self.test_cases.get("dsl_lower_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_regex_true(self):
        test_case = self.test_cases.get("dsl_regex_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_chain_of_not_5_false(self):
        test_case = self.test_cases.get("chain_of_not_5_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_lower_false(self):
        test_case = self.test_cases.get("dsl_lower_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_regex_false(self):
        test_case = self.test_cases.get("dsl_regex_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_chain_of_not_4_true(self):
        test_case = self.test_cases.get("chain_of_not_4_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_eq_false(self):
        test_case = self.test_cases.get("dsl_eq_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_single_not_false(self):
        test_case = self.test_cases.get("single_not_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_chain_of_or_nullify_not_true(self):
        test_case = self.test_cases.get("chain_of_or_nullify_not_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_wildcard_true_front_back_middle_star(self):
        test_case = self.test_cases.get("dsl_wildcard_true_front_back_middle_star")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_chain_of_or_middle_not_false(self):
        test_case = self.test_cases.get("chain_of_or_middle_not_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_chain_of_not_4_false(self):
        test_case = self.test_cases.get("chain_of_not_4_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_wildcard_true_back(self):
        test_case = self.test_cases.get("dsl_wildcard_true_back")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_single_or_true(self):
        test_case = self.test_cases.get("single_or_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_or_true(self):
        test_case = self.test_cases.get("multiple_or_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_wildcard_true_front(self):
        test_case = self.test_cases.get("dsl_wildcard_true_front")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_wildcard_false(self):
        test_case = self.test_cases.get("dsl_wildcard_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_chain_of_and_true(self):
        test_case = self.test_cases.get("chain_of_and_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_chain_of_and_middle_not_false(self):
        test_case = self.test_cases.get("chain_of_and_middle_not_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_single_or_false(self):
        test_case = self.test_cases.get("single_or_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_eq_true(self):
        test_case = self.test_cases.get("dsl_eq_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_and_true(self):
        test_case = self.test_cases.get("multiple_and_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_chain_of_not_5_true(self):
        test_case = self.test_cases.get("chain_of_not_5_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_or_false(self):
        test_case = self.test_cases.get("multiple_or_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_single_and_true(self):
        test_case = self.test_cases.get("single_and_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_multiple_and_false(self):
        test_case = self.test_cases.get("multiple_and_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_wildcard_true_front_back(self):
        test_case = self.test_cases.get("dsl_wildcard_true_front_back")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_chain_of_or_true(self):
        test_case = self.test_cases.get("chain_of_or_true")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_dsl_wildcard_false_front_back_middle_star(self):
        test_case = self.test_cases.get("dsl_wildcard_false_front_back_middle_star")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_single_and_false(self):
        test_case = self.test_cases.get("single_and_false")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )
