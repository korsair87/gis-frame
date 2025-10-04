# coding=utf-8
import os
import sys

import arcpy

from modules.grids_utils import generate_grids
from modules.field_utils import get_unique_values, get_unique_values_with_range
from modules.filesystem_utils import create_folders_for_field_values
from modules.export_utils import extract_by_field_values_to_gdb
from modules.file_utils import copy_files_to_folders
from modules.gdb_utils import create_gdb, copy_shapefile, add_fields_if_not_exist, re_project_feature_class, \
    calculate_grid_convergence_angle, create_gdbs_in_folders, create_feature_datasets

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
    output_fc = os.path.join(new_gdb, "frame_work")

    copy_shapefile(input_shp, intermediate_fc)

    sr_in = arcpy.SpatialReference(4284)  # Pulkovo 1942
    sr_out = arcpy.SpatialReference(config.OUT_SPATIAL_REFERENCE)
    re_project_feature_class(intermediate_fc, output_fc, sr_out, sr_in)

    fields = [("angle", "DOUBLE"), ("nomenclature", "TEXT")]
    add_fields_if_not_exist(output_fc, fields)

    calculate_grid_convergence_angle(output_fc, output_field="angle")


def create_export_folders():
    input_fc = os.path.join(config.get_output_gdb(), "frame_work")
    output_base_folder = config.get_output_folder()
    field_name = config.EXPORT_FIELD

    if config.ENABLE_FRAME_RANGE:
        unique_values = get_unique_values_with_range(
            input_fc, field_name,
            config.FRAME_START,
            config.FRAME_END
        )
        print("Processing frames {0}-{1} ({2} total frames)".format(
            config.FRAME_START, config.FRAME_END, len(unique_values)
        ))
    else:
        unique_values = get_unique_values(input_fc, field_name)
        print("Processing all frames ({0} total frames)".format(len(unique_values)))

    folders_dict = create_folders_for_field_values(output_base_folder, unique_values)
    return folders_dict


def extract_frames_to_gdb(folders_dict):
    input_fc = os.path.join(config.get_output_gdb(), "frame_work")
    field_name = config.EXPORT_FIELD

    extract_by_field_values_to_gdb(input_fc, field_name, folders_dict, gdb_name="frame.gdb", dataset_name="Frame",
                                   out_name_pattern="INP_Frame")


def copy_mxd_files(folders_dict):
    template_path = config.get_template_mxd_path()
    copy_files_to_folders(template_path, folders_dict)


def generate_all_grids(data_set_paths):
    xml_template = config.get_template_xml_path()

    generate_grids(
        dataset_paths=data_set_paths,
        xml_template_path=xml_template,
        gdb_name=None,
        dataset_name=None,
        input_fc_name="INP_Frame",
        grid_prefix="Grid_"
    )


if __name__ == "__main__":
    prepare_data()
    folders = create_export_folders()
    gdb_paths = create_gdbs_in_folders(folders)
    dataset_paths = create_feature_datasets(gdb_paths, sr_code=config.OUT_SPATIAL_REFERENCE)
    extract_frames_to_gdb(folders)
    generate_all_grids(dataset_paths)
    copy_mxd_files(folders)
