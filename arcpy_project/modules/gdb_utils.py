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
