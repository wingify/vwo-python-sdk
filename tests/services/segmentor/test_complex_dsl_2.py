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
with open('tests/data/segmentor_test_cases.json') as json_file:
    segmentor_test_cases = json.load(json_file)


class TestComplexDsl2(unittest.TestCase):

    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()
        self.test_cases = segmentor_test_cases.get('complex_dsl_2')

    def test_false4(self):
        test_case = self.test_cases.get('false4')
        self.assertIs(self.segment_evaluator.evaluate(test_case.get('dsl'),
                      test_case.get('custom_variables')), test_case.get('expectation'))

    def test_false1(self):
        test_case = self.test_cases.get('false1')
        self.assertIs(self.segment_evaluator.evaluate(test_case.get('dsl'),
                      test_case.get('custom_variables')), test_case.get('expectation'))

    def test_false3(self):
        test_case = self.test_cases.get('false3')
        self.assertIs(self.segment_evaluator.evaluate(test_case.get('dsl'),
                      test_case.get('custom_variables')), test_case.get('expectation'))

    def test_false2(self):
        test_case = self.test_cases.get('false2')
        self.assertIs(self.segment_evaluator.evaluate(test_case.get('dsl'),
                      test_case.get('custom_variables')), test_case.get('expectation'))

    def test_true4(self):
        test_case = self.test_cases.get('true4')
        self.assertIs(self.segment_evaluator.evaluate(test_case.get('dsl'),
                      test_case.get('custom_variables')), test_case.get('expectation'))

    def test_true1(self):
        test_case = self.test_cases.get('true1')
        self.assertIs(self.segment_evaluator.evaluate(test_case.get('dsl'),
                      test_case.get('custom_variables')), test_case.get('expectation'))

    def test_true3(self):
        test_case = self.test_cases.get('true3')
        self.assertIs(self.segment_evaluator.evaluate(test_case.get('dsl'),
                      test_case.get('custom_variables')), test_case.get('expectation'))

    def test_true2(self):
        test_case = self.test_cases.get('true2')
        self.assertIs(self.segment_evaluator.evaluate(test_case.get('dsl'),
                      test_case.get('custom_variables')), test_case.get('expectation'))
