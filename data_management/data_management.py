import os
import sys
sys.path.append("..")
import numpy as np

class DataAugmentation(object):
    def __init__(self):
        self._data_type = np.float32
        self._normalization_mode = "interval" # "interval", "standard"
        self._interval = [0.0, 1.0]
        self._mean = 0.0
        self._std = 1.0
        self._normalization_range = "per slice" # "per slice", "per volume", "global"
        self._is_bias_field_correction = False # if True, an N4BiasFieldCorrection in
                                                # ANTs(Advanced Normalization Tools) will be used
        self._data_path = None
        self._output_path = None

        self.label_format = None # 'csv' or 'nifty'
        self.label_storage_type = None # 0, 1, 2, 3

        self.error_message = None

    def getLabelStorageType(self, data_path=None):
        if data_path:
            self._data_path = data_path
        if (not self._data_path) or (not os.path.exists(self._data_path)):
            raise ValueError("Path does not exists: %s"%(self._data_path))
        self.label_storage_type = 0
        self.label_format = 'csv'

    def fetchDataFiles(self):
        if not self.tryToFetchJointDataAndLabel():
                if not self.tryToFetchSeperateDataAndLabel():
                    self.error_message = \
                        "Failed to fetch data files!\nPlease follow right way to store data in the tutorial "
                    raise ValueError("Error!")


    def startConvert(self):
        self.fetchDataFiles()
        self.createHDF5File()
        self.writeDataToFile()


