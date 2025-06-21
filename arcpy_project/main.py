# coding=utf-8
import os
import sys

import arcpy

from modules.gdb_utils import create_gdb, copy_shapefile, add_fields_if_not_exist

reload(sys)
sys.setdefaultencoding("utf-8")


def prepare_data():
    parent_folder = r"D:\Work\GIS\Frames\!!!-IN\Рамки_2_черга_region"
    input_shp_name = "Рамки_2черга_region.shp"
    input_shp = os.path.join(parent_folder, input_shp_name)

    gdb_name = "NewWorkspace.gdb"
    new_gdb = create_gdb(parent_folder, gdb_name)

    fc_name = "CopiedFrames"
    output_fc = os.path.join(new_gdb, fc_name)

    copy_shapefile(input_shp, output_fc)

    sr_out = arcpy.SpatialReference(5565)  # Ukraine_2000_GK_Zone_5
    sr_in = arcpy.SpatialReference(4326)  # WGS 84

    reproject_feature_class(intermediate_fc, output_fc, sr_out, sr_in)

    fields = [("angle", "DOUBLE"), ("nomenclature", "TEXT")]

    add_fields_if_not_exist(output_fc, fields)


if __name__ == "__main__":
    prepare_data()
