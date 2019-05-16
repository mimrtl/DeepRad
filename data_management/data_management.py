import os
import sys
sys.path.append("..")
import numpy as np
import glob
import tables

from include.data import readImage, readCSV, readDictFromCSV
from include.normalization import normalizeToInterval, normalizeToStandardDistribution

class DataManagementClass(object):
    def __init__(self, data_path, output_path, image_shape, normalization_mode=None, normalization_range="global", min_value=0.0, max_value=1.0):
        self._data_type = np.float32
        self._normalization_mode = normalization_mode # "interval", "standard"
        self._interval_min_value = min_value
        self._interval_max_value = max_value
        self._image_shape = image_shape
        #self._mean = 0.0
        #self._std = 1.0
        self._normalization_range = normalization_range # "per_slice", "per_volume", "global"
        self._is_bias_field_correction = False # if True, an N4BiasFieldCorrection in
                                                # ANTs(Advanced Normalization Tools) will be used
        self._data_path = data_path
        self._output_path = output_path
        self._output_file_name = "data.h5"


        self._data_folder_name = "data"
        self._label_folder_name = "label"
        self._label_file_name = "truth"
        self._modalities_name = ["t1", "t1ce", "flair", "t2", "other"]


    def initializeParameters(self):
        self.data_and_label = None

        self.label_format = None  # 'csv' or 'nifty'
        self.label_separate_storage = None  #
        self.num_modalities = None
        self.used_modalities_name = None

        self.error_message = None


    '''def getLabelStorageType(self, data_path=None):
        if data_path:
            self._data_path = data_path
        if (not self._data_path) or (not os.path.exists(self._data_path)):
            raise ValueError("Path does not exists: %s"%(self._data_path))
        self.label_storage_type = 0
        self.label_format = 'csv'''''

    def fetchJointDataAndLabelType1(self, data_and_label, subject_dir, bias=0):
        scan_name = os.path.basename(subject_dir).split(".nii.gz")[0]
        subject_files = glob.glob(os.path.join(subject_dir, "*"))

        if self.num_modalities is None:
            self.num_modalities = len(subject_files) - 1 + bias
        else:
            if self.num_modalities != len(subject_files) - 1 + bias:
                self.error_message = "Folder %s contains different number of files" %subject_dir
                raise ValueError("Error")

        data_and_label["data"][scan_name] = dict()
        #data_and_label["truth"][scan_name] = dict()


        for file in subject_files:
            file_name = os.path.basename(file)
            if "truth" in file_name:
                if self.label_format is None:
                    if ".nii" in file_name:
                        self.label_format = "nii"
                    elif ".csv" in file_name:
                        self.label_format = "csv"
                    else:
                        self.error_message = "Unknown label format in %s" %subject_dir
                        raise ValueError("Error")
                else:
                    if not self.label_format in file_name:
                        self.error_message = "Multiple label formats have been detected: %s" %subject_dir
                        raise ValueError("Error")
                data_and_label["truth"][scan_name] = file
            elif "t1" in file_name and not ("t1ce" in file_name):
                data_and_label["data"][scan_name]["t1"] = file
            elif "t1ce" in file_name:
                data_and_label["data"][scan_name]["t1ce"] = file
            elif "flair" in file_name:
                data_and_label["data"][scan_name]["flair"] = file
            elif "t2" in file_name:
                data_and_label["data"][scan_name]["t2"] = file
            else:
                if "other" in data_and_label["data"][scan_name]:
                    self.error_message = "More than one non-standard modalities have been detected in folder %s" %subject_dir
                    raise ValueError("Error")
                else:
                    data_and_label["data"][scan_name]["other"] = file
        return data_and_label

    def fetchJointDataAndLabelType2(self, data_and_label, file):
        self.num_modalities = 1
        scan_name = os.path.basename(file).split(".nii.gz")[0]
        data_and_label["data"][scan_name] = dict()
        #data_and_label["truth"][scan_name] = dict()

        file_name = os.path.basename(file)
        if "truth" in file_name:
            if self.label_format is None:
                if ".nii" in file_name:
                    self.label_format = "nii"
                elif ".csv" in file_name:
                    self.label_format = "csv"
                else:
                    self.error_message = "Unknown label format in %s" %file
                    raise ValueError("Error")
            else:
                if not self.label_format in file_name:
                    self.error_message = "Multiple label formats have been detected: %s" %file
                    raise ValueError("Error")
            data_and_label["truth"][scan_name] = file
        elif "t1" in file_name and not ("t1ce" in file_name):
            data_and_label["data"][scan_name]["t1"] = file
        elif "t1ce" in file_name:
            data_and_label["data"][scan_name]["t1ce"] = file
        elif "flair" in file_name:
            data_and_label["data"][scan_name]["flair"] = file
        elif "t2" in file_name:
            data_and_label["data"][scan_name]["t2"] = file
        else:
            if "other" in data_and_label["data"][scan_name]:
                self.error_message = "More than one non-standard modalities have been detected in folder %s" %file
                raise ValueError("Error")
            else:
                data_and_label["data"][scan_name]["other"] = file
        return data_and_label


    def fetchJointDataAndLabel(self):
        ## scan1/t1.nii.gz
        ## scan1/truth.nii.gz or scan1/truth.csv
        ## scan2/t1.nii.gz
        ## scan2/truth.nii.gz or scan2/truth.csv

        data_and_label = dict()
        data_and_label["data"] = dict()
        data_and_label["truth"] = dict()
        for subject_dir in glob.glob(os.path.join(self._data_path, "*")):
            data_and_label = self.fetchJointDataAndLabelType1(data_and_label, subject_dir)

        self.data_and_label = data_and_label

    def fetchDataFiles(self):
        data_and_label = dict()
        data_and_label["data"] = dict()
        data_and_label["truth"] = dict()

        dir_indicator = None
        for subject_dir in glob.glob(os.path.join(self._data_path, "data", "*")):
            if dir_indicator is None:
                dir_indicator = os.path.isdir(subject_dir)

            if dir_indicator:
                data_and_label = self.fetchJointDataAndLabelType1(data_and_label, subject_dir, bias=1)
            else:
                data_and_label = self.fetchJointDataAndLabelType2(data_and_label, subject_dir)

        self.data_and_label = data_and_label

    def fetchLabelFiles(self):
        label_files = glob.glob(os.path.join(self._data_path, "label", "*"))
        if os.path.isdir(label_files[0]):
            for folder in label_files:
                scan_name = os.path.basename(folder)
                file_name = os.path.basename(glob.glob(os.path.join(folder, "*"))[0])
                if self.label_format is None:
                    if ".nii" in file_name:
                        self.label_format = "nii"
                    elif ".csv" in file_name:
                        self.label_format = "csv"
                    else:
                        self.error_message = "Unknown label format: %s" % file_name
                        raise ValueError("Unknown label format")
                else:
                    if not (self.label_format in file_name):
                        self.error_message = "Multiple label formats have been detected: %s"%file_name
                        raise ValueError("Multiple label formats have been detected")
                self.data_and_label["truth"][scan_name] = glob.glob(os.path.join(folder, "*"))[0]
        else:
            if (len(label_files) == 1) and os.path.isfile(label_files[0]):
                self.data_and_label["truth"] = label_files[0]
                self.label_format = "csv"
            else:
                for file in label_files:
                    file_name = os.path.basename(file)
                    if self.label_format is None:
                        if ".nii" in file_name:
                            self.label_format = "nii"
                        elif ".csv" in file_name:
                            self.label_format = "csv"
                        else:
                            self.error_message = "Unknown label format: %s"%file_name
                            raise ValueError("Error")
                    else:
                        if not (self.label_format in file_name):
                            self.error_message = "Multiple label formats have been detected: %s"%file_name
                            raise ValueError("Error")
                    scan_name = file_name.split("."+self.label_format)[0]
                    self.data_and_label["truth"][scan_name] = file
        if isinstance(self.data_and_label["truth"], dict):
            if not (self.data_and_label["data"].keys() == self.data_and_label["truth"].keys()):
                self.error_message = "The training data does not match the label data!"
                raise  ValueError("Error")



    def fetchSeparateDataAndLabel(self):
        self.fetchDataFiles()
        self.fetchLabelFiles()

    def tryToFetchJointDataAndLabel(self):
        try:
            self.fetchJointDataAndLabel()
            return True
        except:
            return False

    def tryToFetchSeparateDataAndLabel(self):
        try:
            self.fetchSeparateDataAndLabel()
            return True
        except:
            return False

    def detectTypeOfDataStorage(self):
        folder_list = glob.glob(os.path.join(self._data_path, "*"))
        if len(folder_list) == 2:
            folder_name = [os.path.basename(folder_list[0]), os.path.basename(folder_list[1])]
            if (self._data_folder_name in folder_name) and (self._label_folder_name in folder_name):
                self.label_separate_storage = True
        else:
            self.label_separate_storage = False

    def fetchFiles(self):
        if self.label_separate_storage:
            status = self.tryToFetchSeparateDataAndLabel()
        else:
            status = self.tryToFetchJointDataAndLabel()
        if not status:
            self.error_message = \
                "Failed to fetch data files!\nPlease follow right way to store data in the tutorial "
            raise ValueError("Failed to fetch data files!")


    '''def fetchDataFiles(self):
        status =  self.tryToFetchJointDataAndLabel(fetch_success_status=False)
        status =  self.tryToFetchSeperateDataAndLabel(fetch_success_status=status)
        if not status:
            self.error_message = \
            "Failed to fetch data files!\nPlease follow right way to store data in the tutorial "
            raise ValueError("Error!")'''

    def createHDF5File(self):
        out_file_path = os.path.join(self._output_path, self._output_file_name)
        try:
            hdf5_file = tables.open_file(out_file_path, mode='w')
            filters = tables.Filters(complevel=5, complib='blosc')
            data_shape = tuple([0, self.num_modalities] + list(self._image_shape))
            data_storage = hdf5_file.create_earray(hdf5_file.root, 'data', tables.Float32Atom(), shape=data_shape,
                                                   filters=filters, expectedrows=self.num_modalities)
            if self.label_format == "nii":
                truth_shape = tuple([0, 1] + list(self._image_shape))
                truth_storage = hdf5_file.create_earray(hdf5_file.root, 'truth', tables.UInt8Atom(), shape=truth_shape,
                                                    filters=filters, expectedrows=self.num_modalities)
            elif self.label_format == 'csv':
                truth_shape = tuple([0, self._image_shape[-1]])
                truth_storage = hdf5_file.create_earray(hdf5_file.root, 'truth', tables.UInt32Atom(), shape=truth_shape,
                                                        filters = filters, expectedrows=self.num_modalities)
            else:
                raise ValueError("Fail to recognize label format: %s"%self.label_format)

            affine_storage = hdf5_file.create_earray(hdf5_file.root, 'affine', tables.Float32Atom(), shape=(0, 4, 4),
                                                     filters=filters, expectedrows=self.num_modalities)
            return hdf5_file, data_storage, truth_storage, affine_storage
        except Exception as e:
            # If something goes wrong, delete the incomplete data file
            os.remove(out_file_path)
            raise e

    def addDataToStorage(self, hdf5_file, data_storage, truth_storage, affine_storage):
        if not isinstance(self.data_and_label["truth"], dict):
            labels = readDictFromCSV(self.data_and_label["truth"])

        subject_ids = list()
        for scan_name in self.data_and_label["data"]:
            ## subject id
            subject_ids.append(scan_name)

            ## Modalities name
            if self.used_modalities_name is None:
                self.used_modalities_name = list(self.data_and_label["data"][scan_name].keys())

            ## data
            image_list = list()
            for modality in self._modalities_name:
                if modality in self.data_and_label["data"][scan_name]:
                    interpolation = "linear"
                    image_file = self.data_and_label["data"][scan_name][modality]
                    image = readImage(image_file, image_shape=self._image_shape, interpolation=interpolation)
                    image_list.append(image.get_data())
            data_storage.append(np.asarray(image_list)[np.newaxis])

            ## affine matrix
            affine_storage.append(np.asarray(image.affine)[np.newaxis])

            ## label
            if isinstance(self.data_and_label["truth"], dict):
                if self.label_format == "nii":
                    interpolation = "nearest"
                    image_file = self.data_and_label["truth"][scan_name]
                    image = readImage(image_file, image_shape=self._image_shape, interpolation=interpolation)
                    truth_storage.append(np.asarray(image.get_data())[np.newaxis][np.newaxis])
                if self.label_format == 'csv':
                    labels = readCSV(self.data_and_label["truth"][scan_name])
                    if labels.size == 1:
                        labels = np.repeat(labels, self._image_shape[-1])

                    truth_storage.append(labels[np.newaxis])
            else:
                if labels[scan_name].size == 1:
                    label = np.repeat(labels[scan_name], self._image_shape[-1])
                else:
                    label = labels[scan_name]
                truth_storage.append(label[np.newaxis])

        hdf5_file.create_array(hdf5_file.root, 'subject_ids', obj=subject_ids)
        hdf5_file.create_array(hdf5_file.root, 'used_modalities', obj = self.used_modalities_name)


    def normalizeData(self, data_storage):
        if self._normalization_mode == "interval":
            normalizeToInterval(data_storage, self._interval_min_value, self._interval_max_value)
        elif self._normalization_mode == "standard":
            normalizeToStandardDistribution(data_storage)
        else:
            print("Fail to recognize normalization mode: %s"%self._normalization_mode)
            Warning("Data has not been normalized")


    def writeDataToFile(self):
        hdf5_file, data_storage, truth_storage, affine_storage = self.createHDF5File()
        self.addDataToStorage(hdf5_file, data_storage, truth_storage, affine_storage)
        self.normalizeData(data_storage)
        hdf5_file.close()

    def startConvert(self):
        self.initializeParameters()
        self.detectTypeOfDataStorage()
        self.fetchFiles()
        self.writeDataToFile()


if __name__ == '__main__':
    data = DataManagementClass('/Users/zhangjinnian/Documents/UWmadison/1Project/DeepRad/data_example/type1/train',
                          '../data_example',
                          (128, 128, 128),
                          normalization_mode="interval")
    data.startConvert()
    print("Done!")