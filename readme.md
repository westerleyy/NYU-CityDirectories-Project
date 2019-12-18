### NYU x NYPL Space Time Directories
This repository serves to consolidate all of the scripts required to operationalize the digitization process of New York City's 19th century directories.  

#### Current Status @westerleyy
As of November 16 2019, a workflow for the preprocessing of the images and running them through Tesseract has been developed. At this moment, it sits within the `WorkflowTrial01.ipynb` file.  
The next step will be to look at integration with CRF and column detection scripts and then running a full test to validate efficacy.

#### Current List of Hyperparameters

1. Pre-crop processing?

2. Post-crop contrast heightening

3. Tesseract -oem and -psm values

4. hocr-detect columns?

5. CRF extracted features and amount of training data 