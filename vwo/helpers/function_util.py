""" Function utility for helper math and random functions """

import random
from datetime import datetime
import time


def get_random_number():
    """ Returns a random number

    Returns:
        float: A random number
    """
    return random.random()


def get_current_unix_timestamp():
    """ Returns current unix timestamp

    Returns:
        int: Current unix timestamp
    """
    return int(time.mktime(datetime.now().timetuple()))
