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


class TestcomplexDsl_2(unittest.TestCase):

    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()

    def test_false4(self):
        dsl = \
            '{"or":[{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_starts_with': 'v owv vwo',
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'notvwo': 'vwo',
            'regex_vwo': 'this   is vwo',
            'vwovwovwo': 'vwovovwo',
            'vwo_contains': 'vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_false1(self):
        dsl = \
            '{"or":[{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_starts_with': 'owv vwo',
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwovwo',
            'notvwo': 'vwo',
            'regex_vwo': 'this   is vwo',
            'vwovwovwo': 'vwovw',
            'vwo_contains': 'vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_false3(self):
        dsl = \
            '{"or":[{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_starts_with': 'vwo owv vwo',
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'notvwo': 'vwo',
            'regex_vwo': 'this   isvwo',
            'vwovwovwo': 'vwovwovw',
            'vwo_contains': 'vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_false2(self):
        dsl = \
            '{"or":[{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_starts_with': 'vwo owv vwo',
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'notvwo': 'vwo',
            'regex_vwo': 'this   is vwo',
            'vwovwovwo': 'vwo',
            'vwo_contains': 'vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_true4(self):
        dsl = \
            '{"or":[{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_starts_with': 'vwo owv vwo',
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'notvwo': 'vo',
            'regex_vwo': 'this   is vwo',
            'vwovwovwo': 'vwovwovwo',
            'vwo_contains': 'vw',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_true1(self):
        dsl = \
            '{"or":[{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_starts_with': 'owv vwo',
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'notvwo': 'vwo',
            'regex_vwo': 'this   is vwo',
            'vwovwovwo': 'vwovwovwo',
            'vwo_contains': 'vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_true3(self):
        dsl = \
            '{"or":[{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_starts_with': 'owv vwo',
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'notvwo': 'vwovwo',
            'regex_vwo': 'this   isvwo',
            'vwovwovwo': 'vwovwovwo',
            'vwo_contains': 'vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_true2(self):
        dsl = \
            '{"or":[{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_starts_with': 'owv vwo',
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'notvwo': 'vwo',
            'regex_vwo': 'this   is vwo',
            'vwovwovwo': 'vwo',
            'vwo_contains': 'vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)
