# coding=utf-8
import arcpy
import os
from logger_config import setup_logger

logger = setup_logger("gdb_utils")


def create_gdb(parent_folder, gdb_name):
    new_gdb = os.path.join(parent_folder, gdb_name)
    if not arcpy.Exists(new_gdb):
        logger.debug("Creating geodatabase: %s", new_gdb)
        arcpy.CreateFileGDB_management(parent_folder, gdb_name)
    else:
        logger.debug("Geodatabase already exists: %s", new_gdb)
    return new_gdb


def copy_shapefile(input_shp, output_fc):
    if arcpy.Exists(output_fc):
        logger.debug("Output feature class exists. Deleting: %s", output_fc)
        arcpy.Delete_management(output_fc)

    logger.debug("Copying shapefile from: %s to: %s", input_shp, output_fc)
    arcpy.CopyFeatures_management(input_shp, output_fc)


def re_project_feature_class(input_fc, output_fc, spatial_ref_out, spatial_ref_in=None, geographic_transform=""):
    if arcpy.Exists(output_fc):
        logger.debug("Output feature class exists. Deleting: %s", output_fc)
        arcpy.Delete_management(output_fc)

    # Use proper geographic transformation for Pulkovo 1942 to Ukraine 2000
    if not geographic_transform:
        geographic_transform = "Pulkovo_1942_To_WGS_1984_2 + WGS_1984_To_Ukraine_2000_GK_CM_27E"

    logger.debug("Reprojecting from: %s to: %s", input_fc, output_fc)
    logger.debug("Target spatial reference: %s", spatial_ref_out.factoryCode)
    logger.debug("Using geographic transformation: %s", geographic_transform)

    if spatial_ref_in:
        arcpy.Project_management(input_fc, output_fc, spatial_ref_out, geographic_transform, spatial_ref_in)
    else:
        arcpy.Project_management(input_fc, output_fc, spatial_ref_out, geographic_transform)


def add_fields_if_not_exist(feature_class, fields_to_add):
    existing_fields = [f.name for f in arcpy.ListFields(feature_class)]

    for field_name, field_type in fields_to_add:
        if field_name not in existing_fields:
            logger.debug("Adding field: %s (%s) to %s", field_name, field_type, feature_class)
            arcpy.AddField_management(feature_class, field_name, field_type)
        else:
            logger.debug("Field '%s' already exists in %s. Skipping.", field_name, feature_class)


def calculate_grid_convergence_angle(feature_class, output_field="angle",
                                     coordinate_system="PROJECTED", method="ARITHMETIC_MEAN"):
    """
    Calculate grid convergence angle for proper annotation rotation.

    Args:
        feature_class: Input feature class
        output_field: Field to store angle values
        coordinate_system: "PROJECTED" for projected coordinate systems like Ukraine 2000 GK
        method: "ARITHMETIC_MEAN" for better accuracy with multiple features
    """
    logger.debug("Calculating grid convergence angle for: %s", feature_class)
    logger.debug("Output field: %s, coordinate system: %s, method: %s",
                output_field, coordinate_system, method)

    # Use PROJECTED coordinate system for Ukraine 2000 GK Zone 7
    arcpy.CalculateGridConvergenceAngle_cartography(
        feature_class,
        output_field,
        coordinate_system,
        method
    )

    logger.debug("Grid convergence angle calculation completed")


def fix_annotation_rotation(feature_class, angle_field="angle"):
    """
    Fix annotation rotation using calculated grid convergence angle.

    Args:
        feature_class: Feature class with annotations
        angle_field: Field containing grid convergence angles
    """
    logger.debug("Fixing annotation rotation for: %s", feature_class)

    # Check if feature class has annotations
    desc = arcpy.Describe(feature_class)
    if hasattr(desc, 'featureClass') and desc.featureClass.featureType == "Annotation":
        logger.debug("Processing annotation feature class")

        # Update annotation rotation using angle field
        with arcpy.da.UpdateCursor(feature_class, ['ANGLE', angle_field]) as cursor:
            for row in cursor:
                if row[1] is not None:  # If grid convergence angle exists
                    # Apply rotation correction
                    corrected_angle = row[0] + row[1] if row[0] is not None else row[1]
                    row[0] = corrected_angle
                    cursor.updateRow(row)

        logger.debug("Annotation rotation correction completed")
    else:
        logger.debug("Feature class is not annotation type, skipping rotation fix")


def create_gdbs_in_folders(folders_dict, gdb_name="frame.gdb"):
    logger.debug("Creating geodatabases (%d items)", len(folders_dict))
    gdb_paths = {}

    for key, folder_path in folders_dict.items():
        gdb_path = os.path.join(folder_path, gdb_name)

        if not arcpy.Exists(gdb_path):
            arcpy.CreateFileGDB_management(folder_path, gdb_name)
            logger.info("Created GDB at: %s", gdb_path)
        else:
            logger.debug("GDB already exists: %s", gdb_path)

        gdb_paths[key] = gdb_path

    return gdb_paths


def create_feature_datasets(gdb_paths, dataset_name="Frame", sr_code=5565):
    logger.info("Creating feature datasets (%d items)", len(gdb_paths))
    logger.debug("Dataset name: %s, spatial reference: %d", dataset_name, sr_code)

    sr = arcpy.SpatialReference(sr_code)
    dataset_paths = {}

    for key, gdb_path in gdb_paths.items():
        dataset_path = os.path.join(gdb_path, dataset_name)

        if not arcpy.Exists(dataset_path):
            arcpy.CreateFeatureDataset_management(gdb_path, dataset_name, sr)
            logger.debug("Created Feature Dataset: %s", dataset_path)
        else:
            logger.debug("Feature Dataset already exists: %s", dataset_path)

        dataset_paths[key] = dataset_path

    return dataset_paths
