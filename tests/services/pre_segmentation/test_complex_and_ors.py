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


class TestComplexAndOrs(unittest.TestCase):

    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()

    def test_complex_dsl_1(self):
        dsl = \
            '{"or":[{"or":[{"and":[{"or":[{"custom_variable":{"start_with":"wildcard(my_start_with_val*)"}}]},{"not":{"or":[{"custom_variable":{"neq":"not_eq_value"}}]}}]},{"or":[{"custom_variable":{"contain":"wildcard(*my_contain_val*)"}}]}]},{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}]}'
        custom_variables = {
            'reg': 1,
            'contain': 1,
            'eq': 1,
            'start_with': 'my_start_with_valzzzzzzzzzzzzzzzz',
            'neq': 1,
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_complex_dsl_2(self):
        dsl = \
            '{"or":[{"or":[{"and":[{"or":[{"custom_variable":{"start_with":"wildcard(my_start_with_val*)"}}]},{"not":{"or":[{"custom_variable":{"neq":"not_eq_value"}}]}}]},{"or":[{"custom_variable":{"contain":"wildcard(*my_contain_val*)"}}]}]},{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}]}'
        custom_variables = {
            'reg': 1,
            'contain': 1,
            'eq': 1,
            'start_with': 1,
            'neq': 'not_eq_value',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_complex_dsl_3(self):
        dsl = \
            '{"or":[{"or":[{"and":[{"or":[{"custom_variable":{"start_with":"wildcard(my_start_with_val*)"}}]},{"not":{"or":[{"custom_variable":{"neq":"not_eq_value"}}]}}]},{"or":[{"custom_variable":{"contain":"wildcard(*my_contain_val*)"}}]}]},{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}]}'
        custom_variables = {
            'reg': 1,
            'contain': 'zzzzzzmy_contain_valzzzzz',
            'eq': 1,
            'start_with': 'm1y_1sta1rt_with_val',
            'neq': False,
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_complex_dsl_4(self):
        dsl = \
            '{"or":[{"or":[{"and":[{"or":[{"custom_variable":{"start_with":"wildcard(my_start_with_val*)"}}]},{"not":{"or":[{"custom_variable":{"neq":"not_eq_value"}}]}}]},{"or":[{"custom_variable":{"contain":"wildcard(*my_contain_val*)"}}]}]},{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}]}'
        custom_variables = {
            'reg': 1,
            'contain': 'my_ contain _val',
            'eq': 'eq_value',
            'start_with': 'm1y_1sta1rt_with_val',
            'neq': None,
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_complex_dsl_5(self):
        dsl = \
            '{"or":[{"or":[{"and":[{"or":[{"custom_variable":{"start_with":"wildcard(my_start_with_val*)"}}]},{"not":{"or":[{"custom_variable":{"neq":"not_eq_value"}}]}}]},{"or":[{"custom_variable":{"contain":"wildcard(*my_contain_val*)"}}]}]},{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}]}'
        custom_variables = {
            'reg': 'myregexxxxxx',
            'contain': 'my_ contain _val',
            'eq': 'eq__value',
            'start_with': 'm1y_1sta1rt_with_val',
            'neq': 123,
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_complex_dsl_6(self):
        dsl = \
            '{"or":[{"or":[{"and":[{"or":[{"custom_variable":{"start_with":"wildcard(my_start_with_val*)"}}]},{"not":{"or":[{"custom_variable":{"neq":"not_eq_value"}}]}}]},{"or":[{"custom_variable":{"contain":"wildcard(*my_contain_val*)"}}]}]},{"and":[{"or":[{"custom_variable":{"eq":"eq_value"}}]},{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}]}]}'
        custom_variables = {
            'reg': 'myregexxxxxx',
            'contain': 'my$contain$val',
            'eq': 'eq_value',
            'start_with': 'm1y_1sta1rt_with_val',
            'neq': 'not_matching',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)
