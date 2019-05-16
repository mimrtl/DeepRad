# -*- coding: utf-8 -*-
import json
import os

ERROR_INFO_COLLECTION = {
    ## Prepare Data
    'input_folder': 'Step 1: data folder path does not exist!',
    'input_path': 'Step 1: data file does not exist!',
    'modality_used': 'Step 1: at least one modality should be chosen!',
    'label_folder': 'Step 1: label folder path does not exist!',
    'validation_ratio': 'Step 1: validation ratio should be a real number in [0, 1)!',
    'validation_folder': 'Step 1: validation folder path does not exist!',
    'validation_index': 'Step 1: path of file for validation index does not exist!',
    'resize_shape': 'Step 1: invalid resize shape!',

    ## Choose Model
    'input_size': 'Step 2: invalid input size!',
    'number_of_labels': 'Step 2: invalid number of labels',

    ## Training Configuration
    'learning_rate': 'Step 4: invalid learning rate',
    'drop_factor': 'Step 4: invalid drop factor',
    'patience': 'Step 4: invalid patience',
    'training_batch': 'Step 4: invalid training batch',
    'validation_batch': 'Step 4: invalid validation batch',
    'epoch': 'Step 4: invalid epoch number',
    'early_stop': 'Step 4: invalid early stop number',

    ## Output Configuration
    'output_folder': 'Step 5: output folder does not exist!',
    'output_file': 'Step 5: at least one type of output file should be chosen!'
}

NAMEOFMODALITIES = ["t1", "t1ce", "flair", "t2"]
VALIDATIONMODES = ["split", "folder", "index"]

def isValidPath(path):
    return os.path.exists(path)

def isAllFalseMultiChoice(list):
    return sum(list) == 0

def isValidNumber(number, min = -float('inf'), max = float('inf')):
    return number >= min and number <= max

def isValidIntNumberString(string, min = -float('inf'), max = float('inf')):
    try:
        number = int(string)
        return isValidNumber(number = number, min = min, max = max)
    except ValueError:
        return False

def isValidFloatNumberString(string, min = -float('inf'), max = float('inf')):
    try:
        number = float(string)
        return isValidNumber(number = number, min = min, max = max)
    except ValueError:
        return False

def isEmptyString(string):
    return len(string) == 0

def str2int(string):
    return int(string)

def str2float(string):
    return float(string)

