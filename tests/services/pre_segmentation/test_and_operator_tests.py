# Copyright 2019 Wingify Software Pvt. Ltd.
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


class TestAndOperatorTests(unittest.TestCase):

    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()

    def test_single_and_operator_matching_test(self):
        dsl = '{"and":[{"custom_variable":{"eq":"eq_value"}}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_single_and_operator_case_mismatch_test(self):
        dsl = '{"and":[{"custom_variable":{"eq":"eq_value"}}]}'
        custom_variables = {'eq': 'Eq_Value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_multiple_and_operator_test2(self):
        dsl = \
            '{"and":[{"and":[{"and":[{"and":[{"and":[{"custom_variable":{"eq":"eq_value"}}]}]}]}]}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_multiple_and_operator_with_all_incorrect_correct_values_test(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}'
        custom_variables = {'eq': 'wrong', 'reg': 'wrong'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_multiple_and_operator_with_single_correct_value_test2(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}'
        custom_variables = {'eq': 'wrong', 'reg': 'myregexxxxxx'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_multiple_and_operator_with_all_correct_values_test(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}'
        custom_variables = {'eq': 'eq_value', 'reg': 'myregexxxxxx'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_single_and_operator_mismatch_test(self):
        dsl = '{"and":[{"custom_variable":{"eq":"eq_value"}}]}'
        custom_variables = {'a': 'n_eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_multiple_and_operator_with_single_correct_value_test(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}'
        custom_variables = {'eq': 'eq_value', 'reg': 'wrong'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)
