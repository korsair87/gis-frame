# coding=utf-8
import os
import sys

import arcpy

from modules.export_utils import export_by_nomencl
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


def export_grids_by_field():
    from config import EXPORT_FIELD, EXPORT_SUBFOLDER
    from config import get_output_folder, get_output_gdb

    output_fc = os.path.join(get_output_gdb(), "frame")

    export_by_nomencl(
        input_fc=output_fc,
        output_base_folder=get_output_folder(),
        field_name=EXPORT_FIELD,
        subfolder_name=EXPORT_SUBFOLDER
    )


if __name__ == "__main__":
    prepare_data()
    export_grids_by_field()
