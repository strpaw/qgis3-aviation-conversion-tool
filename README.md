# AviationConversionTool

QGIS plugin to convert between units used in aviation (NM, km, feet, etc.) and various coordinate formats (DMS, DD, ARINC424)

![img](img//aviation_convertion_example.png)

- [Installation](#installation)
  - [For Git users](#git_user)
  - [For no Git users](#no_git_user)
- [Supported coordinate formats](#supported_coord_fromats)
  - [Coordinates from decimal degrees](#coord_from_dd)
  - [Arinc 424](#arinc424)
- [Usage examples](#usage_examples)

# Installation <a name=installation>

## For Git users <a name=git_user>

1. Copy repository to the local disk
2. cd dir to the main dir of the `qgis3-aviation-conversion-tool` repository
3. Create zip file from the `aviation_conversion_tool` subdirectory
4. QGIS - install plugin via Plugin manager/Installer  
   4.1 Open menu: `Plugins > Manage and Install Plugins`  
   4.2 Choose `Install from ZIP`  
   4.3 Select file `aviation_conversion_tool.zip`  
   4.4 Press `Install Plugin button` 
5. Plugin is installed: `Plugins > AviationConversionTool`

## For no Git users <a name=no_git_user>

1. Download repository via `Code > Download ZIP`
2. Unzip to `qgis3-aviation-conversion-tool` directory
3. cd dir to the unzipped directory
4. Create zip file from the `aviation_conversion_tool` subdirectory
5. QGIS - install plugin via Plugin manager/Installer  
   5.1 Open menu: `Plugins > Manage and Install Plugins`   
   5.2 Choose `Install from ZIP`  
   5.3 Select file `aviation_conversion_tool.zip`  
   5.4 Press `Install Plugin button`  
6. Plugin is installed: `Plugins > AviationConversionTool`

# Supported coordinate formats <a name=supported_coord_fromats>

## Coordinates from decimal degrees <a name=coord_from_dd>

* decimal degrees without hemisphere letter suffix/prefix, e.g: -50.5

## Arinc 424 <a name=arinc42>

* Longitude,  Latitude > Arinc 424 code:
  * decimal degrees with hemisphere letter suffix, leading zeros required, e.g: 020E, 01S, 100E, 10N


# Usage examples <a name=usage_examples>

![img](img//to_DMS_latitude_invalid_input.png)

![img](img//to_ARINC424_intput_invalid.png)
