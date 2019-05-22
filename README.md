# DeepRad

This project is for the development of software related to medical imaging using deep learning. DeepRad has two different modes (quick use and developer mode), which are for different goals and researchers with different level of programming.



DeepRad features large scale training with CNN, e.g. there are more than 10k volumes of scan. Loading these dataset directly into memory may cause out-of-memory (OOM) error. Hierarchical Data Format (HDF) is a collection of file formats (HDF4, HDF5) that is designed to store and organize large amounts of data. DeepRad provides **data management tool** to help users convert data to HDF5 file. During training process in DeepRad, only the batch of data will be loaded to memory from the hard driver where dataset is stored. Since all processes can be done in GUI, DeepRad is also friendly to people who are not familiar with coding.



This is the first version of the DeepRad. Currently we support the training process of 3D segmentation. We will add more features to make DeepRad more powerful.

## Step 0. Installation of Dependency
python 3.6 is recommended.

Choose a method from (a) or (b) to install the dependent packages.
### a. Install dependeny one by one
```
(for GPU user)
conda install -c anaconda tensorflow-gpu
conda install -c anaconda keras-gpu 
(for CPU user)
conda install -c anaconda tensorflow 
conda install -c anaconda keras
(common package)
conda install -c conda-forge pillow 
conda install -c conda-forge opencv 
conda install -c conda-forge nibabel
conda install -c conda-forge qimage2ndarray
conda install -c simpleitk simpleitk
conda install -c conda-forge nilearn
conda install -c conda-forge pytables
conda install -c anaconda nomkl
pip install git+https://www.github.com/farizrahman4u/keras-contrib.git
```
### b. Using the Installation.sh
Run the installation.sh. It may take for a while (~15 min).
```
bash installation.sh
```
<!---
<> **Directly use conda**
<>tensorflow
<>keras
<>tensorflow-gpu
<>pyqt
<>opencv
<>pillow
<>#**Should refer to Anaconda Cloud** https://anaconda.org/anaconda/repo
<>nibabel
<>qimage2ndarray
<>simpleitk
<>nilearn
<>**pip**
<>tables
### a. Create a new 'conda' virtual environment **(recommendation)**
```
conda env create --name DeepRad --file requirements.yml
```
-->

## Step 1. Dataset Preparation
### Folder constructure 
There are several possible ways to construct folders.
#### Folder Tree 1
    .
    ├── <data folder>
    │   ├── train                   # Data must be in a folder called "train" 
    │   │   ├── <Volume N>          # This is customized
    │   │   │   ├── <Modality M>    # This is customized
    │   │   │   ├── ...            
    │   │   │   ├── truth.nii.gz OR truth.nii or truth.csv   # Labels must be named as "truth"
    │   │   └── ...
    └── ...

example:

    data_example
    ├── type1
    │   ├── train
    │   │   ├── Brats17_2013_0_1
    │   │   │   ├── t1.nii.gz
    │   │   │   ├── t1ce.nii.gz
    │   │   │   ├── t2.nii.gz
    │   │   │   ├── flair.nii.gz
    │   │   │   ├── truth.nii.gz
    │   │   ├── Brats17_2013_15_1
    │   │   │   ├── t1.nii.gz
    │   │   │   ├── t1ce.nii.gz
    │   │   │   ├── t2.nii.gz
    │   │   │   ├── flair.nii.gz
    │   │   │   ├── truth.nii.gz
    └── ...

#### Folder Tree 2
    .
    ├── <data folder>
    │   ├── data                    # Data must be in a folder called "data"
    │   │   ├── <Volume N>          # This is customized
    │   │   │   ├── <Modality M>    # This is customized
    │   │   │   ├── ...
    │   ├── label                   # Data must be in a folder called "label"
    │   │   ├── <Volume N>          # The name shoule be the same as that in "data" folder
    │   │   │   ├── truth.nii.gz OR truth.nii or truth.csv   # Labels must be named as "truth"
    │   │   └── ...
    └── ...

