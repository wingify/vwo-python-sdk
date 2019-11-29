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


class TestNewCasesForDecimalMismatch(unittest.TestCase):

    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()

    def test_endswith_decimal(self):
        dsl = '{"or":[{"custom_variable":{"val":"wildcard(*123)"}}]}'
        custom_variables = {'val': 765123.0}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_contains_decimal2(self):
        dsl = '{"or":[{"custom_variable":{"val":"wildcard(*123.0*)"}}]}'
        custom_variables = {'val': 876123}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_contains_decimal(self):
        dsl = '{"or":[{"custom_variable":{"val":"wildcard(*123*)"}}]}'
        custom_variables = {'val': 654123.2323}
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)
