"""
const.py
const module provides common constants as unit of measure, angle types used in aviation_gis_toolkit package.
"""

# Units of measure

UOM_M = 'm'
UOM_KM = 'km'
UOM_NM = 'NM'
UOM_FT = 'ft'
UOM_SM = 'SM'

UOM_LIST = [UOM_M, UOM_KM, UOM_NM, UOM_FT, UOM_SM]

# Angle types

AT_LONGITUDE = 'AT_LONGITUDE '
AT_LATITUDE = 'AT_LATITUDE'
AT_BEARING = 'AT_BEARING'

# Angle formats

AF_DMSH_ALL_SEP = 'AF_DMSH_ALL_SEP'  # e.g.: 55 22 43.47 N
AF_HDMS_ALL_SEP = 'AF_HDMS_ALL_SEP'
AF_DMSH_SEP = 'AF_DMSH_SEP'  # e.g.: 55 22 43.47N
AF_HDMS_SEP = 'AF_HDMS_SEP'

AF_DMS_SEP = 'AF_DMS_SEP'  # e.g.: 55 22 43.47
