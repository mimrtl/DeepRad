# -*- coding: utf-8 -*-
from random import shuffle
import numpy as np
import os
import copy

from include.data import pickle_dump
from include.augment import augmentData

def getTrainAndValidationGenerator(data_file, target_size, batch_size, n_labels, training_keys_file, validation_keys_file,
                                   validation_mode='split', validation_split=0.2, validation_path=None, validation_index=None,
                                   validation_batch_size=None,
                                   augment=False, dataAugConfig=None
                                   ):
    """
    Creates the training and validation generators that can be used when training the model.
    :param skip_blank: If True, any blank (all-zero) label images/patches will be skipped by the data generator.
    :param validation_batch_size: Batch size for the validation data.
    :param training_patch_start_offset: Tuple of length 3 containing integer values. Training data will randomly be
    offset by a number of pixels between (0, 0, 0) and the given tuple. (default is None)
    :param validation_patch_overlap: Number of pixels/voxels that will be overlapped in the validation data. (requires
    patch_shape to not be None)
    :param patch_shape: Shape of the data to return with the generator. If None, the whole image will be returned.
    (default is None)
    :param augment_flip: if True and augment is True, then the data will be randomly flipped along the x, y and z axis
    :param augment_distortion_factor: if augment is True, this determines the standard deviation from the original
    that the data will be distorted (in a stretching or shrinking fashion). Set to None, False, or 0 to prevent the
    augmentation from distorting the data in this way.
    :param augment: If True, training data will be distorted on the fly so as to avoid over-fitting.
    :param labels: List or tuple containing the ordered label values in the image files. The length of the list or tuple
    should be equal to the n_labels value.
    Example: (10, 25, 50)
    The data generator would then return binary truth arrays representing the labels 10, 25, and 30 in that order.
    :param data_file: hdf5 file to load the data from.
    :param batch_size: Size of the batches that the training generator will provide.
    :param n_labels: Number of binary labels.
    :param training_keys_file: Pickle file where the index locations of the training data will be stored.
    :param validation_keys_file: Pickle file where the index locations of the validation data will be stored.
    :param data_split: How the training and validation data will be split. 0 means all the data will be used for
    validation and none of it will be used for training. 1 means that all the data will be used for training and none
    will be used for validation. Default is 0.8 or 80%.
    :param overwrite: If set to True, previous files will be overwritten. The default mode is false, so that the
    training and validation splits won't be overwritten when rerunning model training.
    :param permute: will randomly permute the data (data must be 3D cube)
    :return: Training data generator, validation data generator, number of training steps, number of validation steps
    """
    if validation_mode == 'split':
        return getGeneratorsBySplit(
            data_file, target_size, batch_size, n_labels, training_keys_file, validation_keys_file, validation_split,
            validation_batch_size, augment, dataAugConfig
        )
    elif validation_mode == 'folder':
        return getGeneratorsFromValidationFolder(
            data_file, batch_size, n_labels, validation_path,
            validation_batch_size, augment, dataAugConfig
        )
    elif validation_mode == 'index':
        return getGeneratorsFromIndexFile(
            data_file, batch_size, n_labels, training_keys_file, validation_keys_file,
            validation_batch_size, augment, dataAugConfig
        )
    else:
        raise ValueError(" 'validation_mode' should be 'split', 'folder' or 'index'. '{}' is not recognized".format(
            validation_mode))

def splitList(input_list, split=0.2, shuffle_list=True):
    data_split = 1.0 - split
    if shuffle_list:
        shuffle(input_list)
    n_training = int(len(input_list) * data_split)
    training = input_list[:n_training]
    testing = input_list[n_training:]
    return training, testing

