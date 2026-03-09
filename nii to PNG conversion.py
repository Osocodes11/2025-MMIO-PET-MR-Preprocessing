import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import shutil

def save_slices(data, output_folder, base_filename):
    offset = 2  # number of slices before/after sample positions

    axis_lengths = {
        'axial': data.shape[2],
        'coronal': data.shape[1],
        'sagittal': data.shape[0]
    }

    for axis, length in axis_lengths.items():
        step = length // 6
        slice_indices = list(range(offset, length - offset, step))[:6]  # 6 slices evenly spread

        for i in slice_indices:
            if axis == 'axial':
                slice_2d = data[:, :, i]
            elif axis == 'coronal':
                slice_2d = data[:, i, :]
            elif axis == 'sagittal':
                slice_2d = data[i, :, :]

            slice_norm = 255 * (slice_2d - np.min(slice_2d)) / (np.ptp(slice_2d) + 1e-6)
            slice_uint8 = slice_norm.astype(np.uint8)

            png_filename = f"{base_filename}_{axis}_slice{i}.png"
            png_path = os.path.join(output_folder, png_filename)

            plt.figure(figsize=(6, 6))
            plt.axis('off')
            plt.imshow(slice_uint8, cmap="viridis", vmin=0, vmax=255)
            plt.savefig(png_path, bbox_inches='tight', pad_inches=0)
            plt.close()
            print(f"Saved PNG: {png_path}")

def convert_nii_to_png_all_axes(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".nii") or file.endswith(".nii.gz"):
                nii_path = os.path.join(root, file)

                # Relative path from input_dir root
                rel_path = os.path.relpath(root, input_dir)
                output_subfolder = os.path.join(output_dir, rel_path)
                os.makedirs(output_subfolder, exist_ok=True)

                # Copy NIfTI file to output location (optional, keeps originals safe)
                copied_nii_path = os.path.join(output_subfolder, file)
                shutil.copy2(nii_path, copied_nii_path)

                try:
                    img = nib.load(copied_nii_path)
                    data = img.get_fdata()

                    if file.endswith(".nii.gz"):
                        base_filename = file[:-7]
                    else:
                        base_filename = file[:-4]

                    save_slices(data, output_subfolder, base_filename)

                except Exception as e:
                    print(f"Failed to process {copied_nii_path}: {e}")

# Define your input/output paths
input_directory = r"C:\Users\ASUS\Downloads\dPET_nifti\PET_MR_0627\PET & MR_0627"
output_png_dir = r"C:\Users\ASUS\Downloads\dPET_nifti\PET_MR_0627\png_0627"

convert_nii_to_png_all_axes(input_directory, output_png_dir)
