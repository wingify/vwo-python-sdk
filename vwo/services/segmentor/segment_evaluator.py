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


from ...enums.file_name_enum import FileNameEnum
from .operand_evaluator import OperandEvaluator
from ...enums.segments import OperandTypes, OperatorTypes
from ...helpers.generic_util import get_key_value

FILE = FileNameEnum.Services.SegmentEvaluator


class SegmentEvaluator:
    """ Class to evaluate segments defined in VWO app """

    def __init__(self):
        """ Initializes this class with VWOLogger and OperandEvaluator """
        self.operand_evaluator = OperandEvaluator()

    def evaluate(self, segments, custom_variables):
        """A parser which recursively evaluates the custom_variables passed against
        the expression tree represented by segments, and returns the result.

        Args:
            segments(dict): The segments representing the expression tree
            custom_variables(dict): Key/value pair of variables

        Returns:
            bool(result): True or False
        """

        operator, sub_segments = get_key_value(segments)
        if operator == OperatorTypes.NOT:
            return not self.evaluate(sub_segments, custom_variables)
        elif operator == OperatorTypes.AND:
            return all(self.evaluate(y, custom_variables) for y in sub_segments)
        elif operator == OperatorTypes.OR:
            return any(self.evaluate(y, custom_variables) for y in sub_segments)
        elif operator == OperandTypes.CUSTOM_VARIABLE:
            return self.operand_evaluator.evaluate_custom_variable(sub_segments, custom_variables)
        elif operator == OperandTypes.USER:
            return self.operand_evaluator.evaluate_user(sub_segments, custom_variables)
