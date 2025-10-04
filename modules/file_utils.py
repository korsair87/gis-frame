import os
import shutil
from logger_config import setup_logger

logger = setup_logger("file_utils")


def copy_files_to_folders(files, folders_dict):
    if isinstance(files, str):
        files = [files]

    logger.debug("Copying %d files to %d folders", len(files), len(folders_dict))

    for name, folder_path in folders_dict.items():
        for file_path in files:
            ext = os.path.splitext(file_path)[1]
            dest_path = os.path.join(folder_path, "{}{}".format(name, ext))
            logger.info("Copying %s to %s", file_path, dest_path)
            shutil.copyfile(file_path, dest_path)
