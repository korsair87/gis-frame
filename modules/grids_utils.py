# coding=utf-8
import os

import arcpy

from filesystem_utils import safe_shapefile_name
from logger_config import setup_logger

logger = setup_logger("grids_utils")


def generate_grids(dataset_paths, xml_template_path, gdb_name=None, dataset_name=None,
                   input_fc_name="INP_Frame",
                   grid_prefix="Grid_"):
    logger.debug("Generating coordinate grids (%d items)", len(dataset_paths))
    logger.debug("XML template: %s", xml_template_path)

    for nomencl, path in dataset_paths.items():
        if gdb_name and dataset_name:
            gdb_path = os.path.join(os.path.dirname(path), gdb_name)
            feature_dataset = os.path.join(gdb_path, dataset_name)
        else:
            feature_dataset = path

        input_layer = os.path.join(feature_dataset, input_fc_name)
        out_feature_class = os.path.join(feature_dataset, "{}{}".format(grid_prefix, safe_shapefile_name(nomencl)))

        logger.info("Generating grid for nomenclature: %s", nomencl)
        logger.debug("Input layer: %s", input_layer)
        logger.debug("Output feature class: %s", out_feature_class)

        try:
            arcpy.MakeGridsAndGraticulesLayer_cartography(
                in_template=xml_template_path,
                in_aoi=input_layer,
                input_feature_dataset=feature_dataset,
                output_layer=out_feature_class,
                name="Frame 10 000 Ukraine 2000",
                refscale="10000",
                rotation="0",
                mask_size="10 Centimeters",
                xy_tolerance="0,001 Meters",
                primary_coordinate_system=None,
                configure_layout="NO_CONFIGURELAYOUT",
                ancillary_coordinate_system_1=None,
                ancillary_coordinate_system_2=None,
                ancillary_coordinate_system_3=None,
                ancillary_coordinate_system_4=None
            )
            logger.debug("Grid generation completed for: %s", nomencl)
        except Exception as e:
            logger.error("Failed to generate grid for %s: %s", nomencl, str(e))
            raise