def getValidationSplit(data_file, target_size, training_file, validation_file, validation_split=0.2):
    """
    Splits the data into the training and validation indices list.
    :param data_file: pytables hdf5 data file
    :param training_file:
    :param validation_file:
    :param data_split:
    :param overwrite:
    :return:
    """
    print("Creating validation split...")
    num_files = data_file.root.data.shape[0]
    sample_per_file = data_file.root.data.shape[4] - target_size[2] + 1
    print("The total number of samples in this dataset is %d (number of files) * %d (number of samples per file) = %d"%(num_files, sample_per_file, num_files*sample_per_file))
    sample_list = list(range(num_files*sample_per_file))
    training_list, validation_list = splitList(sample_list, split=validation_split)
    #print(training_list)
    #print(validation_list)
    pickle_dump(training_list, training_file)
    pickle_dump(validation_list, validation_file)
    return training_list, validation_list


def getGeneratorAndSteps(data_file, target_size, index_list, batch_size, n_labels, augment=False, dataAugConfig=None):
    if len(index_list) == 0:
        generator = None
        num_steps = None
    else:
        generator = dataGenerator(data_file, target_size, index_list,
                                   batch_size=batch_size,
                                   n_labels=n_labels,
                                   augment=augment,
                                   dataAugConfig=dataAugConfig)
        num_steps = getNumberOfSteps(len(index_list), batch_size)
    return generator, num_steps


'''def getTrainingGenerator(data_file, training_list, batch_size, n_labels, augment):
    if len(training_list) is 0:
        raise ValueError("No training data is detected!")
    else:
        training_generator = data_generator(data_file, training_list,
                                            batch_size=batch_size,
                                            n_labels=n_labels,
                                            augment=augment,
                                            augment_flip=augment_flip,
                                            augment_distortion_factor=augment_distortion_factor,
                                            patch_shape=patch_shape,
                                            patch_overlap=0,
                                            patch_start_offset=training_patch_start_offset,
                                            skip_blank=skip_blank,
                                            permute=permute)

        # Set the number of training and testing samples per epoch correctly
        num_training_steps = get_number_of_steps(get_number_of_patches(data_file, training_list, patch_shape,
                                                                       skip_blank=skip_blank,
                                                                       patch_start_offset=training_patch_start_offset,
                                                                       patch_overlap=0), batch_size)
        print("Number of training steps: ", num_training_steps)
        return training_generator, num_training_steps


def getValidationGenerator():
    if (len(validation_list) is 0) or (validation_batch_size is None):
        validation_generator = None
        num_validation_steps = None
        print("Validation is not activated.")
    else:
        validation_generator = data_generator(data_file, validation_list,
                                              batch_size=validation_batch_size,
                                              n_labels=n_labels,
                                              labels=labels,
                                              patch_shape=patch_shape,
                                              patch_overlap=validation_patch_overlap,
                                              skip_blank=skip_blank)
        num_validation_steps = get_number_of_steps(get_number_of_patches(data_file, validation_list, patch_shape,
                                                                         skip_blank=skip_blank,
                                                                         patch_overlap=validation_patch_overlap),
                                                   validation_batch_size)
        print("Number of validation steps: ", num_validation_steps)
    return validation_generator, num_validation_steps'''

def getGeneratorsBySplit(data_file,tartget_size, batch_size, n_labels, training_keys_file, validation_keys_file, validation_split,
            validation_batch_size, augment=False, dataAugConfig=None):


    training_list, validation_list = getValidationSplit(data_file, tartget_size,
                                                          validation_split=validation_split,
                                                          training_file=training_keys_file,
                                                          validation_file=validation_keys_file)

    training_generator, num_training_steps = getGeneratorAndSteps(data_file, tartget_size, training_list,
                                                                  batch_size=batch_size,
                                                                  n_labels=n_labels,
                                                                  augment=augment,
                                                                  dataAugConfig=dataAugConfig)

    validation_generator, num_validation_steps = getGeneratorAndSteps(data_file, tartget_size, validation_list,
                                                                        batch_size=validation_batch_size,
                                                                        n_labels=n_labels,
                                                                        augment=False,
                                                                        dataAugConfig=None)

    return training_generator, validation_generator, num_training_steps, num_validation_steps

