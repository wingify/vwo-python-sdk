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


class TestRegex(unittest.TestCase):
    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()
        self.test_cases = segmentor_test_cases.get("regex")

    def test_regex_operand_mismatch2(self):
        test_case = self.test_cases.get("regex_operand_mismatch2")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_regex_operand2(self):
        test_case = self.test_cases.get("regex_operand2")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_invalid_regex(self):
        test_case = self.test_cases.get("invalid_regex")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_invalid_regex2(self):
        test_case = self.test_cases.get("invalid_regex2")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_regex_operand_case_mismatch(self):
        test_case = self.test_cases.get("regex_operand_case_mismatch")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )

    def test_regex_operand(self):
        test_case = self.test_cases.get("regex_operand")
        self.assertIs(
            self.segment_evaluator.evaluate(test_case.get("dsl"), test_case.get("custom_variables")),
            test_case.get("expectation"),
        )
