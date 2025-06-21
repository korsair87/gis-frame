# coding=utf-8
import os
import sys

import arcpy

from modules.folder_utils import create_folders_for_field_values, create_subfolders
from modules.export_utils import export_by_field_values, get_unique_values
from modules.file_utils import copy_files_to_folders
from modules.gdb_utils import create_gdb, copy_shapefile, add_fields_if_not_exist, re_project_feature_class, \
    calculate_grid_convergence_angle

import config

reload(sys)
sys.setdefaultencoding("utf-8")


def prepare_data():
    input_shp = config.get_input_path()
    new_gdb_folder = config.get_output_folder()

    if not os.path.exists(new_gdb_folder):
        os.makedirs(new_gdb_folder)

    new_gdb = create_gdb(new_gdb_folder, config.GDB_NAME)

    intermediate_fc = os.path.join(new_gdb, "frame_region_original")
    output_fc = os.path.join(new_gdb, "frame")

    copy_shapefile(input_shp, intermediate_fc)

    sr_in = arcpy.SpatialReference(4284)  # Pulkovo 1942
    sr_out = arcpy.SpatialReference(5565)  # Ukraine_2000_GK_Zone_7
    re_project_feature_class(intermediate_fc, output_fc, sr_out, sr_in)

    fields = [("angle", "DOUBLE"), ("nomenclature", "TEXT")]
    add_fields_if_not_exist(output_fc, fields)

    calculate_grid_convergence_angle(output_fc, output_field="angle")


def create_export_folders():
    input_fc = os.path.join(config.get_output_gdb(), "frame")
    output_base_folder = config.get_output_folder()
    field_name = config.EXPORT_FIELD

    unique_values = get_unique_values(input_fc, field_name)
    folders_dict = create_folders_for_field_values(output_base_folder, unique_values)
    return folders_dict


def extract_shapefiles(folders_dict):
    input_fc = os.path.join(config.get_output_gdb(), "frame")
    field_name = config.EXPORT_FIELD

    export_by_field_values(input_fc, field_name, folders_dict)


def copy_mxd_files(folders_dict):
    template_path = config.get_template_mxd_path()
    copy_files_to_folders(template_path, folders_dict)


if __name__ == "__main__":
    prepare_data()
    folders = create_export_folders()
    shp_folders = create_subfolders(folders, config.INPUT_SHAPEFILE_NAME)
    extract_shapefiles(shp_folders)
    copy_mxd_files(folders)
