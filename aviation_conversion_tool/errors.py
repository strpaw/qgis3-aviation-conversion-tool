"""Custom exceptions"""


class AviationConversionBaseError(Exception):
    """Base exception for QGIS Aviation Conversion Tool Plugin"""


class ARINC424ShorthandValueError(AviationConversionBaseError):
    """Risen when coordinate is not ARINC424 shorthand format"""


class CoordinateFullDegreesError(ARINC424ShorthandValueError):
    """Risen when value is not full degrees coordinate, e.g.: 6000N"""


class CoordinateValueFormatError(AviationConversionBaseError):
    """Risen when coordinate value is incorrect or is in not supported format"""


class NumberNotPositiveError(AviationConversionBaseError):
    """Risen when string value cannot be converted into number/or value can be converted
    but is not positive number"""