class Config_Segmentation(object):

    # ## Prepare Data
    # self.config['data_folder'] = ""
    # self.config['modality_t1'] = True
    # self.config['modality_t1ce'] = True
    # self.config['modality_flair'] = True
    # self.config['modality_t2'] = True
    #
    # self.config['is_split'] = True
    # self.config['is_validation_folder'] = False
    # self.config['is_validation_index'] = False
    # self.config['validation_ratio'] = 0.2
    # self.config['validation_folder'] = ""
    # self.config['validation_index'] = ""
    #
    # self.config['is_resize'] = True
    # self.config['resize_row'] = 256
    # self.config['resize_col'] = 256
    # self.config['resize_channel'] = 256
    #
    # ## Choose Models
    # self.config['model'] = ""
    # self.config['input_size_row'] = 256
    # self.config['input_size_col'] = 256
    # self.config['input_size_channel'] = 3
    # self.config['num_class'] = 2
    #
    # ## Data Augmentation
    # self.config['isDataAug'] = False
    # self.config['DataAugConfig'] = {}
    #
    # ## Training Configuration
    # self.config['LossConfig'] = {}
    # self.config['OptimizerConfig'] = {}
    # self.config['learning_rate'] = 1e-4
    # self.config['drop_factor'] = ""
    # self.config['patience'] = ""
    # self.config['batch_size_training'] = 32
    # self.config['batch_size_validation'] = ""
    # self.config['epoch'] = 10
    # self.config['early_stop'] = ""
    #
    # ## Output Configuration
    # self.config['output_folder'] = ""
    # self.config['is_file_only'] = True
    # self.config['isWeight'] = False
    # self.config['isTensorboard'] = False
    # self.config['isLogs'] = False

    def __init__(self):
        self.config = {}

        self.is_valid_config = True
        self.check_result = []

    def saveConfig(self, path):
        f = open(path, "w")
        json.dump(self.config, f)
        f.close()

    def loadConfig(self, path):
        f = open(path, "r")
        load_dict = json.load(f)

        for curr_key in load_dict:
            self.config[curr_key] = load_dict[curr_key]
        f.close()

    def printConfig(self):
        print(self.config)
        #for curr_key in self.config:
        #    print(self.config[curr_key])


    ## The following functions are for segmentation only
    ## It is better to define a derived class or move these functions to segmentation file
    def getInputDataShape(self):
        num_modalities = sum(self.getListOfAllModalityStatus())
        return (num_modalities, self.config["input_size_row"], self.config["input_size_col"],
                self.config["input_size_channel"])

    def getInputImageShape(self):
        return (self.config["input_size_row"], self.config["input_size_col"], self.config["input_size_channel"])

    def getResizeShape(self):
        return (self.config["resize_row"], self.config["resize_col"], self.config["resize_channel"])

    def getListOfEffectiveModalities(self):
        effective_modalities = list()
        modalities_status = self.getListOfAllModalityStatus()
        for index in range(len(modalities_status)):
            if modalities_status[index]:
                effective_modalities.append(NAMEOFMODALITIES[index])
        return effective_modalities

    def getListOfAllModalityStatus(self):
        return [self.config['modality_t1'], self.config['modality_t1ce'],
               self.config['modality_flair'], self.config['modality_t2']]

    def getListOfAllOutputFileStatus(self):
        return [self.config['isWeight'], self.config['isTensorboard'], self.config['isLogs']]

    def getListOfAllValidationModes(self):
        return [self.config['is_split'], self.config['is_validation_folder'], self.config['is_validation_index']]

    def getValidationMode(self):
        return VALIDATIONMODES[self.getListOfAllValidationModes().index(True)]

    def initializeConfigCheckResult(self):
        self.is_valid_config = True
        self.check_result = []

    def configCheck(self):
        self.initializeConfigCheckResult()
        self.checkPrepareDataConfig()
        self.checkChooseModelConfig()
        self.checkTrainingConfig()
        self.checkOutputConfig()
        self.isValidConfig()

    def isValidConfig(self):
        if len(self.check_result) > 0:
            self.is_valid_config = False
        else:
            self.is_valid_config = True

    def configTransform(self):
        self.setDefaultValuesForLossAndOptimizer()
        self.transformPrepareDataConfig()
        self.transformChooseModelConfig()
        self.transformTrainingConfig()

    # def parameterCheckBeforeTraining(self):

    def setDefaultValuesForLossAndOptimizer(self):
        if self.isUseDefaultValueForLoss():
            self.config['LossConfig'] = {'loss': 'dice_coefficient_loss'}
        if self.isUseDefaultValueForOptimizer():
            self.config['OptimizerConfig'] = {'optimizer': 'Adam'}

    def isUseDefaultValueForLoss(self):
        return (len(self.config['LossConfig']) is 0)

    def isUseDefaultValueForOptimizer(self):
        return (len(self.config['OptimizerConfig']) is 0)

    def checkPrepareDataConfig(self):
        if not isValidPath(self.config['data_file_path']):
            self.check_result += [ERROR_INFO_COLLECTION['input_path']]
        #if isAllFalseMultiChoice(self.getListOfAllModalityStatus()):
        #    self.check_result += [ERROR_INFO_COLLECTION['modality_used']]
        #if not isValidPath(self.config["label_folder"]):
        #    self.check_result += [ERROR_INFO_COLLECTION['label_folder']]
        if self.config["is_split"]:
            if not isValidFloatNumberString(self.config["validation_ratio"], min = 0.0, max = 1.0):
                self.check_result += [ERROR_INFO_COLLECTION['validation_ratio']]
        if self.config["is_validation_folder"]:
            if not isValidPath(self.config["validation_folder"]):
                self.check_result += [ERROR_INFO_COLLECTION['validation_folder']]
        if self.config["validation_index"]:
            if not isValidPath(self.config["validation_index"]):
                self.check_result += [ERROR_INFO_COLLECTION['validation_index']]
        if (not isValidIntNumberString(self.config["resize_row"], min = 1.0))\
                or (not isValidIntNumberString(self.config["resize_col"], min = 1.0))\
                or (not isValidIntNumberString(self.config["resize_channel"], min = 1.0)):
            self.check_result += [ERROR_INFO_COLLECTION['resize_shape']]

    def transformPrepareDataConfig(self):
        if self.config["is_split"]:
            self.config["validation_ratio"] = str2float(self.config["validation_ratio"])
        else:
            self.config["validation_ratio"] = None
        self.config["resize_row"] = str2int(self.config["resize_row"])
        self.config["resize_col"] = str2int(self.config["resize_col"])
        self.config["resize_channel"] = str2int(self.config["resize_channel"])

    def transformChooseModelConfig(self):
        self.config["input_size_row"] = str2int(self.config["input_size_row"])
        self.config["input_size_col"] = str2int(self.config["input_size_col"])
        self.config["input_size_channel"] = str2int(self.config["input_size_channel"])
        self.config["num_class"] = str2int(self.config["num_class"])
    def transformTrainingConfig(self):
        self.config["learning_rate"] = str2float(self.config["learning_rate"])
        self.config["batch_size_training"] = str2int(self.config["batch_size_training"])
        self.config["epoch"] = str2int(self.config["epoch"])

        if isEmptyString(self.config["batch_size_validation"]):
            self.config["batch_size_validation"] = None
        else:
            self.config["batch_size_validation"] = str2int(self.config["batch_size_validation"])
        if isEmptyString(self.config["drop_factor"]):
            self.config['drop_factor'] = None
        else:
            self.config['drop_factor'] = str2float(self.config['drop_factor'])
        if isEmptyString(self.config['patience']):
            self.config['patience'] = None
        else:
            self.config['patience'] = str2int(self.config['patience'])
        if isEmptyString(self.config['early_stop']):
            self.config['early_stop'] = None
        else:
            self.config['early_stop'] = str2int(self.config['early_stop'])

    def checkChooseModelConfig(self):
        if (not isValidIntNumberString(self.config["input_size_row"], min = 1.0))\
                or (not isValidIntNumberString(self.config["input_size_col"], min = 1.0))\
                or (not isValidIntNumberString(self.config["input_size_channel"], min = 1.0)):
            self.check_result += [ERROR_INFO_COLLECTION['input_size']]
        if not isValidIntNumberString(self.config["num_class"], min = 2.0):
            self.check_result += [ERROR_INFO_COLLECTION['number_of_labels']]

    def checkTrainingConfig(self):
        if not isValidFloatNumberString(self.config["learning_rate"], min = 0.0):
            self.check_result += [ERROR_INFO_COLLECTION['learning_rate']]
        if not isEmptyString(self.config["drop_factor"]):
            if not isValidFloatNumberString(self.config["drop_factor"], min = 0.0, max = 1.0):
                self.check_result += [ERROR_INFO_COLLECTION['drop_factor']]
        if not isEmptyString(self.config["patience"]):
            if not isValidIntNumberString(self.config["patience"], min = 1.0):
                self.check_result += [ERROR_INFO_COLLECTION['patience']]
        if not isValidIntNumberString(self.config["batch_size_training"], min = 1.0):
            self.check_result += [ERROR_INFO_COLLECTION['training_batch']]
        if not isEmptyString(self.config["batch_size_validation"]):
            if not isValidIntNumberString(self.config["batch_size_validation"], min = 1.0):
                self.check_result += [ERROR_INFO_COLLECTION['validation_batch']]
        if not isValidIntNumberString(self.config["epoch"], min = 1.0):
            self.check_result += [ERROR_INFO_COLLECTION['epoch']]
        if not isEmptyString(self.config["early_stop"]):
            if not isValidIntNumberString(self.config["early_stop"], min = 1.0):
                self.check_result += [ERROR_INFO_COLLECTION['early_stop']]

    def checkOutputConfig(self):
        if not isValidPath(self.config["output_folder"]):
            self.check_result += [ERROR_INFO_COLLECTION['output_folder']]
        if (not self.config["is_file_only"]) and isAllFalseMultiChoice(self.getListOfAllOutputFileStatus()):
            self.check_result += [ERROR_INFO_COLLECTION['output_file']]

