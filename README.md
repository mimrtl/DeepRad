# DeepRad

This project is for the development of software related to medical imaging using deep learning. DeepRad has two different modes (quick use and developer mode), which are for different goals and researchers with different level of programming.

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

Testing computer: 16G memory and GTX 1080 GPU

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
        - Validation data: (Don't fill anything here)
    - Epoch: (We can fill as many as want)
### 5. Output configuration
    - Folder paht: (The folder path we want to save the results)
    - Configuration file only: Not (if clicks, only a configuration file will be saved)
    - Training output:
        - weights: Yes. (This is the real model)
        - Tensorboard: Yes. (This is a tensorboard log)
        - logs: Tes. (Settings)
        
After that, click "Start" to train the model. And we can monitor the training progress.




## Step X. Documentation

In **Quick Use** mode, there are 4 main functions: classification, segmentation, regression, and synthesis. In this mode, it only supports specific types of data, deep learning models, training and evaluation methods. A data management tool is also embedded in DeepRad to preprocess raw data so that they can be directly used in this mode. 

### 1.0 Data Management Tool

Currently, it only supports certain types of data storage.

1. Classification:
   - Data: single input channel or multiple input channels in 

2. Segmentation:

### 1.1 Classification

Framework: data(nii, hdf5, npy)/label (csv, hdf5, npy; binary or index), model (keras model zoo), training methods (only listed in keras).

### 1.2 Segmentation

Framework: data(nii, hdf5, npy; preprocessed)/truth(nii, hdf5, npy; index), model(Unet2D, Unet3D), training methods(only listed in keras)

#### Configuration Class

```python
self.config={
  # Prepare Data
  'data_folder': "",
  'modality_t1': True,
  'modality_t1ce': True,
  'modality_flair': True,
  'modality_t2': True,
  'label_folder': "", # will be removed
  'is_split': True,
  'is_validation_folder': False,
  'is_validation_index': False,
  'validation_ratio': 0.2,
  'validation_folder': "",
  'validation_index': "",
  'is_resize': True,
  'resize_row': 256,
  'resize_col': 256,
  'resize_channel': 256,
  
  # Choose Models
  'model': "",
  'input_size_row': 256,
  'input_size_col': 256,
  'input_size_channel': 3,
  'num_class': 2,
  
  # Data Augmentation
  'isDataAug': False,
  'data_aug_config': {},
  
  # Training Configuration
  'LossConfig': {},
  'OptimizerConfig': {},
  'learning_rate': 1e-4,
  'drop_factor': "",
  'patience': "",
  'batch_size_training': 32,
  'batch_size_validation': "",
  'epoch': 10,
  'early_stop': "",
  
  # Output Configuration
  'output_folder': "",
  'is_file_only': True,
  'isWeight': False,
  'isTensorboard': False,
  'isLogs': False
}
```



### 1.3



## 2. Developer Mode

In **Developer Mode**, it provides a framework for training and evaluation. Users can replace some of the modules by using their own codes. It will be more flexible and require users have a coding background.

## Q&A

![image-20190512121043729](image/README/image-20190512121043729-7681043.png)

Solutions:

1. Add the following codes in `main.py`

```python
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
```

2. Install the following packages

```
conda install nomkl
```

