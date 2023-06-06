# Copyright 2019-2022 Wingify Software Pvt. Ltd.
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

GROUP_SCHEMA = {
    "type": "object",
    "patternProperties": {
        "^[0-9]+$": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "campaigns": {"type": "array", "items": {"type": "number"}, "uniqueItems": True},
                "et": {"type": "number"},
                "p": {"type": "array", "items": {"type": "number"}},
                "wt": {"type": "object", "patternProperties": {"^[0-9]+$": {"type": "number"}}},
            },
        }
    },
    "additionalProperties": False,
}
