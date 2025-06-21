# coding=utf-8
import os


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
    for val, folder_path in folders_dict.items():
        subfolder_path = os.path.join(folder_path, subfolder_name)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        subfolders[val] = subfolder_path
    return subfolders

