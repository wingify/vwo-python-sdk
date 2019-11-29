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


class TestRegexTests(unittest.TestCase):

    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()

    def test_regex_operand_mismatch_test2(self):
        dsl = \
            '{"or":[{"custom_variable":{"reg":"regex(<(W[^>]*)(.*?)>)"}}]}'
        custom_variables = {'reg': '<wingifySDK id=1></wingifySDK>'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_regex_operand_test2(self):
        dsl = \
            '{"or":[{"custom_variable":{"reg":"regex(<(W[^>]*)(.*?)>)"}}]}'
        custom_variables = {'reg': '<WingifySDK id=1></WingifySDK>'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_invalid_reqex_test(self):
        dsl = '{"or":[{"custom_variable":{"reg":"regex(*)"}}]}'
        custom_variables = {'reg': '*'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_invalid_reqex_test2(self):
        dsl = '{"or":[{"custom_variable":{"reg":"regex(*)"}}]}'
        custom_variables = {'reg': 'asdf'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_regex_operand_case_mismatch_test(self):
        dsl = '{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}'
        custom_variables = {'reg': 'myregeXxxxxx'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_regex_operand_test(self):
        dsl = '{"or":[{"custom_variable":{"reg":"regex(myregex+)"}}]}'
        custom_variables = {'reg': 'myregexxxxxx'}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)
