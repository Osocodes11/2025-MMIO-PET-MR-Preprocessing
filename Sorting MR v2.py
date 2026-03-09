import os
import shutil
import re

def move_and_rename_mr_files(source_dir, pet_output_dir):
    for filename in os.listdir(source_dir):
        # Only process files that start with 'w' and end with '.nii'
        if not filename.lower().startswith('w') or not filename.lower().endswith('.nii'):
            continue

        # Extract patient ID and date after 'y_'
        match = re.match(r"w(.+)\.nii", filename)
        if match:
            patient_id_date = match.group(1)

            # Locate corresponding PET subfolder
            patient_folder = os.path.join(pet_output_dir, patient_id_date)
            if os.path.exists(patient_folder):
                src_file = os.path.join(source_dir, filename)
                dst_file = os.path.join(patient_folder, "MRI.nii")

                # Move and rename the MR file
                shutil.copy2(src_file, dst_file)
                print(f"Moved and renamed: {src_file} → {dst_file}")
            else:
                print(f"Skipped: No PET folder found for {patient_id_date}")

# Customize your paths below:
mr_source_dir = r"C:\Users\ASUS\Downloads\dPET_nifti\PET_MR_0627\MR_0627"
pet_output_dir = r"C:\Users\ASUS\Downloads\dPET_nifti\PET_MR_0627\PET & MR_0627"

move_and_rename_mr_files(mr_source_dir, pet_output_dir)
