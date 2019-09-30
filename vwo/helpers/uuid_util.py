""" Generating UUID required for sending impression to server """

import uuid
from ..enums.log_message_enum import LogMessageEnum
from ..enums.file_name_enum import FileNameEnum
from ..enums.log_level_enum import LogLevelEnum
from ..logger.logger_manager import VWOLogger

VWO_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, 'https://vwo.com')


def generator_for(user_id, account_id):
    """ Generates desired UUID

    Args:
        user_id (int|string): User identifier
        account_id (int|string): Account identifier

    Returns:
        int : Desired Uuid
    """

    user_id = str(user_id)
    account_id = str(account_id)
    user_id_namespace = generate(VWO_NAMESPACE, account_id)
    uuid_for_account_user_id = generate(user_id_namespace, user_id)

    desired_uuid = str(uuid_for_account_user_id).replace('-', '').upper()

    VWOLogger.getInstance().log(
        LogLevelEnum.DEBUG,
        LogMessageEnum.DEBUG_MESSAGES.UUID_FOR_USER.format(
            file=FileNameEnum.UuidUtil,
            user_id=user_id,
            account_id=account_id,
            desired_uuid=desired_uuid
        )
    )
    return desired_uuid


def generate(namespace, name):
    """ Generated uuid from namespace and name, uses uuid5 from python uuid moduele

    Args:
        namespace (string): Namespace
        name (string): Name

    Returns:
        string|None: Uuid, none if any of the arguments is empty
    """

    if name and namespace:
        return uuid.uuid5(namespace, name)
    return None
