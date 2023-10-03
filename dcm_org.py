"""
dcm_org.py

Description:
    This script organizes DICOM files based on their series description. It processes files from an input directory
    and organizes them into an output directory while maintaining the top-level folder structure of the input directory.

Usage:
    1. Modify the `input_dir_path` and `output_dir_path` variables to point to your desired input and output directories.
    2. Run the script using Python: `python dcm_org.py`

Dependencies:
    - os
    - shutil
    - pydicom
    - concurrent.futures

    pip install pydicom

Author: Jean Jimenez
"""

import os
import shutil
import pydicom
from concurrent.futures import ThreadPoolExecutor

# Specify the paths to the input and output directories
input_dir_path = r"path to input directory/ where unorganized imgs are"
output_dir_path = r"path to output directory/ where organized images output to"

def is_dicom_file(file_path):
    """
    Check if a file is a valid DICOM file.
    """
    try:
        pydicom.dcmread(file_path, stop_before_pixels=True)
        return True
    except:
        return False

def get_series_description(file_path):
    """
    Extract the series description from the DICOM metadata.
    """
    try:
        ds = pydicom.dcmread(file_path, stop_before_pixels=True)
        return ds.SeriesDescription
    except:
        return "UnknownSeries"

def handle_file(file_path, output_dir):
    """
    Handle a single DICOM file. Copy the file to the appropriate directory in the output_dir.
    """
    series_description = get_series_description(file_path)
    output_subdir = os.path.join(output_dir, series_description)
    if not os.path.exists(output_subdir):
        os.makedirs(output_subdir)

    # Convert to .dcm format if necessary
    new_file_path = file_path
    if not file_path.endswith('.dcm'):
        new_file_path = file_path.rsplit('.', 1)[0] + '.dcm'
        shutil.move(file_path, new_file_path)
    output_file_path = os.path.join(output_subdir, os.path.basename(new_file_path))
    shutil.copy(new_file_path, output_file_path)

def process_directory(dir_path, output_dir_path):
    """
    Recursively process a directory and its sub-directories.
    """
    for root, _, files in os.walk(dir_path):
        relative_root = os.path.relpath(root, dir_path)
        output_subdir = os.path.join(output_dir_path, relative_root)
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(('.dcm', '.ima')) or 'DICOMDIR' in file or is_dicom_file(file_path):
                handle_file(file_path, output_subdir)

def main():
    """
    Main function of the script. Create the ThreadPoolExecutor and schedule the tasks.
    """
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    with ThreadPoolExecutor() as executor:
        executor.submit(process_directory, input_dir_path, output_dir_path)

    print("Finished processing.")

if __name__ == "__main__":
    main()


"""

import os
import shutil
import pydicom
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


# Specify the paths to the input and output directories
input_dir_path = 'D:\dicom_input_orig'
output_dir_path = 'D:\\dicom_input'


def get_dicom_metadata(file_path):

    try:
        ds = pydicom.dcmread(file_path, stop_before_pixels=True)  # We don't need pixel data for organization
        return ds.PatientID, ds.StudyInstanceUID, ds.SeriesDescription, ds.SeriesInstanceUID
    except Exception as e:
        print(f"Failed to read DICOM metadata from {file_path}. Error: {e}")
        return None, None, None, None


def handle_file(file_path, output_dir):

    print(f"Handling file: {file_path}")
    patient_id, study_uid, series_description, series_uid = get_dicom_metadata(file_path)
    if patient_id and study_uid and series_description and series_uid:  # Only process files with complete metadata
        print(
            f"Metadata - Patient ID: {patient_id}, Study UID: {study_uid}, Series Description: {series_description}, Series UID: {series_uid}")

        # Create the new output directory with the series name
        output_dir = os.path.join(output_dir, patient_id, study_uid, series_description)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file_path = os.path.join(output_dir, os.path.basename(file_path))
        shutil.copy(file_path, output_file_path)
        print(f"Copied file to: {output_file_path}")


def main():

    print(f"Input directory: {input_dir_path}")
    print(f"Output directory: {output_dir_path}")
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(input_dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Schedule the task
                executor.submit(handle_file, file_path, output_dir_path)

    print("Finished processing.")


if __name__ == "__main__":
    main()
"""
