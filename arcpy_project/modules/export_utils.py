# coding=utf-8
import os
import arcpy


def safe_shapefile_name(name):
    if not name:
        return "noname"
    safe_name = name.replace("-", "_")
    safe_name = safe_name.strip()
    return safe_name


def export_by_nomencl(input_fc, output_base_folder, field_name="NOMENCL", subfolder_name="shp"):
    unique_values = set()
    with arcpy.da.SearchCursor(input_fc, [field_name]) as cursor:
        for row in cursor:
            val = row[0]
            if val:
                unique_values.add(val)

    for val in sorted(unique_values):
        folder_path = os.path.join(output_base_folder, val, subfolder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        shp_name = "{}.shp".format(safe_shapefile_name(val))

        where_clause = "{} = '{}'".format(field_name, val)

        arcpy.AddMessage("Exporting '{}' to '{}'...".format(val, os.path.join(folder_path, shp_name)))
        arcpy.FeatureClassToFeatureClass_conversion(input_fc, folder_path, shp_name, where_clause)
