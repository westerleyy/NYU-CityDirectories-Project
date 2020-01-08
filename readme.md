### NYU x NYPL Space Time Directories
This repository serves to consolidate all of the scripts required to operationalize the digitization process of New York City's 19th century directories.  

#### Current Status @westerleyy
As of January 7, 2020, a workflow for the preprocessing of the images has been developed. At this moment, it sits within the `WorkflowTrial01.ipynb` file. The present workflow will crop out images to just the columns and then perform an affine transformation which effectively deskews and rotates the image.  
The `crop_for_columns.py` file operationalizes for bash command line operations.

#### Current List of Hyperparameters

1. Pre-crop processing?

2. Post-crop contrast heightening

3. Tesseract -oem and -psm values

4. hocr-detect columns?

5. CRF extracted features and amount of training data 
