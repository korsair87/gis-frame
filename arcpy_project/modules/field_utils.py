import arcpy


def get_unique_values(input_fc, field_name):
    values = set()
    with arcpy.da.SearchCursor(input_fc, [field_name]) as cursor:
        for row in cursor:
            if row[0]:
                values.add(row[0])
    return sorted(values)
