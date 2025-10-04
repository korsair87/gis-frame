# GIS Frame Processing Application

## Project Description
Python application for geospatial data processing using ArcPy. The program is designed for creating cartographic frames and coordinate grids.

## Core Functionality
- Shapefile processing
- Coordinate system reprojection (from Pulkovo 1942 to Ukraine 2000 GK Zone 7)
- Geodatabase (GDB) creation
- Coordinate grid generation
- Data export by nomenclature sheets

## Key Components
- `main.py` - Main file with core logic
- `config.py` - Configuration settings
- `modules/` - Utility modules for grids, fields, export, GDB operations, and file handling

## Dependencies
- ArcPy (ArcGIS Python API)
- Python 2.7

## Configuration
Main parameters in `config.py`:
- `BASE_WORK_FOLDER`: Base working directory
- `OUT_SPATIAL_REFERENCE`: 5565 (Ukraine 2000 GK Zone 7)
- `EXPORT_FIELD`: "NOMENCL" - field for export
- `INPUT_SHAPEFILE_NAME`: Input shapefile

## Usage
```bash
python main.py
```

## Workflow
1. Data preparation
2. Create export folders
3. Generate geodatabases
4. Generate coordinate grids
5. Copy MXD templates

## Logging
The application uses a comprehensive logging system:
- **Console output**: Simple format with timestamps for real-time monitoring
- **File output**: Detailed logs with function names and line numbers in `logs/gis_frame_YYYYMMDD.log`
- **UTF-8 encoding**: Full support for Cyrillic characters in data fields and file paths
- **Logging guidelines**:
  - All log messages must be in English for consistency and debugging
  - Data containing Cyrillic characters (file paths, field values) is properly encoded
  - Uses Python's built-in `logging` module (no additional dependencies)

## Frame Range Processing
Configure frame processing ranges in `config.py`:
- `ENABLE_FRAME_RANGE = True/False` - Toggle range processing
- `FRAME_START = 1` - Start frame number (1-based)
- `FRAME_END = 10` - End frame number (inclusive)

## Notes
- Uses legacy Python 2.7
- Requires ArcGIS Desktop/ArcPy
- Designed for Ukrainian cartographic data processing
