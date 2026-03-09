% Define paths
input_root = 'C:\Users\ASUS\Documents\dPET_nifti\Final Training Set (nifti)';
output_root = 'C:\Users\ASUS\Documents\dPET_nifti\Normalized FTS';

% Create output root if it doesn't exist
if ~exist(output_root, 'dir')
    mkdir(output_root);
end

% Get list of all subfolders (patients)
patient_folders = dir(input_root);
patient_folders = patient_folders([patient_folders.isdir]);  % Only folders
patient_folders = patient_folders(~ismember({patient_folders.name}, {'.', '..'}));  % Remove . and ..

% Loop through each patient folder
for i = 1:length(patient_folders)
    patient_name = patient_folders(i).name;
    input_subfolder = fullfile(input_root, patient_name);
    output_subfolder = fullfile(output_root, patient_name);
    
    % Create output subfolder
    if ~exist(output_subfolder, 'dir')
        mkdir(output_subfolder);
    end
    
    % Get only frameXX.nii files (not MRI.nii)
    nii_files = dir(fullfile(input_subfolder, 'frame*.nii'));
    
    for j = 1:length(nii_files)
        
        nii_path = fullfile(input_subfolder, nii_files(j).name);
        disp(nii_path)
        % Load header
        hdr = spm_vol(nii_path);
        
        % Read image
        img = niftiread(nii_path);
        
        % Get normalization constant
        norm_const = hdr.pinfo(1);
        
        % Skip if normalization constant is zero
        if norm_const == 0
            warning(['Normalization constant is zero for ' nii_files(j).name]);
            continue;
        end
        
        % Normalize the image
        % norm_img = double(img) / norm_const;
        % disp(norm_const)
        % disp(mean(mean(mean(img))))
        % disp(mean(mean(mean(norm_img))))
        % disp("-----------------")
        % 
        % Set datatype and output settings
        % hdr.pinfo(1) = 1;
        % hdr.dt = [64, 0];
        hdr.fname = fullfile(output_subfolder, nii_files(j).name);
        
        % Write the new normalized image
        spm_write_vol(hdr, norm_img);
        spm_write_vol(hdr, img);
    end
end

disp('All frameXX PET files have been normalized and saved.');
