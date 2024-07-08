import time


def current_milli_time():
    """
    Get current system millis
    """
    return int(round(time.time() * 1000))
