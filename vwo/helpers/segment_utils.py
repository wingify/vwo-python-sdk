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


import math
import re
import sys

from ..enums.segments import OperandValueTypesName, OperandValuesBooleanTypes, OperandValueTypes

# This regex returns array of tuples of (operand_type, operand_value)
# from the string of type "operand_type(operand_value)"
GROUPING_PATTERN = re.compile("^(.+?)\((.*)\)")  # noqa: W605

# This regex returns array of tuples of (starting_star, operand_value, ending_star)
# from the string of type "*operand_value*"
WILDCARD_PATTERN = re.compile("(^\*|^)(.+?)(\*$|$)")  # noqa: W605


def convert_to_true_types(operator_value, custom_variables_value):
    """ Extracts true values represented in the args, and returns
    stringified value of it

    Args:
        operator_value(str): operand/dsl leaf value
        custom_variables_value(int|str|float): custom_variables value

    Returns:
        (str, str): tuple of str value of operator_value, custom_variables_value converted
        into their true types
    """

    # To deal with unicode type in python 2, if the type is unicode
    # encode the values
    if sys.version_info[0] < 3:
        if type(operator_value) is unicode:
            operator_value = operator_value.encode("utf-8")
        if type(custom_variables_value) is unicode:
            custom_variables_value = custom_variables_value.encode("utf-8")

    # This is atomic, either both values will be processed or none
    try:
        true_type_operator_value = float(operator_value)
        true_type_custom_variables_value = float(custom_variables_value)
    except Exception:
        return operator_value, custom_variables_value

    # Now both are float, So, convert them independently to int type
    # if they are int rather than floats
    if true_type_operator_value == math.floor(true_type_operator_value):
        true_type_operator_value = int(true_type_operator_value)
    if true_type_custom_variables_value == math.floor(true_type_custom_variables_value):
        true_type_custom_variables_value = int(true_type_custom_variables_value)

    # Convert them back to string and return
    return str(true_type_operator_value), str(true_type_custom_variables_value)


def separate_operand(operand):
    """ Extract the operand_type, ie. lower, wildcard, regex or equals

    Args:
        operand(str): string value from leaf_node of dsl

    Returns:
        (str, str): tuple of operand value and operand type
    """
    groups = GROUPING_PATTERN.findall(operand)
    if groups:
        return groups[0]
    return (OperandValueTypesName.EQUALS, operand)


def process_custom_variables_value(custom_variables_value):
    """ Processes the value from the custom_variables_variables

    Args:
        custom_variables_value(str|int|float|bool|None): the custom_variables_value provided
        inside custom_variables

    Returns:
        str(custom_variables_value): stringified value of processed custom_variables_value
    """
    if custom_variables_value is None:
        custom_variables_value = ""

    if type(custom_variables_value) is bool:
        if custom_variables_value:
            custom_variables_value = OperandValuesBooleanTypes.TRUE
        else:
            custom_variables_value = OperandValuesBooleanTypes.FALSE

    return str(custom_variables_value)


def process_operand_value(operand):
    """ Extracts operand_type and operand_value from the leaf_node/operand

    Args:
        operand(str): string value from the leaf_node

    Returns:
        (operand_type, operand_value): tuple of defined operand_types and
        operand_value
    """
    # separate the operand type and value inside the bracket
    operand_type_name, operand_value = separate_operand(operand)

    # Enum the operand type, here lower, regex, and equals will be identified
    operand_type = getattr(OperandValueTypes, operand_type_name, None)

    # In case of wildcard, the operand type is further divided into contains, startswith and endswith
    if operand_type_name == OperandValueTypesName.WILDCARD:
        starting_star, operand_value, ending_star = WILDCARD_PATTERN.findall(operand_value)[0]
        if starting_star and ending_star:
            operand_type = OperandValueTypes.contains
        elif starting_star:
            operand_type = OperandValueTypes.startswith
        elif ending_star:
            operand_type = OperandValueTypes.endswith
        else:
            operand_type = OperandValueTypes.equals

    # In case there is an abnormal patter, it would have passed all the above if cases, which means it
    # should be equals, so set the whole operand as operand value and operand type as equals
    if operand_type is None:
        operand_type, operand_value = OperandValueTypes.equals, operand

    return operand_type, operand_value
