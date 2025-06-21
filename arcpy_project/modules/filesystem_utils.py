import os


def safe_shapefile_name(name):
    if not name:
        return "noname"
    return name.replace("-", "_").strip()


def create_folders_for_field_values(base_folder, values_list):
    folders = {}
    for val in values_list:
        folder_path = os.path.join(base_folder, val)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        folders[val] = folder_path
    return folders


def create_subfolders(folders_dict, subfolder_name):
    subfolders = {}
    for val, base_path in folders_dict.items():
        sub_path = os.path.join(base_path, subfolder_name)
        if not os.path.exists(sub_path):
            os.makedirs(sub_path)
        subfolders[val] = sub_path
    return subfolders