example:

    data_example
    ├── type2
    │   ├── data
    │   │   ├── Brats17_2013_0_1
    │   │   │   ├── t1.nii.gz
    │   │   │   ├── t1ce.nii.gz
    │   │   │   ├── t2.nii.gz
    │   │   │   ├── flair.nii.gz
    │   │   ├── Brats17_2013_15_1
    │   │   │   ├── t1.nii.gz
    │   │   │   ├── t1ce.nii.gz
    │   │   │   ├── t2.nii.gz
    │   │   │   ├── flair.nii.gz
    │   ├── label
    │   │   ├── Brats17_2013_0_1
    │   │   │   └── truth.nii.gz
    │   │   ├── Brats17_2013_15_1
    │   │   │   └── truth.nii.gz
    └── ...

#### Folder Tree 3 (for synthesis)
    .
    ├── <data folder>
    │   ├── data                    # Data must be in a folder called "data"
    │   │   ├── <Volume N>          # This is customized
    │   ├── label                   # Data must be in a folder called "label"
    │   │   ├── <Volume N>          # The name shoule be the same as that in "data" folder
    └── ...

example:

    data_example
    ├── type3
    │   ├── data
    │   │   ├── Brats17_2013_0_1.nii.gz
    │   │   ├── Brats17_2013_15_1.nii.gz
    │   ├── label
    │   │   ├── Brats17_2013_0_1.nii.gz
    │   │   ├── Brats17_2013_15_1.nii.gz
    └── ...

#### Folder Tree 4 (for classification)
    .
    ├── <data folder>
    │   ├── data                    # Data must be in a folder called "data"
    │   │   ├── <Volume N>          # This is customized
    │   ├── label                   # Data must be in a folder called "label"
    │   │   ├── <Volume N>          # The name shoule be the same as that in "data" folder
    └── ...

example:

    data_example
    ├── type4
    │   ├── data
    │   │   ├── Brats17_2013_0_1.nii.gz
    │   │   ├── Brats17_2013_15_1.nii.gz
    │   ├── label
    │   │   ├── Brats17_2013_0_1.nii.csv
    │   │   ├── Brats17_2013_15_1.nii.csv
    └── ...

#### Folder Tree 5 (for classification)
    .
    ├── <data folder>
    │   ├── data                    # Data must be in a folder called "data"
    │   │   ├── <Volume N>          # This is customized
    │   ├── label                   # Data must be in a folder called "label"
    │   │   ├── truth.csv           # The name shoule be "truth.csv"
    └── ...

example:

    data_example
    ├── type5
    │   ├── data
    │   │   ├── Brats17_2013_0_1.nii.gz
    │   │   ├── Brats17_2013_15_1.nii.gz
    │   ├── label
    │   │   ├── truth.csv
    └── ...

### A tool of helping rename "truth"
Because **DeepRad** asks all labels named as "truth", a tool is provided to make it easier. Assume all folders are constucted as "type1" above.

    .
    ├── Data_folder                    # File name "Data_folder" is required.
    │   ├── train                      # File name "train" is required.
    │   │   ├── Brats17_2013_0_1
    │   │   │   ├── t1.nii.gz
    │   │   │   ├── t1ce.nii.gz
    │   │   │   ├── t2.nii.gz
    │   │   │   ├── flair.nii.gz
    │   │   │   ├── seg.nii.gz
    │   │   ├── Brats17_2013_15_1
    │   │   │   ├── t1.nii.gz
    │   │   │   ├── t1ce.nii.gz
    │   │   │   ├── t2.nii.gz
    │   │   │   ├── flair.nii.gz
    │   │   │   ├── seg.nii.gz
    └── ...

However, there are like 100 volumes to be trained but all segmentation results are named as "seg". Now, run the following code in the root.
```
python rename.py --seg_name seg
```
The parameter "--seg_name" is a common part of name in all files we want to change to "truth". After running this code, the folders will be like:

    .
    ├── Data_folder                    # File name "Data_folder" is required.
    │   ├── train                      # File name "train" is required.
    │   │   ├── Brats17_2013_0_1
    │   │   │   ├── t1.nii.gz
    │   │   │   ├── t1ce.nii.gz
    │   │   │   ├── t2.nii.gz
    │   │   │   ├── flair.nii.gz
    │   │   │   ├── truth.nii.gz
    │   │   ├── Brats17_2013_15_1
    │   │   │   ├── t1.nii.gz
    │   │   │   ├── t1ce.nii.gz
    │   │   │   ├── t2.nii.gz
    │   │   │   ├── flair.nii.gz
    │   │   │   ├── truth.nii.gz
    └── ...
