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

# flake8: noqa

""" Schema for verifying the settings_file provided by the customer """

from .campaign_schema import CAMPAIGN
from .empty_object_schema import EMPTY_OBJECT


SETTINGS_FILE_SCHEMA = {
    "type": "object",
    "properties": {
        "version": {"type": ["number", "string"]},
        "accountId": {"type": ["number", "string"]},
        "campaigns": {"if": {"type": "array"}, "then": {"items": CAMPAIGN}, "else": EMPTY_OBJECT},
    },
    "required": ["version", "accountId", "campaigns"],
}
