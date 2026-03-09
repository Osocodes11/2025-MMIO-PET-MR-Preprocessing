import nibabel as nib 
import numpy as np

img = nib.load(r"C:\Users\ASUS\Documents\dPET_nifti\Final Training Set (nifti)\006_S_0498_06-09\frame27.nii")
data = img.get_fdata()
print(np.mean(data))