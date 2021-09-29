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

from .variation_schema import VARIATION
from .goal_schema import GOAL
from .variable_schema import VARIABLE
from .empty_object_schema import EMPTY_OBJECT


CAMPAIGN = {
    "type": "object",
    "properties": {
        "id": {"type": ["number", "string"]},
        "name": {"type": ["string"]},
        "key": {"type": ["string"]},
        "status": {"type": ["string"]},
        "percentTraffic": {"type": ["number"]},
        "type": {"type": ["string"]},
        "variations": {"if": {"type": "array"}, "then": {"items": VARIATION}, "else": EMPTY_OBJECT},
        "goals": {"if": {"type": "array"}, "then": {"items": GOAL}, "else": EMPTY_OBJECT},
        "variables": {"if": {"type": "array"}, "then": {"items": VARIABLE}, "else": EMPTY_OBJECT},
        "segments": {"type": "object"},
        "isBucketingSeedEnabled": {"type": "boolean"},
    },
    "required": ["id", "name", "key", "status", "percentTraffic", "variations", "goals"],
}
