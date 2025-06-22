import os
import shutil


def copy_files_to_folders(files, folders_dict):
    if isinstance(files, str):
        files = [files]

    for name, folder_path in folders_dict.items():
        for file_path in files:
            ext = os.path.splitext(file_path)[1]
            dest_path = os.path.join(folder_path, "{}{}".format(name, ext))
            shutil.copyfile(file_path, dest_path)
