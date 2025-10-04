import os
import arcpy

from filesystem_utils import safe_shapefile_name
from logger_config import setup_logger

logger = setup_logger("export_utils")


def extract_by_field_values(input_fc, field_name, folders_dict):
    logger.info("Extracting features by field values to %d folders", len(folders_dict))
    logger.debug("Field name: %s", field_name)

    for val, folder_path in folders_dict.items():
        shp_name = "{}.shp".format(safe_shapefile_name(val))
        where_clause = "{} = '{}'".format(field_name, val)
        output_path = os.path.join(folder_path, shp_name)

        logger.info("Exporting field value '%s' to: %s", val, output_path)
        arcpy.FeatureClassToFeatureClass_conversion(input_fc, folder_path, shp_name, where_clause)

    logger.info("Feature extraction to shapefiles completed")


def extract_by_field_values_to_gdb(input_fc, field_name, folders_dict, gdb_name="frame.gdb", dataset_name="Frame",
                                   out_name_pattern=None):
    logger.debug("Extracting frames to geodatabases (%d items)", len(folders_dict))
    logger.debug("GDB name: %s, dataset: %s, pattern: %s", gdb_name, dataset_name, out_name_pattern)

    for val, folder_path in folders_dict.items():
        gdb_path = os.path.join(folder_path, gdb_name)
        feature_dataset = os.path.join(gdb_path, dataset_name)

        if not arcpy.Exists(feature_dataset):
            logger.error("Feature Dataset not found: %s", feature_dataset)
            continue

        # Use for unique "{val}"
        if out_name_pattern:
            out_name = out_name_pattern.format(val=safe_shapefile_name(val))
        else:
            out_name = safe_shapefile_name(val)

        output_fc = os.path.join(feature_dataset, out_name)

        if arcpy.Exists(output_fc):
            logger.debug("Output feature class exists, deleting: %s", output_fc)
            arcpy.Delete_management(output_fc)

        where_clause = "{} = '{}'".format(field_name, val)

        logger.debug("Exporting field value '%s' to: %s", val, output_fc)
        try:
            arcpy.FeatureClassToFeatureClass_conversion(
                input_fc,
                feature_dataset,
                out_name,
                where_clause
            )
        except Exception as e:
            logger.error("Failed to export %s: %s", val, str(e))
            raise
