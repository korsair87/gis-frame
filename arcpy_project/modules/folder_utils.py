import os


def create_folders_for_field_values(base_folder, values_list, subfolder_name="shp"):
    folders = {}
    for val in values_list:
        folder_path = os.path.join(base_folder, val, subfolder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        folders[val] = folder_path
    return folders
