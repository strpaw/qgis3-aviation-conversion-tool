import unittest
from aviation_conversion_tool.aviation_gis_tools.angle import *


class AngleTests(unittest.TestCase):

    def test_normalize_src_angle(self):
        self.assertEqual('32 44 56.77N', Angle.normalize_src_angle('  32 44 56,77n '))

    def test_angle_is_within_range(self):
        self.assertEqual(Angle.is_angle_within_range(-180.1, AT_LONGITUDE), False)
        self.assertEqual(Angle.is_angle_within_range(-180, AT_LONGITUDE), True)
        self.assertEqual(Angle.is_angle_within_range(180, AT_LONGITUDE), True)
        self.assertEqual(Angle.is_angle_within_range(180.1, AT_LONGITUDE), False)

        self.assertEqual(Angle.is_angle_within_range(-90.1, AT_LATITUDE), False)
        self.assertEqual(Angle.is_angle_within_range(-90, AT_LATITUDE), True)
        self.assertEqual(Angle.is_angle_within_range(90, AT_LATITUDE), True)
        self.assertEqual(Angle.is_angle_within_range(90.1, AT_LATITUDE), False)

    def test_get_hemisphere_character(self):
        self.assertEqual('E', Angle.get_hemisphere_character(1, AT_LONGITUDE))
        self.assertEqual('W', Angle.get_hemisphere_character(-1, AT_LONGITUDE))
        self.assertEqual(None, Angle.get_hemisphere_character('-1', AT_LONGITUDE))
        self.assertEqual(None, Angle.get_hemisphere_character(0, AT_LATITUDE))
        self.assertEqual('S', Angle.get_hemisphere_character(-1, AT_LATITUDE))
        self.assertEqual('N', Angle.get_hemisphere_character(1, AT_LATITUDE))

    def test_dd_to_dms_parts(self):
        self.assertEqual(Angle.dd_to_dms_parts(0), (1, 0, 0, 0.000))
        self.assertEqual(Angle.dd_to_dms_parts(-1), (-1, 1, 0, 0.000))
        self.assertEqual(Angle.dd_to_dms_parts(10), (1, 10, 0, 0.000))
        self.assertEqual(Angle.dd_to_dms_parts(45.5), (1, 45, 30, 0.000))
        self.assertEqual(Angle.dd_to_dms_parts(1.0169444444444400), (1, 1, 1, 1.0))
        self.assertEqual(Angle.dd_to_dms_parts(100.1694444444444000), (1, 100, 10, 10.0))
        self.assertEqual(Angle.dd_to_dms_parts(-120.3388888888889000), (-1, 120, 20, 20.0))
        self.assertEqual(Angle.dd_to_dms_parts(145.9589599661111, prec=6), (1, 145, 57, 32.255878))

    def test_longitude_dd_to_dms_string(self):
        a = Angle()
        self.assertEqual('E 145 57 32.256',
                         a.dd_to_dms_string(145.9589599661111000, AT_LONGITUDE, ang_format=AF_HDMS_ALL_SEP))
        self.assertEqual('W145 57 32.256',
                         a.dd_to_dms_string(-145.9589599661111000, AT_LONGITUDE, ang_format=AF_HDMS_SEP))
        self.assertEqual('145 57 32.256 E',
                         a.dd_to_dms_string(145.9589599661111000, AT_LONGITUDE, ang_format=AF_DMSH_ALL_SEP))
        self.assertEqual('145 57 32.256E',
                         a.dd_to_dms_string(145.9589599661111000, AT_LONGITUDE, ang_format=AF_DMSH_SEP))

    def test_latitude_dd_to_dms_string(self):
        a = Angle()
        self.assertEqual('N 45 57 32.256',
                         a.dd_to_dms_string(45.9589599661111000, AT_LATITUDE, ang_format=AF_HDMS_ALL_SEP))
        self.assertEqual('N45 57 32.256',
                         a.dd_to_dms_string(45.9589599661111000, AT_LATITUDE, ang_format=AF_HDMS_SEP))
        self.assertEqual('45 57 32.256 N',
                         a.dd_to_dms_string(45.9589599661111000, AT_LATITUDE, ang_format=AF_DMSH_ALL_SEP))
        self.assertEqual('45 57 32.256N',
                         a.dd_to_dms_string(45.9589599661111000, AT_LATITUDE, ang_format=AF_DMSH_SEP))

    def test_bearing_dd_to_dms_string(self):
        a = Angle()
        self.assertEqual('45 57 32.256',
                         a.dd_to_dms_string(45.9589599661111000, AT_BEARING, ang_format=AF_DMS_SEP))

    def test_check_dd_format_longitude(self):
        self.assertEqual(-180, Angle.check_dd_format(-180, AT_LONGITUDE))
        self.assertEqual(25.44, Angle.check_dd_format('25,44', AT_LONGITUDE))
        self.assertEqual(None, Angle.check_dd_format(181, AT_LONGITUDE))

    def test_check_dd_format_latitude(self):
        self.assertEqual(-90, Angle.check_dd_format(-90, AT_LATITUDE))
        self.assertEqual(25.44, Angle.check_dd_format('25,44', AT_LATITUDE))
        self.assertEqual(None, Angle.check_dd_format(181, AT_LATITUDE))

    def test_check_dd_format_bearing(self):
        self.assertEqual(0, Angle.check_dd_format(0, AT_BEARING))
        self.assertEqual(25.44, Angle.check_dd_format('25,44', AT_BEARING))
        self.assertEqual(None, Angle.check_dd_format('361,0', AT_BEARING))

    def test_dmsh_parts_to_dd(self):
        self.assertEqual(None, Angle.dmsh_parts_to_dd((100, 61, 59, 'W')))
        self.assertEqual(None, Angle.dmsh_parts_to_dd((100, 0, 60, 'E')))
        self.assertEqual(None, Angle.dmsh_parts_to_dd((100, -1, 0, 'S')))
        self.assertEqual(None, Angle.dmsh_parts_to_dd((100, 5, 10, 'A')))
        self.assertEqual(100.59555555555555, Angle.dmsh_parts_to_dd((100, 35, 44, 'N')))
        self.assertEqual(-100.59555555555555, Angle.dmsh_parts_to_dd((100, 35, 44, 'W')))

    def test_dms_parts_to_dd(self):
        self.assertEqual(None, Angle.dms_parts_to_dd((100, 61, 59)))
        self.assertEqual(None, Angle.dms_parts_to_dd((100, 0, 60)))
        self.assertEqual(None, Angle.dms_parts_to_dd((100, -1, 0)))
        self.assertEqual(100.59555555555555, Angle.dms_parts_to_dd((100, 35, 44)))
