# coding=utf-8
import os

BASE_WORK_FOLDER = r"D:\Work\GIS\Frames"
INPUT_FOLDER = r"!!!-IN"
OUTPUT_FOLDER = r"!!!-OUT"
TEMPLATE_MXD_NAME = "template.mxd"
ITERATION = "2_iteration"

INPUT_SHAPEFILE_NAME = "Рамки_2черга_region.shp"
GDB_NAME = "NewWorkspace.gdb"

EXPORT_FIELD = "NOMENCL"
SHAPE_SUBFOLDER = "shp"


def get_input_path():
    return os.path.join(BASE_WORK_FOLDER, INPUT_FOLDER, ITERATION, INPUT_SHAPEFILE_NAME)


def get_template_mxd_path():
    return os.path.join(BASE_WORK_FOLDER, INPUT_FOLDER, ITERATION, TEMPLATE_MXD_NAME)


def get_output_folder():
    return os.path.join(BASE_WORK_FOLDER, OUTPUT_FOLDER, ITERATION)


def get_output_gdb():
    return os.path.join(get_output_folder(), GDB_NAME)
