# dcm_svr_tools

## Author: Jean Jimenez

---

## Introduction
This repository contains two Python scripts, `rename_studies_anum.py` and `dcm_org.py`, which are designed to work on a DICOM server to organize, rename, and restructure DICOM files and folders. These tools are particularly useful for radiology research and can be integrated into existing DICOM processing pipelines.

---

## Dependencies
- Python 3.x
- pydicom
- os
- shutil
- concurrent.futures

### External Tools
- DCMTK (DICOM Toolkit)

### Package Installation
For Python package dependencies, you can install them using pip:
```bash
pip install -r requirements.txt
```

---

## `rename_studies_anum.py`

### Description
This script organizes DICOM studies based on their accession numbers. It scans through a base directory containing multiple subdirectories, each representing a DICOM study. The script then renames these folders based on the accession numbers found in the DICOM files.

### Usage
1. Update the `user_input_path` variable to point to the directory containing the DICOM study folders.
2. Run the script using Python:
```bash
python rename_studies_anum.py
```

---

## `dcm_org.py`

### Description
This script organizes DICOM files based on their series description. It processes files from an input directory and organizes them into an output directory while maintaining the top-level folder structure of the input directory.

### Usage
1. Modify the `input_dir_path` and `output_dir_path` variables to point to your desired input and output directories.
2. Run the script using Python:
```bash
python dcm_org.py
```

---

## Citations
- [pydicom](https://github.com/pydicom/pydicom): A Python package to work with DICOM files.
- [DCMTK](https://dicom.offis.de/dcmtk.php.en): DICOM Toolkit for processing DICOM files.

