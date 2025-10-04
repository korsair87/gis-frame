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

## Notes
- Uses legacy Python 2.7
- Requires ArcGIS Desktop/ArcPy
- Designed for Ukrainian cartographic data processing
