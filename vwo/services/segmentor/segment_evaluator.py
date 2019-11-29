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


from ...enums.file_name_enum import FileNameEnum
from ...enums.log_level_enum import LogLevelEnum
from ...enums.log_message_enum import LogMessageEnum
from ...helpers import validate_util
from ...logger.logger_manager import VWOLogger
from ...helpers.generic_util import get_key_value
from .operand_evaluator import OperandEvaluator
from ...enums.segments import OperandTypes, OperatorTypes
FILE = FileNameEnum.SegmentEvaluator


class SegmentEvaluator:

    def __init__(self):
        """ Initializes this class with VWOLogger and OperandEvaluator """
        self.logger = VWOLogger.getInstance()
        self.operand_evaluator = OperandEvaluator()

    def evaluate_util(self, dsl, custom_variables):
        """ A parser which recursively evaluates the expression tree represented by dsl,
        and returns the result

        Args:
            dsl(dict): The segments defined in the campaign
            custom_variables(dict): Key/value pair of custom_attributs properties

        Returns:
            bool(result): True or False
        """

        operator, sub_dsl = get_key_value(dsl)
        if operator == OperatorTypes.NOT:
            return not self.evaluate_util(sub_dsl, custom_variables)
        elif operator == OperatorTypes.AND:
            return all(self.evaluate_util(y, custom_variables) for y in sub_dsl)
        elif operator == OperatorTypes.OR:
            return any(self.evaluate_util(y, custom_variables) for y in sub_dsl)
        elif operator == OperandTypes.CUSTOM_VARIABLE:
            return self.operand_evaluator.evaluate_operand(sub_dsl, custom_variables)

    def evaluate(self, campaign_key, user_id, dsl, custom_variables):
        """ Evaluates the custom_variables passed against the pre-segmentation condition defined
            in the corresponding campaign.

        Args:
            campaign_key(str): Running_campaign's key
            user_id(str): Unique user identifier
            dsl(dict): segments provided in the settings_file
            custom_variables(dict): custom variables provided in the apis

        Returns:
            bool(result): True if user passed pre-segmentation, else False """
        try:
            if validate_util.is_valid_value(dsl):
                result = self.evaluate_util(dsl, custom_variables)
            else:
                result = None
            if result:
                self.logger.log(
                    LogLevelEnum.INFO,
                    LogMessageEnum.INFO_MESSAGES.USER_PASSED_PRE_SEGMENTATION.format(
                        file=FILE,
                        user_id=user_id,
                        campaign_key=campaign_key,
                        custom_variables=custom_variables,
                    )
                )
            else:
                self.logger.log(
                    LogLevelEnum.INFO,
                    LogMessageEnum.INFO_MESSAGES.USER_FAILED_PRE_SEGMENTATION.format(
                        file=FILE,
                        user_id=user_id,
                        campaign_key=campaign_key,
                        custom_variables=custom_variables,
                    )
                )
            return result
        except Exception as e:
            self.logger.log(
                LogLevelEnum.ERROR,
                LogMessageEnum.ERROR_MESSAGES.PRE_SEGMENTATION_ERROR.format(
                    file=FILE,
                    user_id=user_id,
                    campaign_key=campaign_key,
                    custom_variables=custom_variables,
                    error_message=e
                )
            )
            return None
