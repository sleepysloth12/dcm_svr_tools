import os
import shutil
import pydicom
from pydicom.errors import InvalidDicomError

user_input_path=r"path to unlabled study folders"

def get_accession_number(dicom_file):
    try:
        ds = pydicom.dcmread(dicom_file)
        accession_number = ds.AccessionNumber
        return accession_number
    except (InvalidDicomError, KeyError, PermissionError):
        return None

def merge_subdirs(src, dst):
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
    for filename in os.listdir(dirpath):
        if not filename.endswith('.dcm'):
            old_file_path = os.path.join(dirpath, filename)
            new_file_path = os.path.join(dirpath, filename + '.dcm')
            os.rename(old_file_path, new_file_path)

def merge_and_rename_folder(dirpath, base_path):
    rename_files_to_dcm(dirpath)  # Rename files to have .dcm extension
    for filename in os.listdir(dirpath):
        if filename.endswith('.dcm'):
            dicom_file = os.path.join(dirpath, filename)
            accession_number = get_accession_number(dicom_file)
            
            if accession_number is not None:
                new_folder_name = os.path.join(base_path, accession_number)
                
                # Create new folder if it doesn't exist
                if not os.path.exists(new_folder_name):
                    os.makedirs(new_folder_name)
                
                # Merge all files and sub-directories from the current folder to the new folder
                merge_subdirs(dirpath, new_folder_name)
                
                print(f"Merged and renamed folder {dirpath} to {new_folder_name}")
                return True  # Folder merged and renamed successfully
    return False  # No DICOM file found or folder not merged

def merge_folders_by_accession_number(base_path):
    for dirpath, _, _ in os.walk(base_path):
        merge_and_rename_folder(dirpath, base_path)

def process_studies_folder(base_path):
    if os.path.exists(base_path):
        merge_folders_by_accession_number(base_path)
    else:
        print("The provided path does not exist. Please check the path and try again.")

# Example usage
if __name__ == "__main__":
    
    process_studies_folder(user_input_path)
