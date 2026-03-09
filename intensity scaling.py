import os
import SimpleITK as sitk
import numpy as np

# Define paths
input_root = r'C:\Users\ASUS\Documents\dPET_nifti\Final Training Set (nifti)'
output_root = r'C:\Users\ASUS\Documents\dPET_nifti\Normalized FTS'

os.makedirs(output_root, exist_ok=True)

# List patient subfolders
patient_folders = [f for f in os.listdir(input_root) if os.path.isdir(os.path.join(input_root, f))]

# Loop through each patient
for patient_name in patient_folders:
    input_subfolder = os.path.join(input_root, patient_name)
    output_subfolder = os.path.join(output_root, patient_name)
    os.makedirs(output_subfolder, exist_ok=True)

    # Find only frameXX.nii files (skip MRI)
    nii_files = [f for f in os.listdir(input_subfolder) if f.startswith('frame') and f.endswith('.nii')]

    for filename in nii_files:
        nii_path = os.path.join(input_subfolder, filename)
        print(nii_path)

        # Load image
        img = sitk.ReadImage(nii_path)
        data = sitk.GetArrayFromImage(img).astype(np.float64)

        # Default scale = 1.0
        scl_slope = 1.0

        # Try to extract scl_slope from metadata
        if img.HasMetaDataKey("scl_slope"):
            scl_slope = float(img.GetMetaData("scl_slope"))

        if scl_slope == 0:
            print(f"⚠️ Skipping {filename}: normalization constant is zero")
            continue

        # Normalize
        norm_data = data / scl_slope
        print(f"scl_slope: {scl_slope}")
        print(f"Mean before: {np.mean(data):.4f}, after: {np.mean(norm_data):.4f}")
        print("-----------------")

        # Create normalized image
        norm_img = sitk.GetImageFromArray(norm_data)
        norm_img.CopyInformation(img)
        norm_img = sitk.Cast(norm_img, sitk.sitkFloat64)

        # Optional: Reset slope/intercept (not required, but clean)
        norm_img.SetMetaData("scl_slope", "1")
        norm_img.SetMetaData("scl_inter", "0")

        # Save
        out_path = os.path.join(output_subfolder, filename)
        sitk.WriteImage(norm_img, out_path)

print("✅ All frameXX PET files have been normalized and saved.")
