import unittest
from aviation_conversion_tool.aviation_gis_tools.coordinate import *


class CoordinateTests(unittest.TestCase):

    def test_dmsh_compacted_format_valid_dmsh(self):
        longitudes = [
            ('1800000E', 180),
            ('1800000.0W', -180),
            ('0453000.000E', 45.5),
            ('0003000.000W', -0.5),
            ('1234601.445E', 123.76706805555555)
        ]

        for lon in longitudes:
            self.assertAlmostEqual(lon[1], Coordinate.convert_compacted_to_dd(lon[0], AT_LONGITUDE))

        latitudes = [
            ('900000N', 90),
            ('900000.0S', -90),
            ('453000.000S', -45.5),
            ('003000.000N', 0.5),
            ('234601.445N', 23.76706805555555)
        ]

        for lat in latitudes:
            self.assertAlmostEqual(lat[1], Coordinate.convert_compacted_to_dd(lat[0], AT_LATITUDE))

    def test_dmsh_compacted_format_valid_hdms(self):
        longitudes = [
            ('E1800000', 180),
            ('W1800000.0', -180),
            ('E0453000.000', 45.5),
            ('W0003000.000', -0.5),
            ('E1234601.445', 123.76706805555555)
        ]

        for lon in longitudes:
            self.assertAlmostEqual(lon[1], Coordinate.convert_compacted_to_dd(lon[0], AT_LONGITUDE))

        latitudes = [
            ('N900000', 90),
            ('S900000.0', -90),
            ('S453000.000', -45.5),
            ('N003000.000', 0.5),
            ('N234601.445', 23.76706805555555)
        ]

        for lat in latitudes:
            self.assertAlmostEqual(lat[1], Coordinate.convert_compacted_to_dd(lat[0], AT_LATITUDE))

    def test_dmsh_compacted_format_invalid_hdms(self):
        longitudes = [
            ('S1800000', None),
            ('1800000.1E', None),
            ('E0456000.000', None),
            ('W01002545.000', None),
            ('E1002560.445', None)
        ]

        for lon in longitudes:
            self.assertIsNone(Coordinate.convert_compacted_to_dd(lon[0], AT_LONGITUDE))

        latitudes = [
            ('E900000', None),
            ('S910000.0', None),
            ('S0453000.000', None),
            ('N003060.000', None),
            ('N236101.445', None)
        ]

        for lat in latitudes:
            self.assertIsNone(Coordinate.convert_compacted_to_dd(lat[0], AT_LATITUDE))

    def test_dmsh_separated_format_valid_coordinate(self):
        longitudes = [
            ('180 00 00E', 180),
            ('180 00 00.0 W', -180),
            ('045 30 00.000E', 45.5),
            ('000 30 00.000 W', -0.5),
            ('123 46 01.445E', 123.76706805555555)
        ]

        for lon in longitudes:
            self.assertAlmostEqual(lon[1], Coordinate.convert_separated_to_dd(lon[0], AT_LONGITUDE))

        latitudes = [
            ('N 90 00 00', 90),
            ('S90 00 00.0', -90),
            ('S 45 30 00.000', -45.5),
            ('N00 30 00.000', 0.5),
            ('N 23 46 01.445', 23.76706805555555)
        ]

        for lat in latitudes:
            self.assertAlmostEqual(lat[1], Coordinate.convert_separated_to_dd(lat[0], AT_LATITUDE))

    def test_dmsh_separated_format_invalid_coordinate(self):
        longitudes = [
            ('S180 0000', None),
            ('180 00 00.1E', None),
            ('E045 60 00.000', None),
            ('W010 025 45.000', None),
            ('E100 25 60.445', None)
        ]

        for lon in longitudes:
            self.assertIsNone(Coordinate.convert_separated_to_dd(lon[0], AT_LONGITUDE))

        latitudes = [
            ('E90 00 00', None),
            ('S 91 00 00.0', None),
            ('S045 30 00.000', None),
            ('N00 30 60.000', None),
            ('N23 61 01.445', None)
        ]

        for lat in latitudes:
            self.assertIsNone(Coordinate.convert_separated_to_dd(lat[0], AT_LATITUDE))

    def test_convert_to_dd_valid_coordinate(self):
        longitudes = [
            ('180', 180),
            ('-133.55666', -133.55666),
            ('E1233021.5555', 123.50598763888888),
            ('045 23 41.7888 W', -45.394941333333335),
            ('3 9 2.111E', 3.1505863888888888),
            ('W 003 09 02.111', -3.1505863888888888),
        ]

        for lon in longitudes:
            c = Coordinate(lon[0], AT_LONGITUDE)
            self.assertAlmostEqual(lon[1], c.convert_to_dd())

        latitudes = [
            ('90', 90),
            ('-33.55666', -33.55666),
            ('N233021.5555', 23.50598763888888),
            ('45 23 41.7888 S', -45.394941333333335),
            ('3 9 2.111N', 3.1505863888888888),
            ('S 03 09 02.111', -3.1505863888888888),
        ]

        for lat in latitudes:
            c = Coordinate(lat[0], AT_LATITUDE)
            self.assertAlmostEqual(lat[1], c.convert_to_dd())

    def test_convert_to_dd_invalid_coordinate(self):
        longitudes = [
            '181',
            '-180.55666',
            'S1233021.5555',
            '045 023 41.7888 W',
            '3 60 2.111E',
            'W 003 09 60.111',
        ]

        for lon in longitudes:
            c = Coordinate(lon, AT_LONGITUDE)
            self.assertIsNone(c.convert_to_dd())

        latitudes = [
            91,
            '91.55666',
            'E233021.5555',
            '045 23 41.7888 S',
            '3 60 2.111N',
            'S 03 09 60.00'
        ]

        for lat in latitudes:
            c = Coordinate(lat, AT_LATITUDE)
            self.assertIsNone(c.convert_to_dd())
