# Author: Jean Jimenez

import os
import shutil
import pydicom
from pydicom.errors import InvalidDicomError

# Path to unlabeled study folders
user_input_path = r"path to unlabeled study folders"


def get_accession_number(dicom_file):
    """
    Extracts the accession number from a DICOM file.

    Parameters:
        dicom_file (str): The path to the DICOM file.

    Returns:
        str: The accession number if available, otherwise None.
    """
    try:
        ds = pydicom.dcmread(dicom_file)
        accession_number = ds.AccessionNumber
        return accession_number
    except (InvalidDicomError, KeyError, PermissionError):
        return None


def merge_subdirs(src, dst):
    """
    Merges all files and subdirectories from source to destination directory.

    Parameters:
        src (str): The source directory.
        dst (str): The destination directory.
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if os.path.isdir(s):
            if not os.path.exists(d):
                os.makedirs(d)
            merge_subdirs(s, d)
        else:
            shutil.copy2(s, d)


def rename_files_to_dcm(dirpath):
    """
    Renames all files in the directory to have a .dcm extension.

    Parameters:
        dirpath (str): The directory containing the files.
    """
    for filename in os.listdir(dirpath):
        if not filename.endswith('.dcm'):
            old_file_path = os.path.join(dirpath, filename)
            new_file_path = os.path.join(dirpath, filename + '.dcm')
            os.rename(old_file_path, new_file_path)


def merge_and_rename_folder(dirpath, base_path):
    """
    Merges and renames a folder based on accession numbers in DICOM files.

    Parameters:
        dirpath (str): The directory containing the DICOM files.
        base_path (str): The base directory where new folders will be created.

    Returns:
        bool: True if folder is successfully merged and renamed, otherwise False.
    """
    rename_files_to_dcm(dirpath)
    for filename in os.listdir(dirpath):
        if filename.endswith('.dcm'):
            dicom_file = os.path.join(dirpath, filename)
            accession_number = get_accession_number(dicom_file)

            if accession_number is not None:
                new_folder_name = os.path.join(base_path, accession_number)

                if not os.path.exists(new_folder_name):
                    os.makedirs(new_folder_name)

                merge_subdirs(dirpath, new_folder_name)

                print(f"Merged and renamed folder {dirpath} to {new_folder_name}")
                return True
    return False


def merge_folders_by_accession_number(base_path):
    """
    Iterates through all folders in a base directory and merges them based on accession numbers.

    Parameters:
        base_path (str): The base directory containing study folders.
    """
    for dirpath, _, _ in os.walk(base_path):
        merge_and_rename_folder(dirpath, base_path)


def process_studies_folder(base_path):
    """
    Entry point for processing a base directory containing multiple study folders.

    Parameters:
        base_path (str): The base directory containing study folders.
    """
    if os.path.exists(base_path):
        merge_folders_by_accession_number(base_path)
    else:
        print("The provided path does not exist. Please check the path and try again.")


if __name__ == "__main__":
    process_studies_folder(user_input_path)
