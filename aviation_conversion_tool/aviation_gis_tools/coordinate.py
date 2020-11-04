import re
from aviation_conversion_tool.aviation_gis_tools.angle import *

# Note: Patterns does not take into account if coordinate is valid or not,
# for example if longitude does not exceed 180 degrees.
COORDINATE_COMPACTED = {
    AT_LONGITUDE: {
        'DMSH_COMPACTED': re.compile(r'''(?P<deg>^180|^1[0-7]\d|^0\d{2})  # Degrees
                                 (?P<min>[0-5]\d)  # Minutes
                                 (?P<sec>[0-5]\d\.\d+|[0-5]\d)  # Seconds
                                 (?P<hem>[EW]$)  # Hemisphere
                             ''', re.VERBOSE),
        'HDMS_COMPACTED': re.compile(r'''(?P<hem>^[EW])  # Hemisphere
                                (?P<deg>180|1[0-7]\d|0\d{2})  # Degrees
                                (?P<min>[0-5]\d)  # Minutes
                                (?P<sec>[0-5]\d\.\d+$|[0-5]\d$)  # Seconds             
                            ''', re.VERBOSE)
    },
    AT_LATITUDE: {
        'DMSH_COMPACTED': re.compile(r'''(?P<deg>^90|^[0-8]\d)  # Degrees
                                 (?P<min>[0-5]\d)  # Minutes
                                 (?P<sec>[0-5]\d\.\d+|[0-5]\d)  # Seconds
                                 (?P<hem>[NS]$)  # Hemisphere
                             ''', re.VERBOSE),
        'HDMS_COMPACTED': re.compile(r'''(?P<hem>^[NS])  # Hemisphere
                                 (?P<deg>90|[0-8]\d)  # Degrees
                                 (?P<min>[0-5]\d)  # Minutes
                                 (?P<sec>[0-5]\d\.\d+$|[0-5]\d$)  # Seconds
                              ''', re.VERBOSE)
    }
}

COORDINATE_SEPARATED = {
    AT_LONGITUDE: {
        'HDMS': re.compile(r'^[EW].*$'),
        'DMSH': re.compile(r'^\d.*[EW]$')
    },
    AT_LATITUDE: {
        'HDMS': re.compile(r'^[NS].*$'),
        'DMSH': re.compile(r'^\d.*[NS]$')
    }
}


class Coordinate(Angle):

    def __init__(self, src_angle, angle_type):
        Angle.__init__(self)
        self.src_angle = src_angle
        self.angle_type = angle_type

    @staticmethod
    def convert_compacted_to_dd(ang, ang_type):
        """ Converts DMSH or HDMS format into DD format.
        :param ang: str
        :param ang_type: str
        :return: float: angle in decimal degrees format, if conversion failed (not supported format,
                 error in angle example minutes >= 60, incorrect type - returns None)
        """
        for pattern in COORDINATE_COMPACTED[ang_type].values():
            if pattern.match(ang):
                dmsh_parts = pattern.search(ang)
                d = int(dmsh_parts.group('deg'))
                m = int(dmsh_parts.group('min'))
                s = float(dmsh_parts.group('sec'))
                h = dmsh_parts.group('hem')
                dd = Coordinate.dmsh_parts_to_dd((d, m, s, h))
                if Coordinate.is_angle_within_range(dd, ang_type):
                    return dd

    @staticmethod
    def convert_separated_to_dd(ang, ang_type):
        """ Converts DMSH or HDMS space separated format into DD format.
        :param ang: str,
        :param ang_type: str,
        :return: float: angle in decimal degrees format, if conversion failed (not supported format,
                 error in angle example minutes >= 60, incorrect type - returns None)
        """
        h, ang_parts = None, None
        patterns = COORDINATE_SEPARATED[ang_type]
        if re.match(patterns['HDMS'], ang):
            h = ang[0]
            ang_parts = ang[1:].strip().split(' ')
        elif re.match(patterns['DMSH'], ang):
            h = ang[-1]
            ang_parts = ang[:-1].strip().split(' ')
        if ang_parts:
            if len(ang_parts) == 3:
                try:
                    if (len(ang_parts[0]) <= 3 and ang_type == AT_LONGITUDE) or \
                       (len(ang_parts[0]) <= 2 and ang_type == AT_LATITUDE):
                        if len(ang_parts[1]) <= 2:
                            d, m, s = int(ang_parts[0]), int(ang_parts[1]), float(ang_parts[2])
                            dd = Coordinate.dmsh_parts_to_dd((d, m, s, h))
                            if dd is not None:
                                if Coordinate.is_angle_within_range(dd, ang_type):
                                    return dd
                except Exception as e:
                    return e

    def convert_to_dd(self):
        """ Convert src_angle to DD format
        :return: float, angle in DD format
        """
        dd = self.check_dd_format(self.src_angle, self.angle_type)
        if dd is None:
            dd = self.convert_compacted_to_dd(str(self.src_angle), self.angle_type)
            if dd is None:
                dd = self.convert_separated_to_dd(str(self.src_angle), self.angle_type)
        return dd
