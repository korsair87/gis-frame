# coding=utf-8
import arcpy
import os


def create_gdb(parent_folder, gdb_name):
    new_gdb = os.path.join(parent_folder, gdb_name)
    if not arcpy.Exists(new_gdb):
        arcpy.CreateFileGDB_management(parent_folder, gdb_name)
    return new_gdb


def copy_shapefile(input_shp, output_fc):
    if arcpy.Exists(output_fc):
        arcpy.AddMessage("Output feature class exists. Deleting...")
        arcpy.Delete_management(output_fc)

    arcpy.AddMessage("Copying shapefile...")
    arcpy.CopyFeatures_management(input_shp, output_fc)


def re_project_feature_class(input_fc, output_fc, spatial_ref_out, spatial_ref_in=None, geographic_transform=""):
    if arcpy.Exists(output_fc):
        arcpy.AddMessage("Output feature class exists. Deleting...")
        arcpy.Delete_management(output_fc)

    arcpy.AddMessage("Projecting feature class...")
    if spatial_ref_in:
        arcpy.Project_management(input_fc, output_fc, spatial_ref_out, geographic_transform, spatial_ref_in)
    else:
        arcpy.Project_management(input_fc, output_fc, spatial_ref_out)


def add_fields_if_not_exist(feature_class, fields_to_add):
    existing_fields = [f.name for f in arcpy.ListFields(feature_class)]

    for field_name, field_type in fields_to_add:
        if field_name not in existing_fields:
            arcpy.AddMessage("Adding field: {} ({})".format(field_name, field_type))
            arcpy.AddField_management(feature_class, field_name, field_type)
        else:
            arcpy.AddMessage("Field '{}' already exists. Skipping.".format(field_name))


def calculate_grid_convergence_angle(feature_class, output_field="angle",
                                     coordinate_system="GEOGRAPHIC", method="NONE"):
    arcpy.AddMessage("Calculating grid convergence angle for '{}'...".format(feature_class))
    arcpy.CalculateGridConvergenceAngle_cartography(
        feature_class,
        output_field,
        coordinate_system,
        method
    )
    arcpy.AddMessage("Calculation completed.")


def create_gdbs_in_folders(folders_dict, gdb_name="frame.gdb"):
    gdb_paths = {}

    for key, folder_path in folders_dict.items():
        gdb_path = os.path.join(folder_path, gdb_name)

        if not arcpy.Exists(gdb_path):
            arcpy.CreateFileGDB_management(folder_path, gdb_name)
            arcpy.AddMessage("Created GDB at: {}".format(gdb_path))
        else:
            arcpy.AddMessage("GDB already exists: {}".format(gdb_path))

        gdb_paths[key] = gdb_path

    return gdb_paths


def create_feature_datasets(gdb_paths, dataset_name="Frame", sr_code=5565):
    sr = arcpy.SpatialReference(sr_code)
    dataset_paths = {}

    for key, gdb_path in gdb_paths.items():
        dataset_path = os.path.join(gdb_path, dataset_name)

        if not arcpy.Exists(dataset_path):
            arcpy.CreateFeatureDataset_management(gdb_path, dataset_name, sr)
            arcpy.AddMessage("Created Feature Dataset: {}".format(dataset_path))
        else:
            arcpy.AddMessage("Feature Dataset already exists: {}".format(dataset_path))

        dataset_paths[key] = dataset_path

    return dataset_paths