class Config_Classification(object):
    # ## Prepare Data
    # self.config['data_folder'] = ""
    # self.config['modality_t1'] = True
    # self.config['modality_t1ce'] = True
    # self.config['modality_flair'] = True
    # self.config['modality_t2'] = True
    #
    # self.config['label_folder'] = ""
    # self.config['is_split'] = True
    # self.config['is_validation_folder'] = False
    # self.config['is_validation_index'] = False
    # self.config['validation_ratio'] = 0.2
    # self.config['validation_folder'] = ""
    # self.config['validation_index'] = ""
    #
    # self.config['is_resize'] = True
    # self.config['resize_row'] = 256
    # self.config['resize_col'] = 256
    # self.config['resize_channel'] = 256
    #
    # ## Choose Models
    # self.config['model'] = ""
    # self.config['input_size_row'] = 256
    # self.config['input_size_col'] = 256
    # self.config['input_size_channel'] = 3
    # self.config['num_class'] = 2
    #
    # ## Data Augmentation
    # self.config['isDataAug'] = False
    # self.config['DataAugConfig'] = {}
    #
    # ## Training Configuration
    # self.config['LossConfig'] = {}
    # self.config['OptimizerConfig'] = {}
    # self.config['learning_rate'] = 1e-4
    # self.config['drop_factor'] = ""
    # self.config['patience'] = ""
    # self.config['batch_size_training'] = 32
    # self.config['batch_size_validation'] = ""
    # self.config['epoch'] = 10
    # self.config['early_stop'] = ""
    #
    # ## Output Configuration
    # self.config['output_folder'] = ""
    # self.config['is_file_only'] = True
    # self.config['isWeight'] = False
    # self.config['isTensorboard'] = False
    # self.config['isLogs'] = False

    def __init__(self):
        self.config = {}

        self.is_valid_config = True
        self.check_result = []

    def saveConfig(self, path):
        f = open(path, "w")
        json.dump(self.config, f)
        f.close()

    def loadConfig(self, path):
        f = open(path, "r")
        load_dict = json.load(f)

        for curr_key in load_dict:
            self.config[curr_key] = load_dict[curr_key]
        f.close()

    def printConfig(self):
        print(self.config)
        # for curr_key in self.config:
        #    print(self.config[curr_key])

    ## The following functions are for segmentation only
    ## It is better to define a derived class or move these functions to segmentation file
    def getInputDataShape(self):
        num_modalities = sum(self.getListOfAllModalityStatus())
        return (num_modalities, self.config["input_size_row"], self.config["input_size_col"],
                self.config["input_size_channel"])

    def getInputImageShape(self):
        return (self.config["input_size_row"], self.config["input_size_col"], self.config["input_size_channel"])

    def getResizeShape(self):
        return (self.config["resize_row"], self.config["resize_col"], self.config["resize_channel"])

    def getListOfEffectiveModalities(self):
        effective_modalities = list()
        modalities_status = self.getListOfAllModalityStatus()
        for index in range(len(modalities_status)):
            if modalities_status[index]:
                effective_modalities.append(NAMEOFMODALITIES[index])
        return effective_modalities

    def getListOfAllModalityStatus(self):
        return [self.config['modality_t1'], self.config['modality_t1ce'],
                self.config['modality_flair'], self.config['modality_t2']]

    def getListOfAllOutputFileStatus(self):
        return [self.config['isWeight'], self.config['isTensorboard'], self.config['isLogs']]

    def getListOfAllValidationModes(self):
        return [self.config['is_split'], self.config['is_validation_folder'], self.config['is_validation_index']]

    def getValidationMode(self):
        return VALIDATIONMODES[self.getListOfAllValidationModes().index(True)]

    def initializeConfigCheckResult(self):
        self.is_valid_config = True
        self.check_result = []

    def configCheck(self):
        self.initializeConfigCheckResult()
        self.checkPrepareDataConfig()
        self.checkChooseModelConfig()
        self.checkTrainingConfig()
        self.checkOutputConfig()
        self.isValidConfig()

    def isValidConfig(self):
        if len(self.check_result) > 0:
            self.is_valid_config = False
        else:
            self.is_valid_config = True

    def configTransform(self):
        self.setDefaultValuesForLossAndOptimizer()
        self.transformPrepareDataConfig()
        self.transformChooseModelConfig()
        self.transformTrainingConfig()

    # def parameterCheckBeforeTraining(self):

    def setDefaultValuesForLossAndOptimizer(self):
        if self.isUseDefaultValueForLoss():
            self.config['LossConfig'] = {'loss': 'cross_entropy'}
        if self.isUseDefaultValueForOptimizer():
            self.config['OptimizerConfig'] = {'optimizer': 'Adam'}

    def isUseDefaultValueForLoss(self):
        return (len(self.config['LossConfig']) is 0)

    def isUseDefaultValueForOptimizer(self):
        return (len(self.config['OptimizerConfig']) is 0)

    def checkPrepareDataConfig(self):
        if not isValidPath(self.config['data_file_path']):
            self.check_result += [ERROR_INFO_COLLECTION['data_path']]
        #if isAllFalseMultiChoice(self.getListOfAllModalityStatus()):
        #    self.check_result += [ERROR_INFO_COLLECTION['modality_used']]
        #if not isValidPath(self.config["label_folder"]):
        #    self.check_result += [ERROR_INFO_COLLECTION['label_folder']]
        if self.config["is_split"]:
            if not isValidFloatNumberString(self.config["validation_ratio"], min=0.0, max=1.0):
                self.check_result += [ERROR_INFO_COLLECTION['validation_ratio']]
        if self.config["is_validation_folder"]:
            if not isValidPath(self.config["validation_folder"]):
                self.check_result += [ERROR_INFO_COLLECTION['validation_folder']]
        if self.config["validation_index"]:
            if not isValidPath(self.config["validation_index"]):
                self.check_result += [ERROR_INFO_COLLECTION['validation_index']]
        if (not isValidIntNumberString(self.config["resize_row"], min=1.0)) \
                or (not isValidIntNumberString(self.config["resize_col"], min=1.0)) \
                or (not isValidIntNumberString(self.config["resize_channel"], min=1.0)):
            self.check_result += [ERROR_INFO_COLLECTION['resize_shape']]

    def transformPrepareDataConfig(self):
        if self.config["is_split"]:
            self.config["validation_ratio"] = str2float(self.config["validation_ratio"])
        else:
            self.config["validation_ratio"] = None
        self.config["resize_row"] = str2int(self.config["resize_row"])
        self.config["resize_col"] = str2int(self.config["resize_col"])
        self.config["resize_channel"] = str2int(self.config["resize_channel"])

    def transformChooseModelConfig(self):
        self.config["input_size_row"] = str2int(self.config["input_size_row"])
        self.config["input_size_col"] = str2int(self.config["input_size_col"])
        self.config["input_size_channel"] = str2int(self.config["input_size_channel"])
        self.config["num_class"] = str2int(self.config["num_class"])

    def transformTrainingConfig(self):
        self.config["learning_rate"] = str2float(self.config["learning_rate"])
        self.config["batch_size_training"] = str2int(self.config["batch_size_training"])
        self.config["epoch"] = str2int(self.config["epoch"])

        if isEmptyString(self.config["batch_size_validation"]):
            self.config["batch_size_validation"] = None
        else:
            self.config["batch_size_validation"] = str2int(self.config["batch_size_validation"])
        if isEmptyString(self.config["drop_factor"]):
            self.config['drop_factor'] = None
        else:
            self.config['drop_factor'] = str2float(self.config['drop_factor'])
        if isEmptyString(self.config['patience']):
            self.config['patience'] = None
        else:
            self.config['patience'] = str2int(self.config['patience'])
        if isEmptyString(self.config['early_stop']):
            self.config['early_stop'] = None
        else:
            self.config['early_stop'] = str2int(self.config['early_stop'])

    def checkChooseModelConfig(self):
        if (not isValidIntNumberString(self.config["input_size_row"], min=1.0)) \
                or (not isValidIntNumberString(self.config["input_size_col"], min=1.0)) \
                or (not isValidIntNumberString(self.config["input_size_channel"], min=1.0)):
            self.check_result += [ERROR_INFO_COLLECTION['input_size']]
        if not isValidIntNumberString(self.config["num_class"], min=2.0):
            self.check_result += [ERROR_INFO_COLLECTION['number_of_labels']]

    def checkTrainingConfig(self):
        if not isValidFloatNumberString(self.config["learning_rate"], min=0.0):
            self.check_result += [ERROR_INFO_COLLECTION['learning_rate']]
        if not isEmptyString(self.config["drop_factor"]):
            if not isValidFloatNumberString(self.config["drop_factor"], min=0.0, max=1.0):
                self.check_result += [ERROR_INFO_COLLECTION['drop_factor']]
        if not isEmptyString(self.config["patience"]):
            if not isValidIntNumberString(self.config["patience"], min=1.0):
                self.check_result += [ERROR_INFO_COLLECTION['patience']]
        if not isValidIntNumberString(self.config["batch_size_training"], min=1.0):
            self.check_result += [ERROR_INFO_COLLECTION['training_batch']]
        if not isEmptyString(self.config["batch_size_validation"]):
            if not isValidIntNumberString(self.config["batch_size_validation"], min=1.0):
                self.check_result += [ERROR_INFO_COLLECTION['validation_batch']]
        if not isValidIntNumberString(self.config["epoch"], min=1.0):
            self.check_result += [ERROR_INFO_COLLECTION['epoch']]
        if not isEmptyString(self.config["early_stop"]):
            if not isValidIntNumberString(self.config["early_stop"], min=1.0):
                self.check_result += [ERROR_INFO_COLLECTION['early_stop']]

    def checkOutputConfig(self):
        if not isValidPath(self.config["output_folder"]):
            self.check_result += [ERROR_INFO_COLLECTION['output_folder']]
        if (not self.config["is_file_only"]) and isAllFalseMultiChoice(self.getListOfAllOutputFileStatus()):
            self.check_result += [ERROR_INFO_COLLECTION['output_file']]