def getGeneratorsFromValidationFolder(data_file, batch_size, n_labels, training_keys_file, validation_keys_file, data_split,
            validation_batch_size, labels, augment, dataAugConfig):
    print('In construction')

def getGeneratorsFromIndexFile(data_file, batch_size, n_labels, training_keys_file, validation_keys_file, data_split,
            validation_batch_size, labels, augment, dataAugConfig):
    print('In construction')


def dataGenerator(data_file, target_size, index_list, batch_size,
                  n_labels=2, shuffle_index_list=True, augment=False, dataAugConfig=None):
    while True:
        x_list = list()
        y_list = list()

        index_list_copy = copy.copy(index_list)

        if shuffle_index_list:
            shuffle(index_list_copy)
            #print("index list: "+str(index_list_copy))
            #input()
        while len(index_list_copy) > 0:
            index = index_list_copy.pop()
            addData(x_list, y_list, target_size, data_file, index, augment, dataAugConfig)
            if len(x_list) == batch_size or (len(index_list_copy) == 0 and len(x_list) > 0):
                yield np.asarray(x_list), getOneHotLabels(np.asarray(y_list), n_labels, squeezed=True)
                x_list = list()
                y_list = list()

def getFileAndSampleIndex(index, total_sample):
    return index // total_sample, index % total_sample

def getImageByIndex(data_file, target_size, index):
    total_sample_per_file = data_file.root.data.shape[4] - target_size[2] + 1
    #print(total_sample_per_file)
    file_index, sample_index = getFileAndSampleIndex(index, total_sample_per_file)
    #print([file_index, sample_index, target_size[2]])
    #input()
    x = data_file.root.data[file_index, :, :, :, sample_index:sample_index+target_size[2]]
    y = data_file.root.truth[file_index, 0, :, :, sample_index:sample_index+target_size[2]]
    return x, y


def addData(x_list, y_list, target_size, data_file, index, augment=False, dataAugConfig=None):
    x, y = getImageByIndex(data_file, target_size, index)
    if augment:
        x, y = augmentData(x, y,
                           featurewise_center=dataAugConfig["featurewise_center"],
                           samplewise_center=dataAugConfig["samplewise_center"],
                           featurewise_std_normalization=dataAugConfig["featurewise_std_normalization"],
                           samplewise_std_normalization=dataAugConfig["samplewise_std_normalization"],
                           zca_whitening=dataAugConfig["ZCA_whitening"],
                           zca_epsilon=dataAugConfig["ZCA_epsilon"],
                           rotation_range=dataAugConfig["rotation_range"],
                           width_shift_range=dataAugConfig["width_shift_range"],
                           height_shift_range=dataAugConfig["height_shift_range"],
                           brightness_range=dataAugConfig["brightness_range"],
                           shear_range=dataAugConfig["shear_range"],
                           zoom_range=dataAugConfig["zoom_range"],
                           channel_shift_range=dataAugConfig["channel_shift_range"],
                           fill_mode=dataAugConfig["fill_mode"],
                           cval=dataAugConfig["cval"],
                           horizontal_flip=dataAugConfig["horizontal_flip"],
                           vertical_flip=dataAugConfig["vertical_flip"],
                           rescale=dataAugConfig["rescale"],
                           )
    x_list.append(x)
    y_list.append(y)


def getOneHotLabels(y_list, n_labels=2, squeezed=True):
    y_array = np.asarray(y_list)
    if squeezed:
        new_shape = [y_array.shape[0], n_labels] + list(y_array.shape[1:])
    else:
        new_shape = [y_array.shape[0], n_labels] + list(y_array.shape[2:])

    y = np.zeros(new_shape, np.int8)
    for label_index in range(n_labels):
        if squeezed:
            y[:, label_index][y_list == label_index] = 1
        else:
            y[:, label_index][y_list[:, 0] == label_index] = 1
    return y


def getNumberOfSteps(n_samples, batch_size):
    if n_samples <= batch_size:
        return n_samples
    else:
        return int(np.ceil(n_samples/batch_size))
