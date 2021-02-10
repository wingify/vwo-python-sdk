# Copyright 2019-2021 Wingify Software Pvt. Ltd.
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

from vwo.storage.user import UserStorage


class USTest(unittest.TestCase):
    def test_class_initialization(self):
        class US(UserStorage):
            pass

        self.assertIsNotNone(US())

    def test_check_get_is_present(self):
        us = UserStorage()
        self.assertIsNone(us.get(123, "None"))

    def test_check_set_is_present(self):
        us = UserStorage()
        self.assertIsNone(us.set(123))