'''class Config_Classification(object):
    def __init__(self):
        self.config = {}

        # self.config['input_folder'] = None
        # self.config['output_folder'] = None
        # self.config['validation_ratio'] = 0.2
        # self.config['model'] = None
        # self.config['input_size_row'] = 256
        # self.config['input_size_col'] = 256
        # self.config['input_size_channel'] = 3
        # self.config['num_class'] = 2
        # self.config['loss'] = None
        # self.config['optimizer'] = None
        # self.config['batch_size'] = 32
        # self.config['learning_rate'] = 1e-4
        # self.config['epoch'] = 10

        # self.config['isWeight'] = False
        # self.config['isTensorboard'] = False
        # self.config['isLogs'] = False

        # self.config['isDataAug'] = False

    def config_check(self):
        check_result = {}
        if not os.path.exists(self.config['input_folder']):
            check_result['Valid_config'] = False
            check_result['Message'] = 'Data folder does not exist'
            return check_result
        if not os.path.exists(self.config['output_folder']):
            check_result['Valid_config'] = False
            check_result['Message'] = 'Output folder does not exist'
            return check_result
        try:
            self.config['validation_ratio'] = float(self.config['validation_ratio'])
            if (self.config['validation_ratio']>1.0) or (self.config['validation_ratio']<0.0):
                check_result['Valid_config'] = False
                check_result['Message'] = 'Invalid validation ratio (should be in the interval of [0.0, 1.0])'
                return check_result
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Validation ratio should be a float number (e.g. 0.2, 2e-1)'
            return check_result
        if self.config['model'] == None:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Invalid model'
            return check_result
        try:
            self.config['input_size_row'] = int(self.config['input_size_row'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Input row size should be a positive integer'
            return check_result
        try:
            self.config['input_size_col'] = int(self.config['input_size_col'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Input column size should be a positive integer'
            return check_result
        try:
            self.config['input_size_channel'] = int(self.config['input_size_channel'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Input channel size should be a positive integer'
            return check_result
        if (self.config['input_size_row']<1) or (self.config['input_size_col']<1) or \
                (self.config['input_size_channel']<1):
            check_result['Valid_config'] = False
            check_result['Message'] = 'Invalid input size (should be positive integers)'
            return check_result
        try:
            self.config['num_class'] = int(self.config['num_class'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Number of output classes should be a positive integer'
            return check_result
        if self.config['num_class'] < 1:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Invalid number of label classes (should be a positive integer)'
            return check_result
        if self.config['loss'] == None:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Invalid loss function'
            return check_result
        if self.config['optimizer'] == None:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Invalid optimizer'
            return check_result
        try:
            self.config['batch_size'] = int(self.config['batch_size'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Batch size should be a positive integer'
            return check_result
        if self.config['batch_size'] < 1:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Invalid batch size (should be a positive integer)'
            return check_result
        try:
            self.config['learning_rate'] = float(self.config['learning_rate'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Learning rate should be a positive real number'
            return check_result
        if self.config['learning_rate'] < 0.0:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Invalid learning rate (should be a positive real number)'
            return check_result
        try:
            self.config['epoch'] = int(self.config['epoch'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Epoch should be a positive integer'
            return check_result
        if self.config['epoch']<1:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Invalid epoch (should be a positive integer)'
            return check_result
        check_result['Valid_config'] = True
        check_result['Message'] = 'Valid configuration'
        return check_result

    def save_config(self, path):
        f = open(path, "w")
        json.dump(self.config, f)

    def load_config(self, path):
        f = open(path, "r")
        load_dict = json.load(f)

        for curr_key in self.config:
            self.config[curr_key] = load_dict[curr_key]'''


if __name__ == '__main__':
    x = Config_Classification()
    print(x.config_check())
    path = './test/test.json'
    x.save_config(path)
    #x.load_config(path)
    #print(x.config)
