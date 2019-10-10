""" Utitlity for managing feature related functionalities """

from ..constants import constants
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..logger.logger_manager import VWOLogger


def get_type_casted_feature_value(value, variable_type):
    """ Returns type casted value to given value type if possbile.

    Args:
        value (int|float|str|bool): Value to type cast
        variable_type (type): Type to which value needs to be casted
    Returns:
        type_casted_value|None : Type casted value if value can be
        typecasted else None
    """

    # Check if type(value) is already equal to required variable_type
    if type(value) == constants.PY_VARIABLE_TYPES.get(variable_type):
        return value
    try:
        if variable_type == constants.VARIABLE_TYPES.STRING:
            return str(value)
        elif variable_type == constants.VARIABLE_TYPES.INTEGER:
            return int(value)
        elif variable_type == constants.VARIABLE_TYPES.DOUBLE:
            return float(value)
        else:
            # required type is boolean, simply raise exception
            # as it doesn't belong to bool type
            raise Exception
    except Exception:
        VWOLogger.getInstance().log(
            LogLevelEnum.ERROR,
            LogMessageEnum.ERROR_MESSAGES.UNABLE_TO_TYPE_CAST.format(
                file=FileNameEnum.FeatureUtil,
                value=value,
                variable_type=variable_type,
                of_type=type(value)
            )
        )
        return None
