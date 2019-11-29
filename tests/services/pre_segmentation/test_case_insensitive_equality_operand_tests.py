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


class TestCaseInsensitiveEqualityOperandTests(unittest.TestCase):

    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()

    def something(self):
        pass

    def test_exact_match_with_special_characters_test(self):
        dsl = \
            '{"or":[{"custom_variable":{"eq":"lower(f25u!v@b#k$6%9^f&o*v(m)w_-=+s,./`(*&^%$#@!)"}}]}'
        custom_variables = {'eq': 'f25u!v@b#k$6%9^f&o*v(m)w_-=+s,./`(*&^%$#@!'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_float_data_type_mismatch_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(123.456)"}}]}'
        custom_variables = {'eq': 123}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_numeric_data_type_mismatch_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(123)"}}]}'
        custom_variables = {'eq': 12}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_float_data_type_mismatch_test2(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(123.456)"}}]}'
        custom_variables = {'eq': 123.4567}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_incorrect_key_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(something)"}}]}'
        custom_variables = {'neq': 'something'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_incorrect_key_case_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(something)"}}]}'
        custom_variables = {'EQ': 'something'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_single_char_test(self):
        dsl = \
            '{"or":[{"custom_variable":{"eq":"lower(zzsomethingzz)"}}]}'
        custom_variables = {'eq': 'i'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_char_data_type_case_mismatch_test2(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(e)"}}]}'
        custom_variables = {'eq': 'E'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_case_mismatch_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(something)"}}]}'
        custom_variables = {'eq': 'Something'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_exact_match_with_spaces_test(self):
        dsl = \
            '{"or":[{"custom_variable":{"eq":"lower(nice to see you. will    YOU be   my        Friend?)"}}]}'
        custom_variables = \
            {'eq': 'nice to see you. will    YOU be   my        Friend?'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_stringified_float_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(123.456)"}}]}'
        custom_variables = {'eq': '123.456000000'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_char_data_type_case_mismatch_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(E)"}}]}'
        custom_variables = {'eq': 'e'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_char_data_type_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(E)"}}]}'
        custom_variables = {'eq': 'E'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_boolean_data_type_mismatch_test2(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(true)"}}]}'
        custom_variables = {'eq': False}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_boolean_data_type_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(true)"}}]}'
        custom_variables = {'eq': True}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_numeric_data_type_mismatch_test2(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(123)"}}]}'
        custom_variables = {'eq': 123.0}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_mismatch_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(something)"}}]}'
        custom_variables = {'eq': 'notsomething'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_numeric_data_type_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(123)"}}]}'
        custom_variables = {'eq': 123}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_exact_match_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(something)"}}]}'
        custom_variables = {'eq': 'something'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_part_of_text_test(self):
        dsl = \
            '{"or":[{"custom_variable":{"eq":"lower(zzsomethingzz)"}}]}'
        custom_variables = {'eq': 'something'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_exact_match_with_upper_case_test(self):
        dsl = \
            '{"or":[{"custom_variable":{"eq":"lower(HgUvshFRjsbTnvsdiUFFTGHFHGvDRT.YGHGH)"}}]}'
        custom_variables = {'eq': 'HgUvshFRjsbTnvsdiUFFTGHFHGvDRT.YGHGH'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_null_value_provided_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(something)"}}]}'
        custom_variables = {'eq': None}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_boolean_data_type_mismatch_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(false)"}}]}'
        custom_variables = {'eq': True}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_no_value_provided_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(something)"}}]}'
        custom_variables = {'eq': ''}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_missingkey_value_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(something)"}}]}'
        custom_variables = {}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_stringified_float_test3(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(123.4560000)"}}]}'
        custom_variables = {'eq': 123.456}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_stringified_float_test2(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(123.0)"}}]}'
        custom_variables = {'eq': 123}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_case_mismatch_test2(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(something)"}}]}'
        custom_variables = {'eq': 'SOMETHINg'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_float_data_type_extra_decimal_zeros_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(123.456)"}}]}'
        custom_variables = {'eq': 123.456}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_boolean_data_type_test3(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(True)"}}]}'
        custom_variables = {'eq': True}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_boolean_data_type_test2(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(false)"}}]}'
        custom_variables = {'eq': False}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_float_data_type_test(self):
        dsl = '{"or":[{"custom_variable":{"eq":"lower(123.456)"}}]}'
        custom_variables = {'eq': 123.456}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)
