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


class TestcomplexDsl_4(unittest.TestCase):

    def setUp(self):
        self.segment_evaluator = SegmentEvaluator()

    def test_false4(self):
        dsl = \
            '{"and":[{"or":[{"and":[{"not":{"or":[{"custom_variable":{"thanos":"snap"}}]}},{"or":[{"custom_variable":{"batman":"wildcard(*i am batman*)"}}]}]},{"or":[{"custom_variable":{"joker":"regex((joker)+)"}}]}]},{"and":[{"or":[{"or":[{"custom_variable":{"lol":"lolololololol"}}]},{"or":[{"custom_variable":{"blablabla":"wildcard(*bla*)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"and":[{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"or":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]}]}]}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'vwovwovwo': 'vwovwovwo',
            'vwo_starts_with': 'vwo',
            'regex_vwo': 'this   is vwo',
            'thanos': 'snap',
            'lol': 'lollolololol',
            'notvwo': 'vwo',
            'joker': 'joker joker joker',
            'batman': 'hello i am batman world',
            'blablabla': 'lba',
            'vwo_contains': 'vwo vwo vwo vwo vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_false1(self):
        dsl = \
            '{"and":[{"or":[{"and":[{"not":{"or":[{"custom_variable":{"thanos":"snap"}}]}},{"or":[{"custom_variable":{"batman":"wildcard(*i am batman*)"}}]}]},{"or":[{"custom_variable":{"joker":"regex((joker)+)"}}]}]},{"and":[{"or":[{"or":[{"custom_variable":{"lol":"lolololololol"}}]},{"or":[{"custom_variable":{"blablabla":"wildcard(*bla*)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"and":[{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"or":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]}]}]}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'vwovwovwo': 'vwovwovwo',
            'vwo_starts_with': 'owv vwo',
            'regex_vwo': 'this   is vwo',
            'thanos': 'half universe',
            'lol': 'lolololololol',
            'notvwo': 'vwo',
            'joker': 'joker joker joker',
            'batman': 'hello i am batman world',
            'blablabla': 'bla bla bla',
            'vwo_contains': 'vwo vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_false3(self):
        dsl = \
            '{"and":[{"or":[{"and":[{"not":{"or":[{"custom_variable":{"thanos":"snap"}}]}},{"or":[{"custom_variable":{"batman":"wildcard(*i am batman*)"}}]}]},{"or":[{"custom_variable":{"joker":"regex((joker)+)"}}]}]},{"and":[{"or":[{"or":[{"custom_variable":{"lol":"lolololololol"}}]},{"or":[{"custom_variable":{"blablabla":"wildcard(*bla*)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"and":[{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"or":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]}]}]}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'vwovwovwo': 'vwovwovwo',
            'vwo_starts_with': 'vwo',
            'regex_vwo': 'this   is vwo',
            'thanos': 'snap',
            'lol': 'lollolololol',
            'notvwo': 'vwo',
            'joker': 'joker joker joker',
            'batman': 'hello i am batman world',
            'blablabla': 'bla bla bla',
            'vwo_contains': 'vwo vwo vwo vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), False)

    def test_true1(self):
        dsl = \
            '{"and":[{"or":[{"and":[{"not":{"or":[{"custom_variable":{"thanos":"snap"}}]}},{"or":[{"custom_variable":{"batman":"wildcard(*i am batman*)"}}]}]},{"or":[{"custom_variable":{"joker":"regex((joker)+)"}}]}]},{"and":[{"or":[{"or":[{"custom_variable":{"lol":"lolololololol"}}]},{"or":[{"custom_variable":{"blablabla":"wildcard(*bla*)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"and":[{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"or":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]}]}]}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'vwovwovwo': 'vwovwovwo',
            'vwo_starts_with': 'owv vwo',
            'regex_vwo': 'this   is vwo',
            'thanos': 'half universe',
            'lol': 'lollolololol',
            'notvwo': 'vwo',
            'joker': 'joker joker joker',
            'batman': 'hello i am batman world',
            'blablabla': 'bla bla bla',
            'vwo_contains': 'vwo vwo vwo vwo vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_true3(self):
        dsl = \
            '{"and":[{"or":[{"and":[{"not":{"or":[{"custom_variable":{"thanos":"snap"}}]}},{"or":[{"custom_variable":{"batman":"wildcard(*i am batman*)"}}]}]},{"or":[{"custom_variable":{"joker":"regex((joker)+)"}}]}]},{"and":[{"or":[{"or":[{"custom_variable":{"lol":"lolololololol"}}]},{"or":[{"custom_variable":{"blablabla":"wildcard(*bla*)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"and":[{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"or":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]}]}]}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'vwovwovwo': 'vwovwovwo',
            'vwo_starts_with': 'owv vwo',
            'regex_vwo': 'this   is vwo',
            'thanos': 'half universe',
            'lol': 'lolololololol',
            'notvwo': 'vwo',
            'joker': 'joker joker joker',
            'batman': 'hello i am batman world',
            'blablabla': 'bla bla bla',
            'vwo_contains': 'vwo vwo vwo vwo vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)

    def test_true2(self):
        dsl = \
            '{"and":[{"or":[{"and":[{"not":{"or":[{"custom_variable":{"thanos":"snap"}}]}},{"or":[{"custom_variable":{"batman":"wildcard(*i am batman*)"}}]}]},{"or":[{"custom_variable":{"joker":"regex((joker)+)"}}]}]},{"and":[{"or":[{"or":[{"custom_variable":{"lol":"lolololololol"}}]},{"or":[{"custom_variable":{"blablabla":"wildcard(*bla*)"}}]}]},{"and":[{"and":[{"not":{"or":[{"custom_variable":{"notvwo":"notvwo"}}]}},{"or":[{"and":[{"or":[{"custom_variable":{"vwovwovwo":"regex(vwovwovwo)"}}]},{"or":[{"custom_variable":{"regex_vwo":"regex(this\\\\s+is\\\\s+vwo)"}}]}]},{"or":[{"and":[{"not":{"or":[{"custom_variable":{"vwo_not_equal_to":"owv"}}]}},{"or":[{"custom_variable":{"vwo_equal_to":"vwo"}}]}]},{"or":[{"custom_variable":{"vwo_starts_with":"wildcard(owv vwo*)"}}]}]}]}]},{"or":[{"custom_variable":{"vwo_contains":"wildcard(*vwo vwo vwo vwo vwo*)"}}]}]}]}]}'
        custom_variables = {
            'vwo_not_equal_to': 'vwo',
            'vwo_equal_to': 'vwo',
            'vwovwovwo': 'vwovwovwo',
            'vwo_starts_with': 'owv vwo',
            'regex_vwo': 'this   is vwo',
            'thanos': 'snap',
            'lol': 'lolololololol',
            'notvwo': 'vwo',
            'joker': 'joker joker joker',
            'batman': 'hello i am batman world',
            'blablabla': 'bla bla bla',
            'vwo_contains': 'vwo vwo vwo vwo vwo',
        }
        self.assertIs(self.segment_evaluator.evaluate('campaing_key', 'user_id', json.loads(dsl),
                      custom_variables), True)
