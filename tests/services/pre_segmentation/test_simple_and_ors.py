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


class TestSimpleAndOrs(unittest.TestCase):

    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()

    def test_test_single_not_true(self):
        dsl = \
            '{"not":{"or":[{"custom_variable":{"neq":"not_eq_value"}}]}}'
        custom_variables = {'neq': 'eq_valaue'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_chain_of_and_nullify_not_true(self):
        dsl = \
            '{"and":[{"not":{"and":[{"not":{"and":[{"custom_variable":{"eq":"eq_value"}}]}}]}}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_dsl_lower_true(self):
        dsl = '{"or":[{"custom_variable":{"a":"lower(something)"}}]}'
        custom_variables = {'a': 'SoMeThIng'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_dsl_regex_true(self):
        dsl = '{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}'
        custom_variables = {'reg': 'myregexxxxxx'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_chain_of_not_5_false(self):
        dsl = \
            '{"not":{"or":[{"not":{"or":[{"not":{"or":[{"not":{"or":[{"not":{"or":[{"custom_variable":{"neq":"eq_value"}}]}}]}}]}}]}}]}}'
        custom_variables = {'neq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_dsl_lower_false(self):
        dsl = '{"or":[{"custom_variable":{"a":"lower(something)"}}]}'
        custom_variables = {'a': 'SoMeThIngS'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_dsl_regex_false(self):
        dsl = '{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}'
        custom_variables = {'reg': 'myregeXxxxxx'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_chain_of_not_4_true(self):
        dsl = \
            '{"not":{"or":[{"not":{"or":[{"not":{"or":[{"not":{"or":[{"custom_variable":{"neq":"eq_value"}}]}}]}}]}}]}}'
        custom_variables = {'neq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_dsl_eq_false(self):
        dsl = '{"not":{"or":[{"custom_variable":{"a":"something"}}]}}'
        custom_variables = {'a': 'something'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_single_not_false(self):
        dsl = \
            '{"not":{"or":[{"custom_variable":{"neq":"not_eq_value"}}]}}'
        custom_variables = {'neq': 'not_eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_chain_of_or_nullify_not_true(self):
        dsl = \
            '{"or":[{"not":{"or":[{"not":{"or":[{"custom_variable":{"eq":"eq_value"}}]}}]}}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_dsl_wildcard_true_front_back_middle_star(self):
        dsl = \
            '{"or":[{"custom_variable":{"a":"wildcard(*some*thing*)"}}]}'
        custom_variables = {'a': 'hellosome*thingworld'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_chain_of_or_middle_not_false(self):
        dsl = \
            '{"or":[{"or":[{"not":{"or":[{"or":[{"custom_variable":{"eq":"eq_value"}}]}]}}]}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_chain_of_not_4_false(self):
        dsl = \
            '{"not":{"or":[{"not":{"or":[{"not":{"or":[{"not":{"or":[{"custom_variable":{"neq":"not_eq_value"}}]}}]}}]}}]}}'
        custom_variables = {'neq': 'eq_valaue'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_dsl_wildcard_true_back(self):
        dsl = \
            '{"or":[{"custom_variable":{"a":"wildcard(something*)"}}]}'
        custom_variables = {'a': 'somethingworld'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_single_or_true(self):
        dsl = '{"or":[{"custom_variable":{"eq":"eq_value"}}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_multiple_or_true(self):
        dsl = \
            '{"or":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}'
        custom_variables = {'eq': 'eq_value', 'reg': 'myregeXxxxxx'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_dsl_wildcard_true_front(self):
        dsl = \
            '{"or":[{"custom_variable":{"a":"wildcard(*something)"}}]}'
        custom_variables = {'a': 'hellosomething'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_dsl_wildcard_false(self):
        dsl = \
            '{"or":[{"custom_variable":{"a":"wildcard(*something)"}}]}'
        custom_variables = {'a': 'somethin'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_chain_of_and_true(self):
        dsl = \
            '{"and":[{"and":[{"and":[{"and":[{"and":[{"custom_variable":{"eq":"eq_value"}}]}]}]}]}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_chain_of_and_middle_not_false(self):
        dsl = \
            '{"and":[{"and":[{"not":{"and":[{"and":[{"custom_variable":{"eq":"eq_value"}}]}]}}]}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_single_or_false(self):
        dsl = '{"or":[{"custom_variable":{"eq":"n_eq_value"}}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_dsl_eq_true(self):
        dsl = '{"or":[{"custom_variable":{"a":"something"}}]}'
        custom_variables = {'a': 'something'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_multiple_and_true(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}'
        custom_variables = {'eq': 'eq_value', 'reg': 'myregexxxxxx'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_chain_of_not_5_true(self):
        dsl = \
            '{"not":{"or":[{"not":{"or":[{"not":{"or":[{"not":{"or":[{"not":{"or":[{"custom_variable":{"neq":"neq_value"}}]}}]}}]}}]}}]}}'
        custom_variables = {'neq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_multiple_or_false(self):
        dsl = \
            '{"or":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}'
        custom_variables = {'eq': 'eq_values', 'reg': 'myregeXxxxxx'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_single_and_true(self):
        dsl = '{"and":[{"custom_variable":{"eq":"eq_value"}}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_multiple_and_false(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}'
        custom_variables = {'eq': 'eq_value', 'reg': 'myregeXxxxxx'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_dsl_wildcard_true_front_back(self):
        dsl = \
            '{"or":[{"custom_variable":{"a":"wildcard(*something*)"}}]}'
        custom_variables = {'a': 'hellosomethingworld'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_chain_of_or_true(self):
        dsl = \
            '{"or":[{"or":[{"or":[{"or":[{"or":[{"custom_variable":{"eq":"eq_value"}}]}]}]}]}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_test_dsl_wildcard_false_front_back_middle_star(self):
        dsl = \
            '{"or":[{"custom_variable":{"a":"wildcard(*some*thing*)"}}]}'
        custom_variables = {'a': 'hellosomethingworld'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_test_single_and_false(self):
        dsl = '{"and":[{"custom_variable":{"eq":"n_eq_value"}}]}'
        custom_variables = {'eq': 'eq_value'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)
