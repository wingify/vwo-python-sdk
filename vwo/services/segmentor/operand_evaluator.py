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


import re

from ...helpers.generic_util import get_key_value
from ...helpers.segment_utils import convert_to_true_types, process_custom_variables_value, process_operand_value


class OperandEvaluator:
    """ Class to evaluate different kinds of operands supported by segmentation """

    def lower(self, operand_value, custom_variables_value):
        """ Checks if both values are same after 'lowercasing'
            i.e. case insensitive check

        Args:
            operand_value: Leaf value from the segments
            custom_variables_value: Value from the custom_variables

        Returns:
            bool (result): True or False
        """
        return operand_value.lower() == custom_variables_value.lower()

    def contains(self, operand_value, custom_variables_value):
        """ Checks if custom_variables_value contains operand_value

        Args:
            operand_value: Leaf value from the segments
            custom_variables_value: Value from the custom_variables

        Returns:
            bool (result): True or False
        """
        return custom_variables_value.__contains__(operand_value)

    def startswith(self, operand_value, custom_variables_value):
        """ Checks if custom_variables_value starts with operand_value

        Args:
            operand_value: Leaf value from the segments
            custom_variables_value: Value from the custom_variables

        Returns:
            bool (result): True or False
        """
        return custom_variables_value.endswith(operand_value)

    def endswith(self, operand_value, custom_variables_value):
        """ Checks if custom_variables_value ends with operand_value

        Args:
            operand_value: Leaf value from the segments
            custom_variables_value: Value from the custom_variables

        Returns:
            bool (result): True or False
        """
        return custom_variables_value.startswith(operand_value)

    def regex(self, operand_value, custom_variables_value):
        """ Checks if custom_variables_value matches the regex specified by
            operand_value

        Args:
            operand_value: Leaf value from the segments
            custom_variables_value: Value from the custom_variables

        Returns:
            bool (result): True or False
        """
        try:
            pattern = re.compile(operand_value)
            return bool(pattern.search(custom_variables_value))
        except Exception:
            return False

    def equals(self, operand_value, custom_variables_value):
        """ Checks if both values are exactly same

        Args:
            operand_value: Leaf value from the segments
            custom_variables_value: Value from the custom_variables

        Returns:
            bool (result): True or False
        """
        return custom_variables_value == operand_value

    def evaluate_custom_variable(self, operand, custom_variables):
        """ Identifies the condition stated in the leaf node and evaluates the result

        Args:
            operand(str): String representation of operand_type and operand_value,
            for eg. lower(vwo), wildcard(www.vwo.com/*), etc.
            custom_variables(dict): Custom variables provided to the sdk through the api

        Returns:
            boolean (result): True if custom_variable satisfies condition stated by operand_value,
            else False
        """

        # Extract custom_variable_key and custom_variables_value from operand
        operand_key, operand = get_key_value(operand)

        # Retrieve corresponding custom_variable value from custom_variables
        custom_variables_value = custom_variables.get(operand_key)

        # Pre process custom_variable value
        custom_variables_value = process_custom_variables_value(custom_variables_value)

        # Pre process operand value
        operand_type, operand_value = process_operand_value(operand)

        # Process the custom_variables_value and operand_value to make them of same type
        operand_value, custom_variables_value = convert_to_true_types(operand_value, custom_variables_value)

        # Call the self method corresponding to operand_type to evaluate the result
        return getattr(self, operand_type)(operand_value, custom_variables_value)

    def evaluate_user(self, operand, variation_targeting_variables):
        """ Identifies the condition stated in the leaf node and evaluates the result

        Args:
            operand(str): String representation of comma separated user_ids
            variation_targeting_variables(dict): Variation targeting variables provided to the sdk through the api

        Returns:
            boolean (result): True if _vwo_user_id is in comma separated user_ids represented in operand
            else False
        """

        # Retrieve corresponding _vwo_user_id value from variation_targeting_variables
        _vwo_user_id = variation_targeting_variables.get("_vwo_user_id")

        # Extract user_id list from operand
        operand_user_id_list = operand.split(",")

        # check if _vwo_user_id exists in operand_user_id_list or not
        for user_id in operand_user_id_list:
            if user_id.strip() == _vwo_user_id:
                return True
        return False
