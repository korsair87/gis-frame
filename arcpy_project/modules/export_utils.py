import os
import arcpy

from filesystem_utils import safe_shapefile_name


def extract_by_field_values(input_fc, field_name, folders_dict):
    for val, folder_path in folders_dict.items():
        shp_name = "{}.shp".format(safe_shapefile_name(val))
        where_clause = "{} = '{}'".format(field_name, val)
        output_path = os.path.join(folder_path, shp_name)
        arcpy.AddMessage("Exporting '{}' to '{}'".format(val, output_path))
        arcpy.FeatureClassToFeatureClass_conversion(input_fc, folder_path, shp_name, where_clause)


def extract_by_field_values_to_gdb(input_fc, field_name, folders_dict, gdb_name="frame.gdb", dataset_name="Frame",
                                   out_name_pattern=None):
    for val, folder_path in folders_dict.items():
        gdb_path = os.path.join(folder_path, gdb_name)
        feature_dataset = os.path.join(gdb_path, dataset_name)

        if not arcpy.Exists(feature_dataset):
            arcpy.AddError("Feature Dataset not found: {}".format(feature_dataset))
            continue

        # Use for unique "{val}"
        if out_name_pattern:
            out_name = out_name_pattern.format(val=safe_shapefile_name(val))
        else:
            out_name = safe_shapefile_name(val)

        output_fc = os.path.join(feature_dataset, out_name)
        if arcpy.Exists(output_fc):
            arcpy.Delete_management(output_fc)

        where_clause = "{} = '{}'".format(field_name, val)

        arcpy.AddMessage("Exporting '{}' to '{}'".format(val, output_fc))
        arcpy.FeatureClassToFeatureClass_conversion(
            input_fc,
            feature_dataset,
            out_name,
            where_clause
        )
