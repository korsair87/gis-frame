import arcpy
from logger_config import setup_logger

logger = setup_logger("field_utils")


def get_unique_values(input_fc, field_name):
    logger.debug("Getting unique values from field '%s' in %s", field_name, input_fc)
    values = set()
    with arcpy.da.SearchCursor(input_fc, [field_name]) as cursor:
        for row in cursor:
            if row[0]:
                values.add(row[0])

    sorted_values = sorted(values)
    logger.debug("Found %d unique values in field '%s'", len(sorted_values), field_name)
    return sorted_values


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
    logger.debug("Getting unique values with range from field '%s' in %s", field_name, input_fc)
    logger.debug("Range: start=%s, end=%s", start_index, end_index)

    values = set()
    with arcpy.da.SearchCursor(input_fc, [field_name]) as cursor:
        for row in cursor:
            if row[0]:
                values.add(row[0])

    sorted_values = sorted(values)
    logger.debug("Total unique values found: %d", len(sorted_values))

    # Apply range filtering if specified
    if start_index is not None or end_index is not None:
        start_idx = (start_index - 1) if start_index is not None else 0
        end_idx = end_index if end_index is not None else len(sorted_values)
        sorted_values = sorted_values[start_idx:end_idx]
        logger.debug("Applied range filter: returning %d values (%d-%d)",
                   len(sorted_values), start_index or 1, end_index or len(values))

    return sorted_values
