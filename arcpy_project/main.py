# coding=utf-8
import os
import sys

import arcpy

from modules.folder_utils import create_folders_for_field_values
from modules.export_utils import export_by_field_values, get_unique_values
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


def export_file_by_nomenclature():
    input_fc = os.path.join(config.get_output_gdb(), "frame")
    output_base_folder = config.get_output_folder()
    field_name = config.EXPORT_FIELD
    subfolder_name = config.EXPORT_SUBFOLDER

    unique_values = get_unique_values(input_fc, field_name)

    folders_dict = create_folders_for_field_values(output_base_folder, unique_values, subfolder_name)

    export_by_field_values(input_fc, field_name, folders_dict)


if __name__ == "__main__":
    prepare_data()
    export_file_by_nomenclature()
