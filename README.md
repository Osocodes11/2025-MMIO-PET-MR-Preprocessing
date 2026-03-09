# 2025-MMIO-PET-MR-Preprocessing
Overview
This repository contains scripts and workflow documentation used in a dynamic PET/MR preprocessing project conducted in a biomedical imaging research environment. The project focused on organizing neuroimaging datasets, performing quality control on preprocessed PET and MR brain images, and supporting established preprocessing pipelines used for downstream machine learning analysis. The code in this repository reflects my contributions to data organization, preprocessing workflow execution, and dataset preparation.

Project Objectives
1. Verify the quality of preprocessed PET and MR brain images
2. Organize large imaging datasets and metadata
3. Apply established PET/MR preprocessing workflows
4. Prepare datasets for cross-validation experiments

Key Components
1. Image Quality Control
PET and MR brain images were inspected using MRIcron to identify distorted or incomplete anatomical regions after preprocessing.

2. Dataset Organization
Python scripts were written to:
- Organize imaging datasets
- Detect missing files
- Identify inconsistent metadata
- Maintain structured directory layouts for analysis

3. Preprocessing Workflow
Established neuroimaging preprocessing workflows were applied using MATLAB and SPM, including:
- Co-registration of PET and MR images
- Spatial normalization
- Tissue segmentation
These workflows followed standard neuroimaging analysis practices.

4. Dataset Preparation
Imaging datasets were manually organized into five-fold cross-validation splits using Excel, and preprocessing outputs were verified before further analysis.

Tools & Technologies
- Python
- MATLAB
- SPM (Statistical Parametric Mapping)
- MRIcron
- Microsoft Excel
