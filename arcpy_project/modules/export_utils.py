import os
import arcpy

from filesystem_utils import safe_shapefile_name


def export_by_field_values(input_fc, field_name, folders_dict):
    for val, folder_path in folders_dict.items():
        shp_name = "{}.shp".format(safe_shapefile_name(val))
        where_clause = "{} = '{}'".format(field_name, val)
        output_path = os.path.join(folder_path, shp_name)
        arcpy.AddMessage("Exporting '{}' to '{}'".format(val, output_path))
        arcpy.FeatureClassToFeatureClass_conversion(input_fc, folder_path, shp_name, where_clause)
