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


class TestcomplexDsl_3(unittest.TestCase):

    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()

    def test_false5(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"contains_vwo":"wildcard(*vwo*)"}}]},{"and":[{"and":[{"or":[{"and":[{"or":[{"and":[{"or":[{"custom_variable":{"regex_for_all_letters":"regex(^[A-z]+$)"}}]},{"or":[{"custom_variable":{"regex_for_capital_letters":"regex(^[A-Z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_small_letters":"regex(^[a-z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_no_zeros":"regex(^[1-9]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_zeros":"regex(^[0]+$)"}}]}]},{"or":[{"custom_variable":{"regex_real_number":"regex(^\\\\d+(\\\\.\\\\d+)?)"}}]}]},{"or":[{"or":[{"custom_variable":{"this_is_regex":"regex(this\\\\s+is\\\\s+text)"}}]},{"and":[{"and":[{"or":[{"custom_variable":{"starts_with":"wildcard(starts_with_variable*)"}}]},{"or":[{"custom_variable":{"contains":"wildcard(*contains_variable*)"}}]}]},{"or":[{"not":{"or":[{"custom_variable":{"is_not_equal_to":"is_not_equal_to_variable"}}]}},{"or":[{"custom_variable":{"is_equal_to":"equal_to_variable"}}]}]}]}]}]}]}'
        custom_variables = {
            'contains_vwo': 'legends say that vwo is the best',
            'regex_for_no_zeros': 12231023,
            'regex_for_all_letters': 'dsfASF6',
            'regex_for_small_letters': 'sadfksjdf',
            'regex_real_number': 12321.2242,
            'regex_for_zeros': '0001000',
            'is_equal_to': 'equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'this    is    regex',
            'starts_with': 'starts_with_variable',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_false4(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"contains_vwo":"wildcard(*vwo*)"}}]},{"and":[{"and":[{"or":[{"and":[{"or":[{"and":[{"or":[{"custom_variable":{"regex_for_all_letters":"regex(^[A-z]+$)"}}]},{"or":[{"custom_variable":{"regex_for_capital_letters":"regex(^[A-Z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_small_letters":"regex(^[a-z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_no_zeros":"regex(^[1-9]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_zeros":"regex(^[0]+$)"}}]}]},{"or":[{"custom_variable":{"regex_real_number":"regex(^\\\\d+(\\\\.\\\\d+)?)"}}]}]},{"or":[{"or":[{"custom_variable":{"this_is_regex":"regex(this\\\\s+is\\\\s+text)"}}]},{"and":[{"and":[{"or":[{"custom_variable":{"starts_with":"wildcard(starts_with_variable*)"}}]},{"or":[{"custom_variable":{"contains":"wildcard(*contains_variable*)"}}]}]},{"or":[{"not":{"or":[{"custom_variable":{"is_not_equal_to":"is_not_equal_to_variable"}}]}},{"or":[{"custom_variable":{"is_equal_to":"equal_to_variable"}}]}]}]}]}]}]}'
        custom_variables = {
            'contains_vwo': 'legends say that vwo is the best',
            'regex_for_no_zeros': 1223123,
            'regex_for_all_letters': 'dsfASF',
            'regex_for_small_letters': 'sadfksjdf',
            'regex_real_number': 12321.2242,
            'regex_for_zeros': 0,
            'is_equal_to': 'is_not_equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'this    is    regex',
            'starts_with': 'starts_with_variable',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_false6(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"contains_vwo":"wildcard(*vwo*)"}}]},{"and":[{"and":[{"or":[{"and":[{"or":[{"and":[{"or":[{"custom_variable":{"regex_for_all_letters":"regex(^[A-z]+$)"}}]},{"or":[{"custom_variable":{"regex_for_capital_letters":"regex(^[A-Z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_small_letters":"regex(^[a-z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_no_zeros":"regex(^[1-9]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_zeros":"regex(^[0]+$)"}}]}]},{"or":[{"custom_variable":{"regex_real_number":"regex(^\\\\d+(\\\\.\\\\d+)?)"}}]}]},{"or":[{"or":[{"custom_variable":{"this_is_regex":"regex(this\\\\s+is\\\\s+text)"}}]},{"and":[{"and":[{"or":[{"custom_variable":{"starts_with":"wildcard(starts_with_variable*)"}}]},{"or":[{"custom_variable":{"contains":"wildcard(*contains_variable*)"}}]}]},{"or":[{"not":{"or":[{"custom_variable":{"is_not_equal_to":"is_not_equal_to_variable"}}]}},{"or":[{"custom_variable":{"is_equal_to":"equal_to_variable"}}]}]}]}]}]}]}'
        custom_variables = {
            'contains_vwo': 'legends say that vwo is the best',
            'regex_for_no_zeros': 12231023,
            'regex_for_all_letters': 'dsfASF6',
            'regex_for_small_letters': 'sadfksjdf',
            'regex_real_number': 12321.2242,
            'regex_for_zeros': 0,
            'is_equal_to': 'equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'this    is    regex',
            'starts_with': 'startss_with_variable',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_false1(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"contains_vwo":"wildcard(*vwo*)"}}]},{"and":[{"and":[{"or":[{"and":[{"or":[{"and":[{"or":[{"custom_variable":{"regex_for_all_letters":"regex(^[A-z]+$)"}}]},{"or":[{"custom_variable":{"regex_for_capital_letters":"regex(^[A-Z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_small_letters":"regex(^[a-z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_no_zeros":"regex(^[1-9]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_zeros":"regex(^[0]+$)"}}]}]},{"or":[{"custom_variable":{"regex_real_number":"regex(^\\\\d+(\\\\.\\\\d+)?)"}}]}]},{"or":[{"or":[{"custom_variable":{"this_is_regex":"regex(this\\\\s+is\\\\s+text)"}}]},{"and":[{"and":[{"or":[{"custom_variable":{"starts_with":"wildcard(starts_with_variable*)"}}]},{"or":[{"custom_variable":{"contains":"wildcard(*contains_variable*)"}}]}]},{"or":[{"not":{"or":[{"custom_variable":{"is_not_equal_to":"is_not_equal_to_variable"}}]}},{"or":[{"custom_variable":{"is_equal_to":"equal_to_variable"}}]}]}]}]}]}]}'
        custom_variables = {
            'contains_vwo': 'wingify',
            'regex_for_no_zeros': 1223123,
            'regex_for_all_letters': 'dsfASF',
            'regex_for_small_letters': 'sadfksjdf',
            'regex_real_number': 12321.2242,
            'regex_for_zeros': 0,
            'is_equal_to': 'equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'this    is    regex',
            'starts_with': 'starts_with_variable',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_false3(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"contains_vwo":"wildcard(*vwo*)"}}]},{"and":[{"and":[{"or":[{"and":[{"or":[{"and":[{"or":[{"custom_variable":{"regex_for_all_letters":"regex(^[A-z]+$)"}}]},{"or":[{"custom_variable":{"regex_for_capital_letters":"regex(^[A-Z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_small_letters":"regex(^[a-z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_no_zeros":"regex(^[1-9]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_zeros":"regex(^[0]+$)"}}]}]},{"or":[{"custom_variable":{"regex_real_number":"regex(^\\\\d+(\\\\.\\\\d+)?)"}}]}]},{"or":[{"or":[{"custom_variable":{"this_is_regex":"regex(this\\\\s+is\\\\s+text)"}}]},{"and":[{"and":[{"or":[{"custom_variable":{"starts_with":"wildcard(starts_with_variable*)"}}]},{"or":[{"custom_variable":{"contains":"wildcard(*contains_variable*)"}}]}]},{"or":[{"not":{"or":[{"custom_variable":{"is_not_equal_to":"is_not_equal_to_variable"}}]}},{"or":[{"custom_variable":{"is_equal_to":"equal_to_variable"}}]}]}]}]}]}]}'
        custom_variables = {
            'contains_vwo': 'legends say that vwo is the best',
            'regex_for_no_zeros': 1223123,
            'regex_for_all_letters': 'dsfASF',
            'regex_for_small_letters': 'sadfksjdf',
            'regex_real_number': 'not a number',
            'regex_for_zeros': 0,
            'is_equal_to': 'equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'this    is    regex',
            'starts_with': 'starts_with_variable',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_false2(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"contains_vwo":"wildcard(*vwo*)"}}]},{"and":[{"and":[{"or":[{"and":[{"or":[{"and":[{"or":[{"custom_variable":{"regex_for_all_letters":"regex(^[A-z]+$)"}}]},{"or":[{"custom_variable":{"regex_for_capital_letters":"regex(^[A-Z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_small_letters":"regex(^[a-z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_no_zeros":"regex(^[1-9]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_zeros":"regex(^[0]+$)"}}]}]},{"or":[{"custom_variable":{"regex_real_number":"regex(^\\\\d+(\\\\.\\\\d+)?)"}}]}]},{"or":[{"or":[{"custom_variable":{"this_is_regex":"regex(this\\\\s+is\\\\s+text)"}}]},{"and":[{"and":[{"or":[{"custom_variable":{"starts_with":"wildcard(starts_with_variable*)"}}]},{"or":[{"custom_variable":{"contains":"wildcard(*contains_variable*)"}}]}]},{"or":[{"not":{"or":[{"custom_variable":{"is_not_equal_to":"is_not_equal_to_variable"}}]}},{"or":[{"custom_variable":{"is_equal_to":"equal_to_variable"}}]}]}]}]}]}]}'
        custom_variables = {
            'contains_vwo': 'legends say that vwo is the best',
            'regex_for_no_zeros': 1223123,
            'regex_for_all_letters': 'dsfASF',
            'regex_for_small_letters': 'sadfksjdf',
            'regex_real_number': 12321.2242,
            'regex_for_zeros': 0,
            'is_equal_to': 'equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'thisis    regex',
            'starts_with': '_variable',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_true4(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"contains_vwo":"wildcard(*vwo*)"}}]},{"and":[{"and":[{"or":[{"and":[{"or":[{"and":[{"or":[{"custom_variable":{"regex_for_all_letters":"regex(^[A-z]+$)"}}]},{"or":[{"custom_variable":{"regex_for_capital_letters":"regex(^[A-Z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_small_letters":"regex(^[a-z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_no_zeros":"regex(^[1-9]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_zeros":"regex(^[0]+$)"}}]}]},{"or":[{"custom_variable":{"regex_real_number":"regex(^\\\\d+(\\\\.\\\\d+)?)"}}]}]},{"or":[{"or":[{"custom_variable":{"this_is_regex":"regex(this\\\\s+is\\\\s+text)"}}]},{"and":[{"and":[{"or":[{"custom_variable":{"starts_with":"wildcard(starts_with_variable*)"}}]},{"or":[{"custom_variable":{"contains":"wildcard(*contains_variable*)"}}]}]},{"or":[{"not":{"or":[{"custom_variable":{"is_not_equal_to":"is_not_equal_to_variable"}}]}},{"or":[{"custom_variable":{"is_equal_to":"equal_to_variable"}}]}]}]}]}]}]}'
        custom_variables = {
            'contains_vwo': 'legends say that vwo is the best',
            'regex_for_no_zeros': 1223123,
            'regex_for_all_letters': 'dsfASF',
            'regex_for_small_letters': 'sadfksjdf',
            'regex_real_number': 12321.2242,
            'regex_for_zeros': 0,
            'is_equal_to': 'equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'this    is    regex',
            'starts_with': 'starts_with_variable',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_true1(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"contains_vwo":"wildcard(*vwo*)"}}]},{"and":[{"and":[{"or":[{"and":[{"or":[{"and":[{"or":[{"custom_variable":{"regex_for_all_letters":"regex(^[A-z]+$)"}}]},{"or":[{"custom_variable":{"regex_for_capital_letters":"regex(^[A-Z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_small_letters":"regex(^[a-z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_no_zeros":"regex(^[1-9]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_zeros":"regex(^[0]+$)"}}]}]},{"or":[{"custom_variable":{"regex_real_number":"regex(^\\\\d+(\\\\.\\\\d+)?)"}}]}]},{"or":[{"or":[{"custom_variable":{"this_is_regex":"regex(this\\\\s+is\\\\s+text)"}}]},{"and":[{"and":[{"or":[{"custom_variable":{"starts_with":"wildcard(starts_with_variable*)"}}]},{"or":[{"custom_variable":{"contains":"wildcard(*contains_variable*)"}}]}]},{"or":[{"not":{"or":[{"custom_variable":{"is_not_equal_to":"is_not_equal_to_variable"}}]}},{"or":[{"custom_variable":{"is_equal_to":"equal_to_variable"}}]}]}]}]}]}]}'
        custom_variables = {
            'contains_vwo': 'legends say that vwo is the best',
            'regex_for_no_zeros': 1223123,
            'regex_for_all_letters': 'dsfASF',
            'regex_for_small_letters': 'sadfksjdf',
            'regex_real_number': 1234,
            'regex_for_zeros': 0,
            'is_equal_to': 'equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'this    is    regex',
            'starts_with': 'starts_with_variable',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_true3(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"contains_vwo":"wildcard(*vwo*)"}}]},{"and":[{"and":[{"or":[{"and":[{"or":[{"and":[{"or":[{"custom_variable":{"regex_for_all_letters":"regex(^[A-z]+$)"}}]},{"or":[{"custom_variable":{"regex_for_capital_letters":"regex(^[A-Z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_small_letters":"regex(^[a-z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_no_zeros":"regex(^[1-9]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_zeros":"regex(^[0]+$)"}}]}]},{"or":[{"custom_variable":{"regex_real_number":"regex(^\\\\d+(\\\\.\\\\d+)?)"}}]}]},{"or":[{"or":[{"custom_variable":{"this_is_regex":"regex(this\\\\s+is\\\\s+text)"}}]},{"and":[{"and":[{"or":[{"custom_variable":{"starts_with":"wildcard(starts_with_variable*)"}}]},{"or":[{"custom_variable":{"contains":"wildcard(*contains_variable*)"}}]}]},{"or":[{"not":{"or":[{"custom_variable":{"is_not_equal_to":"is_not_equal_to_variable"}}]}},{"or":[{"custom_variable":{"is_equal_to":"equal_to_variable"}}]}]}]}]}]}]}'
        custom_variables = {
            'contains_vwo': 'legends say that vwo is the best',
            'regex_for_no_zeros': 12231023,
            'regex_for_all_letters': 'dsfASF6',
            'regex_for_small_letters': 'sadfAksjdf',
            'regex_real_number': 12321.2242,
            'regex_for_zeros': 0,
            'is_equal_to': 'equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'this    is    regex',
            'starts_with': 'starts_with_variable',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_true2(self):
        dsl = \
            '{"and":[{"or":[{"custom_variable":{"contains_vwo":"wildcard(*vwo*)"}}]},{"and":[{"and":[{"or":[{"and":[{"or":[{"and":[{"or":[{"custom_variable":{"regex_for_all_letters":"regex(^[A-z]+$)"}}]},{"or":[{"custom_variable":{"regex_for_capital_letters":"regex(^[A-Z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_small_letters":"regex(^[a-z]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_no_zeros":"regex(^[1-9]+$)"}}]}]},{"or":[{"custom_variable":{"regex_for_zeros":"regex(^[0]+$)"}}]}]},{"or":[{"custom_variable":{"regex_real_number":"regex(^\\\\d+(\\\\.\\\\d+)?)"}}]}]},{"or":[{"or":[{"custom_variable":{"this_is_regex":"regex(this\\\\s+is\\\\s+text)"}}]},{"and":[{"and":[{"or":[{"custom_variable":{"starts_with":"wildcard(starts_with_variable*)"}}]},{"or":[{"custom_variable":{"contains":"wildcard(*contains_variable*)"}}]}]},{"or":[{"not":{"or":[{"custom_variable":{"is_not_equal_to":"is_not_equal_to_variable"}}]}},{"or":[{"custom_variable":{"is_equal_to":"equal_to_variable"}}]}]}]}]}]}]}'
        custom_variables = {
            'contains_vwo': 'legends say that vwo is the best',
            'regex_for_no_zeros': 12231023,
            'regex_for_all_letters': 'dsfASF6',
            'regex_for_small_letters': 'sadfksjdf',
            'regex_real_number': 12321.2242,
            'regex_for_zeros': 0,
            'is_equal_to': 'equal_to_variable',
            'contains': 'contains_variable',
            'regex_for_capital_letters': 'SADFLSDLF',
            'is_not_equal_to': 'is_not_equal_to_variable',
            'this_is_regex': 'this    is    regex',
            'starts_with': 'starts_with_variable',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)
