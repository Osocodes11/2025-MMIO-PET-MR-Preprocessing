import os
import nibabel as nib
import numpy as np
import re

def load_and_sort_frames(folder):
    nii_files = [f for f in os.listdir(folder) if re.match(r'frame\d{2}\.nii(\.gz)?$', f)]
    nii_files.sort()  # Assumes frame01 to frame33
    if len(nii_files) < 33:
        print(f"⚠️ Skipping {folder}: only {len(nii_files)} frames found")
        return None, None, None

    data_list = []
    path_list = []

    for f in nii_files[:33]:
        path = os.path.join(folder, f)
        img = nib.load(path)
        data = img.get_fdata()
        data_list.append(data)
        path_list.append(path)

    sample_img = nib.load(path_list[0])
    return data_list, sample_img, nii_files[:33]

def save_single_frame(data, ref_img, output_path):
    new_img = nib.Nifti1Image(data, affine=ref_img.affine, header=ref_img.header)
    nib.save(new_img, output_path)

def save_slices_as_png(volume, output_folder, base_name, axis, vmin=None, vmax=None):
    import matplotlib.pyplot as plt
    os.makedirs(output_folder, exist_ok=True)

    axis_length = volume.shape[axis]
    num_slices = 6
    step = axis_length // (num_slices + 1)

    for idx in range(1, num_slices + 1):
        slice_index = idx * step

        if axis == 0:
            slice_img = volume[slice_index, :, :]
            view = 'sagittal'
        elif axis == 1:
            slice_img = volume[:, slice_index, :]
            view = 'coronal'
        elif axis == 2:
            slice_img = volume[:, :, slice_index]
            view = 'axial'
        else:
            continue

        # Normalize for display
        slice_norm = 255 * (slice_img - np.min(slice_img)) / (np.ptp(slice_img) + 1e-6)
        slice_uint8 = slice_norm.astype(np.uint8)

        plt.figure(figsize=(6, 6))
        plt.imshow(np.rot90(slice_img), cmap="viridis", vmin=vmin, vmax=vmax)
        plt.axis("off")

        filename = os.path.join(output_folder, f"{base_name}_{view}_slice{slice_index}.png")
        plt.savefig(filename, bbox_inches='tight', pad_inches=0)
        plt.close()

def generate_pngs_for_frame(nii_path, output_folder, vmin=None, vmax=None):
    img = nib.load(nii_path)
    data = img.get_fdata()

    save_slices_as_png(data, output_folder, base_name="frame", axis=0, vmin=vmin, vmax=vmax)  # sagittal
    save_slices_as_png(data, output_folder, base_name="frame", axis=1, vmin=vmin, vmax=vmax)  # coronal
    save_slices_as_png(data, output_folder, base_name="frame", axis=2, vmin=vmin, vmax=vmax)  # axial

def process_patient_folder(input_folder, output_folder):
    data_list, ref_img, file_names = load_and_sort_frames(input_folder)
    if data_list is None:
        return

    os.makedirs(output_folder, exist_ok=True)

    # Frame 01 = mean of frames 0–19
    frame01 = np.mean(data_list[0:20], axis=0)
    save_single_frame(frame01, ref_img, os.path.join(output_folder, "frame01.nii"))

    # Frame 02 = mean of frames 20–22
    frame02 = np.mean(data_list[20:23], axis=0)
    save_single_frame(frame02, ref_img, os.path.join(output_folder, "frame02.nii"))

    # Frames 03–12 = original frames 24–33
    for i in range(23, 33):
        new_idx = i - 20  # 23 → 03, ..., 32 → 12
        frame = data_list[i]
        save_single_frame(frame, ref_img, os.path.join(output_folder, f"frame{new_idx:02}.nii"))

    # === Generate PNG previews with shared color scale for frame01 and frame02 ===
    frame01_path = os.path.join(output_folder, "frame01.nii")
    frame02_path = os.path.join(output_folder, "frame02.nii")

    img1 = nib.load(frame01_path).get_fdata()
    img2 = nib.load(frame02_path).get_fdata()

    vmin = min(img1.min(), img2.min())
    vmax = max(img1.max(), img2.max())

    for i, data in zip([1, 2], [img1, img2]):
        png_out = os.path.join(output_folder, f"frame{i:02}_png")
        generate_pngs_for_frame(os.path.join(output_folder, f"frame{i:02}.nii"), png_out, vmin=vmin, vmax=vmax)

    print(f"✅ Processed {input_folder} → {output_folder}")

def batch_process_all_patients(input_root, output_root):
    for patient in os.listdir(input_root):
        patient_input_path = os.path.join(input_root, patient)
        if not os.path.isdir(patient_input_path):
            continue
        patient_output_path = os.path.join(output_root, patient)
        process_patient_folder(patient_input_path, patient_output_path)

# === Configure Paths ===
input_root = r"C:\Users\ASUS\Documents\dPET_nifti\Normalized FTS"
output_root = r"C:\Users\ASUS\Documents\dPET_nifti\Normalized 12 Frame FTS"

batch_process_all_patients(input_root, output_root)