### Converting data into hdf5 format.
**DeepRad** provides a tool to load the dataset and convert it as .hdf5 files, for better compatibility for huge dataset. 
To open **DeepRad**, follow **step 0** to install the dependent packages and run the following code in the **DeepRad** folder:
```
python main.py
```
Then we can see a main window. Now click "Quick use" and "Menu" in the top. Click "Data Management Tool" Assume we have the following folder constructure.

    .
    ├── Data_folder                    # File name "Data_folder" is required.
    │   ├── train                      # File name "train" is required.
    │   │   ├── Brats17_2013_0_1
    │   │   │   ├── t1.nii.gz
    │   │   │   ├── t1ce.nii.gz
    │   │   │   ├── t2.nii.gz
    │   │   │   ├── flair.nii.gz
    │   │   │   ├── truth.nii.gz
    │   │   ├── Brats17_2013_15_1
    │   │   │   ├── t1.nii.gz
    │   │   │   ├── t1ce.nii.gz
    │   │   │   ├── t2.nii.gz
    │   │   │   ├── flair.nii.gz
    │   │   │   ├── truth.nii.gz
    └── ...

In **Data Management Tool**, the data directory will be like: 
```
 ./DeepRad/Data_folder/train          # must be in "train" folder
```
And we can specify the output directory like:
```
 ./DeepRad/Data_folder
```
After specifying the directories, we can move to **Normalized to**. Two modes of normalization is provided: Standard and Interval.
1. Standard (Z-score)
   - data = (data / mean) / std
   - mean and std is calculated on all values, not only non-zeros values
2. Interval
   - data -= data_min
   - data /= (data_max - data_min)/(MAX-MIN)
   - data += MIN
   

**Normalization Type** determines how mean/std or data_max/data_min is calcuated. Assume we have 100 volumes, in each volume we have for modalities "t1", "t2", "t1ce", "flair". Each modality has the shape (240, 240, 155).
   - Global: parameters will be calculated among 100\*4\*(240, 240, 155) datasets
   - Per volume: paremeters will be caculated only on each (240, 240, 155) dataset
   - Per slice: paremeters will be calcuated only on each (240, 240) slice.

**Image Shape** is the output dataset shape. Becasue we are using a 3D model to do it, we recommend:
   - row: 64
   - col: 64
   - channel: 64

The right part is a preview tool to see our dataset. It can **only work** if we specify the volume path, like:
```
 ./DeepRad/Data_folder/train/Brats18_2013_1_1
```

After setting parameters, click **Convert**. Attention: it may take a few minutes, don't click other things or there will be several unknow bugs. We can see a "data.hdf5" in our path, like:
```
 ./DeepRad/Data_folder/train/data.hdf5
```
## Step 2. Main function (Take segmentation as an example)

Testing environment: 16G memory and GTX 1080 GPU and test 5 volume of Brats 2018 dataset.

Brats dataset: https://www.med.upenn.edu/sbia/brats2018/data.html

Click **Segmentation** in main window. And we can see 5 steps here. Now we are sharing the recommendation setting, and use the default setting if not mentioned.

### 1. Prepare Data
    - Data folder: ./DeepRad/Data_folder/train/data.hdf5
    - Validation data ratio: 0
    - Resize image to:
        - Row: 64
        - Col: 64
        - Channel: 64
### 2. Choose Models
    - isensee2017
    - Image channel size: 64 
    - Number of labels: 4
### 3. Data Augmentatiton
    - Enable: Not
### 4. Training Configuration
    - Batch size:
        - Training data: 8
    - Epoch: (We can fill as many as want)
### 5. Output configuration
    - Folder path: (The folder path we want to save the results)
    - Configuration file only: Not (if clicks, only a configuration file will be saved)
    - Training output:
        - weights: Yes. (This is the real model)
        - Tensorboard: Yes. (This is a tensorboard log)
        - logs: Tes. (Settings)

After that, click "Start" to train the model. And we can monitor the training progress.

![Visualization](/tools/DeepRad.png)

