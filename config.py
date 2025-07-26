# coding=utf-8
import os

BASE_WORK_FOLDER = r"D:\Work\GIS\Frames"
INPUT_FOLDER = r"!!!-IN"
OUTPUT_FOLDER = r"!!!-OUT"
FRAME_TEMPLATE_FOLDER = "ShablonFrame"

ITERATION = "3_iteration"
INPUT_SHAPEFILE_NAME = "Рамки_3черга_region.shp"
TEMPLATE_MXD_NAME = "template.mxd"
OUT_SPATIAL_REFERENCE = 5565  # Ukraine_2000_GK_Zone_7
FRAME_TEMPLATE_NAME = "Frame 10 000 Ukraine 2000 Zona 7_SID 2025.xml"

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


def get_template_xml_path():
    return os.path.join(BASE_WORK_FOLDER, FRAME_TEMPLATE_FOLDER, FRAME_TEMPLATE_NAME)
