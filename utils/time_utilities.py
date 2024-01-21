import time
import math
from typing import Union
from datetime import datetime


class TimeUtilities:
    epoch = datetime(1970, 1, 1)

    @staticmethod
    def current_time_in_sec() -> int:
        return int(time.time())

    @staticmethod
    def current_time_in_milliseconds() -> int:
        return int((time.time() * 1000))

    @staticmethod
    def convert_milliseconds_to_sec(millisec: Union[int, str]) -> int:
        return millisec // 1000

    @staticmethod
    def get_epoch_time_from_dd_mm_yyyy(date_string: str) -> int:
        return int((datetime.strptime(date_string, "%d-%B-%Y") - TimeUtilities.epoch).total_seconds())

    @staticmethod
    def is_epoch_in_milliseconds(epoch_time) -> bool:

        if math.floor(math.log10(epoch_time) + 1) == 13:
            return True

        return False

    @staticmethod
    def convert_epoch_time_to_ddmmyy(epoch_time):
        """format -- 180621"""
        if TimeUtilities.is_epoch_in_milliseconds(epoch_time):
            epoch_time = TimeUtilities.convert_milliseconds_to_sec(epoch_time)

        return time.strftime('%d%m%y', time.localtime(epoch_time))

    @staticmethod
    def convert_epoch_time_to_ddmmyyyy(epoch_time):
        """format -- 180621"""
        if TimeUtilities.is_epoch_in_milliseconds(epoch_time):
            epoch_time = TimeUtilities.convert_milliseconds_to_sec(epoch_time)

        return time.strftime('%d-%b-%Y', time.localtime(epoch_time))

    @staticmethod
    def convert_epoch_time_to_yyyy(epoch_time):
        """format -- 180621"""
        if TimeUtilities.is_epoch_in_milliseconds(epoch_time):
            epoch_time = TimeUtilities.convert_milliseconds_to_sec(epoch_time)

        return time.strftime('%Y', time.localtime(epoch_time))
