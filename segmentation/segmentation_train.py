# -*- coding: utf-8 -*-
# Reference: https://github.com/ellisdg/3DUnetCNN
import os
import sys
sys.path.append("..")

from include.data import openDataFile, fetchTrainingDataFiles, preprocessAndSaveDataToFile
from include.training import createModel, trainModel
from include.generator import getTrainAndValidationGenerator

TRAINING_STATUS_COLLECTION = {
    "ready": "Status: Ready",
    "open_data_file": "Status: Open data file...",
    "create_model": "Status: Create model...",
    "training": "Status: Training...",
    "end_of_train": "Status: End of Train"
}

train_paras = dict()
train_paras["config_file"] = "segmentation_config.json"
#train_paras["data_file"] = "data.h5"
train_paras["validation_file"] = "validation.h5"
train_paras["model_file"] = "model.h5"
train_paras["training_file"] = "training_ids.pkl"
train_paras["validation_file"] = "validation_ids.pkl"
train_paras["log_file"] = "training.log"
train_paras["tensorboard_dir"] = "logs"

def isSaveConfigFileOnly(config):
    if config['is_file_only']:
        return True
    else:
        return False

def saveConfigFile(config_class, file):
    config_class.saveConfig(file)

def updateTrainParas(config):
    folder = config['output_folder']
    for key in train_paras:
        train_paras[key] = os.path.join(folder, os.path.basename(train_paras[key]))


def startTraining(config_class):
    config = config_class.config

    print(TRAINING_STATUS_COLLECTION["open_data_file"])
    data_file_opened = openDataFile(config["data_file_path"])
    num_modalities = len(data_file_opened.root.used_modalities)


    print(TRAINING_STATUS_COLLECTION["create_model"])
    model = createModel(config_class=config_class,
                        input_shape = tuple([num_modalities]+list(config_class.getInputImageShape())),
                        model_type=config['model'])


    print(TRAINING_STATUS_COLLECTION["training"])
    train_gen, validation_gen, n_train_steps, n_validation_steps = getTrainAndValidationGenerator(
        data_file_opened,
        config_class.getInputImageShape(),
        config["batch_size_training"],
        config["num_class"],
        train_paras["training_file"],
        train_paras["validation_file"],
        validation_mode=config_class.getValidationMode(),
        validation_split=config["validation_ratio"],
        validation_path=config["validation_folder"],
        validation_index=config["validation_index"],
        validation_batch_size=config["batch_size_validation"],
        augment=config["isDataAug"],
        dataAugConfig=config["data_aug_config"]
    )
    trainModel(
        model=model,
        model_file=train_paras["model_file"],
        training_generator=train_gen,
        validation_generator=validation_gen,
        steps_per_epoch=n_train_steps,
        validation_steps=n_validation_steps,
        initial_learning_rate=config["learning_rate"],
        learning_rate_drop=config["drop_factor"],
        learning_rate_patience=config["patience"],
        early_stopping_patience=config["early_stop"],
        n_epochs=config["epoch"],
        isTrainingLogs=config["isLogs"],
        TrainingLogs=train_paras["log_file"],
        isTensorboard=config["isTensorboard"],
        tensorboard_log_dir=train_paras["tensorboard_dir"]
    )
    data_file_opened.close()
    print(TRAINING_STATUS_COLLECTION["end_of_train"])

def train(config_class):
    config = config_class.config
    #effective_modalities = config_class.getListOfEffectiveModalities()
    updateTrainParas(config)

    if isSaveConfigFileOnly(config):
        saveConfigFile(config_class=config_class, file=train_paras["config_file"])
    else:
        saveConfigFile(config_class=config_class, file=train_paras["config_file"])
        #training_data_files, subject_ids = fetchTrainingDataFiles(effective_modalities, config['data_folder'],
        #                                                          return_subject_ids=True)
        #preprocessAndSaveDataToFile(training_data_files, train_paras["data_file"],
        #                            image_shape=config_class.getResizeShape(),
        #                            subject_ids=subject_ids)

        startTraining(config_class=config_class)

if __name__ == '__main__':
    from configuration import Config_Segmentation
    path = '../result/segmentation_config.json'
    config_class = Config_Segmentation()
    config_class.loadConfig(path)
    train(config_class)
