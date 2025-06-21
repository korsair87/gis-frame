# coding=utf-8
import os
import arcpy


def safe_shapefile_name(name):
    if not name:
        return "noname"
    safe_name = name.replace("-", "_")
    safe_name = safe_name.strip()
    return safe_name


def get_unique_values(input_fc, field_name):
    unique_values = set()
    with arcpy.da.SearchCursor(input_fc, [field_name]) as cursor:
        for row in cursor:
            val = row[0]
            if val:
                unique_values.add(val)
    return sorted(unique_values)


def create_folders_for_field_values(base_folder, values_list, subfolder_name="shp"):
    folders = {}
    for val in values_list:
        folder_path = os.path.join(base_folder, val, subfolder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        folders[val] = folder_path
    return folders


def export_by_field_values(input_fc, field_name, folders_dict):
    for val, folder_path in folders_dict.items():
        shp_name = "{}.shp".format(safe_shapefile_name(val))
        where_clause = "{} = '{}'".format(field_name, val)
        arcpy.AddMessage("Exporting '{}' to '{}'".format(val, os.path.join(folder_path, shp_name)))
        arcpy.FeatureClassToFeatureClass_conversion(input_fc, folder_path, shp_name, where_clause)
