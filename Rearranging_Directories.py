import os
import shutil
import re

def extract_waframe_files(source_dir, output_dir):
    """
    For each patient folder in source_dir:
    - Copy only 'waframeXX.nii' files to corresponding folder in output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)

    for folder_name in os.listdir(source_dir):
        patient_folder = os.path.join(source_dir, folder_name)
        if not os.path.isdir(patient_folder):
            continue  # Skip if it's not a directory

        # Get all waframeXX.nii files
        waframe_files = [
            f for f in os.listdir(patient_folder)
            if re.match(r"waframe\d+\.nii", f, re.IGNORECASE)
        ]

        if not waframe_files:
            print(f"No waframe files in: {folder_name}")
            continue

        # Create corresponding output subfolder
        output_subfolder = os.path.join(output_dir, folder_name)
        os.makedirs(output_subfolder, exist_ok=True)

        for file in waframe_files:
            src_file = os.path.join(patient_folder, file)
            dst_file = os.path.join(output_subfolder, file[2:])
            shutil.copy2(src_file, dst_file)
            print(f"Copied: {src_file} → {dst_file}")

if __name__ == "__main__":
    source_dir = r"C:\Users\ASUS\Documents\dPET_nifti\PET"
    output_dir = r"C:\Users\ASUS\Documents\dPET_nifti\sorted_PET & MR nifti"

    extract_waframe_files(source_dir, output_dir)