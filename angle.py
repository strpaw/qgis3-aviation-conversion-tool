"""
angle.py
Angle module provides common functionality for longitude, latitude and bearing angle types.
"""
import math
from const import *

# Angle string representation formats
ANGLE_STRING_FORMATS = {
    AT_LONGITUDE: {
        AF_HDMS_ALL_SEP: '{hem} {d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_HDMS_SEP: '{hem}{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_DMSH_ALL_SEP: '{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f} {hem}',
        AF_DMSH_SEP: '{d:03d} {m:02d} {s:0{sec_length}.{sec_prec}f}{hem}',
    },
    AT_LATITUDE: {
        AF_HDMS_ALL_SEP: '{hem} {d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_HDMS_SEP: '{hem}{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
        AF_DMSH_ALL_SEP: '{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f} {hem}',
        AF_DMSH_SEP: '{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}{hem}',
    },
    AT_BEARING: {
        AF_DMS_SEP: '{d:02d} {m:02d} {s:0{sec_length}.{sec_prec}f}',
    }
}


class Angle:

    def __init__(self):
        self.err_msg = ''

    @staticmethod
    def normalize_src_angle(angle):
        """ Normalize input (source) angle before angle validation conversion to DD format:
            - remove leading and trailing blank characters
            - replace comma decimal point with dot decimal point
            - make upper case, example hemisphere character (direction) 'n' change to 'N'
        :param angle: str, angle to normalize, example "  32 44 56,77n "
        :return: str, normalized angle, example: 32 44 56.77N
        """
        return angle.strip().replace(',', '.').upper()

    @staticmethod
    def is_angle_within_range(ang_dd, ang_type):
        """  Check if angle is within range for specified angle type.
        :param ang_dd: float, angle to check
        :param ang_type: const(str): type of angle
        :return:
        """
        if ang_type == AT_LONGITUDE:
            return bool(-180 <= ang_dd <= 180)
        elif ang_type == AT_LATITUDE:
            return bool(-90 <= ang_dd <= 90)
        elif ang_type == AT_BEARING:
            return bool(0 <= ang_dd <= 360)

    @staticmethod
    def get_hemisphere_character(sign, ang_type):
        """ Get hemisphere character e.g. S, N base on "sign" (positive/negative) and angle type.
        :param sign: str, character '-', '+'
        :param ang_type: str, angle type
        :return: str: hemisphere character: N, E, S or W
        """
        if ang_type == AT_LONGITUDE:
            if sign == -1:
                return 'W'
            elif sign == 1:
                return 'E'
        elif ang_type == AT_LATITUDE:
            if sign == -1:
                return 'S'
            elif sign == 1:
                return 'N'

    @staticmethod
    def dd_to_dms_parts(ang_dd, prec=3):
        """ Convert angle from DD format into DMS 'parts': degrees, minutes and seconds
        :param ang_dd: float, angle in DD format
        :param prec: int, positive number of decimal point of seconds, default value is 3
        :return tuple: tuple of dd, mm, sec - float
        """

        d_frac_part, d_whole_part = math.modf(math.fabs(ang_dd))  # frac_part - fractional part
        m_frac_part, m_whole_part = math.modf(d_frac_part * 60)
        s_part = m_frac_part * 60

        def sign(a_dd): return 1 if a_dd >= 0 else -1
        dd = int(d_whole_part)
        mm = int(m_whole_part)
        sec = round(s_part, prec)

        return sign(ang_dd), dd, mm, sec

    def dd_to_dms_string(self, ang_dd, ang_type, ang_format=AF_DMSH_ALL_SEP, prec=3):
        """ Convert angle from DD format into DMS format
        :param ang_dd: float, angle in DD
        :param ang_type: str, angle type
        :param ang_format: str, desired format of angle in DMS format
        :param prec:  int, positive number of decimal point of seconds, default value is 3
        :return: ang_dms: str, input angle in DMS format
        """
        if Angle.is_angle_within_range(ang_dd, ang_type):
            sign, d, m, s = Angle.dd_to_dms_parts(ang_dd, prec)
            hem = Angle.get_hemisphere_character(sign, ang_type)

            if prec > 0:
                sec_length = prec + 3
            elif prec == 0:
                sec_length = 2
            else:
                return None

            try:
                formatted_dms_string = ANGLE_STRING_FORMATS[ang_type][ang_format]
                return formatted_dms_string.format(d=d, m=m, s=s,
                                                   sec_length=sec_length,
                                                   sec_prec=prec,
                                                   hem=hem)
            except KeyError:
                self.err_msg = 'Angle format "{}" is not supported for "{}" angle type'.format(ang_format, ang_type)

    @staticmethod
    def check_dd_format(angle, angle_type):
        if isinstance(angle, str):
            norm_ang = Angle.normalize_src_angle(angle)
            try:
                ang_dd = float(norm_ang)
                if Angle.is_angle_within_range(ang_dd, angle_type):
                    return ang_dd
            except ValueError:
                return
        elif isinstance(angle, (float, int)):
            if Angle.is_angle_within_range(angle, angle_type):
                return angle

    @staticmethod
    def dmsh_parts_to_dd(dmsh_parts):
        """ Convert coordinates parts into degrees minutes format.
        Note: If angle is within range, example longitude <-180, 180> will be check in separated method.
        :param dmsh_parts: tuple of degrees (int), minutes (int), seconds (float) and hemisphere character (str)
        :return: dd: float
        """
        d, m, s, h = dmsh_parts
        if (0 <= m < 60) and (0 <= s < 60):
            dd = d + m / 60 + s / 3600
            if h in ['W', 'S']:
                return -dd
            elif h in ['N', 'E']:
                return dd

    @staticmethod
    def dms_parts_to_dd(dms_parts):
        """ Convert coordinates parts into degrees minutes format.
        Note: If angle is within range, example longitude <-180, 180> will be check in separated method.
        :param dms_parts: tuple of degrees (int), minutes (int), seconds (float)
        :return: dd: float
        """
        d, m, s = dms_parts
        if (0 <= m < 60) and (0 <= s < 60):
            dd = d + m / 60 + s / 3600
            return dd
