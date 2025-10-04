import arcpy


def get_unique_values(input_fc, field_name):
    values = set()
    with arcpy.da.SearchCursor(input_fc, [field_name]) as cursor:
        for row in cursor:
            if row[0]:
                values.add(row[0])
    return sorted(values)


def get_unique_values_with_range(input_fc, field_name, start_index=None, end_index=None):
    """
    Get unique values from a field with optional range filtering.

    Args:
        input_fc: Input feature class
        field_name: Field name to get values from
        start_index: Start index (1-based, inclusive)
        end_index: End index (1-based, inclusive)

    Returns:
        Sorted list of unique values within the specified range
    """
    values = set()
    with arcpy.da.SearchCursor(input_fc, [field_name]) as cursor:
        for row in cursor:
            if row[0]:
                values.add(row[0])

    sorted_values = sorted(values)

    # Apply range filtering if specified
    if start_index is not None or end_index is not None:
        start_idx = (start_index - 1) if start_index is not None else 0
        end_idx = end_index if end_index is not None else len(sorted_values)
        sorted_values = sorted_values[start_idx:end_idx]

    return sorted_values
