# -*- coding: utf-8 -*-
import numpy as np

NORMALIZATION_TYPE=['standard', 'interval']

def normalizeDataToStd(data, mean, std):
    data -= mean[:, np.newaxis, np.newaxis, np.newaxis]
    data /= std[:, np.newaxis, np.newaxis, np.newaxis]
    return data


def normalizeDataStorage(data_storage, normalization_type):
    if normalization_type == "standard":
        mean, std = getMeanAndStd(data_storage)
        for index in range(data_storage.shape[0]):
            data_storage[index] = normalizeDataToStd(data_storage[index], mean, std)
        return data_storage

def getMeanAndStd(data_storage):
    means = list()
    stds = list()
    for index in range(data_storage.shape[0]):
        data = data_storage[index]
        means.append(data.mean(axis=(1, 2, 3)))
        stds.append(data.std(axis=(1, 2, 3)))
    mean = np.asarray(means).mean(axis=0)
    std = np.asarray(stds).mean(axis=0)
    return mean, std

def normalizeToInterval(data_storage, min_value=None, max_value=None, normalization_range='global'):
    if normalization_range == 'global':
        data_min = np.min(data_storage)
        data_max = np.max(data_storage)

        data_storage -= data_min
        data_storage /= (data_max - data_min)/(max_value - min_value)
        data_storage += min_value


    elif normalization_range == 'per_slice':
        data_min = np.min(data_storage, axis=4, keepdims=True)
        data_max = np.max(data_storage, axis=4, keepdims=True)

        data_storage -= data_min
        data_storage /= (data_max - data_min)/(max_value - min_value)
        data_storage += min_value

    elif normalization_range == 'per_volume':
        data_min = np.min(data_storage, axis=4, keepdims=True)
        data_max = np.max(data_storage, axis=4, keepdims=True)

        data_storage -= data_min
        data_storage /= (data_max - data_min) / (max_value - min_value)
        data_storage += min_value

    else:
        print("Fail to recognize normalization range: %s" % normalization_range)
        Warning("The data has not been normalized!")


def normalizeToStandardDistribution(data_storage, normalization_range='global'):
    if normalization_range == 'global':
        mean = np.mean(data_storage)
        std = np.std(data_storage)

        data_storage -= mean
        data_storage /= std

    elif normalization_range == 'per_slice':
        mean = np.mean(data_storage, axis=4, keepdims=True)
        std = np.std(data_storage, axis=4, keepdims=True)

        data_storage -= mean
        data_storage /= std

    elif normalization_range == 'per_volume':
        mean = np.mean(data_storage, axis=(1,2,3,4), keepdims=True)
        std = np.std(data_storage, axis=(1,2,3,4), keepdims=True)

        data_storage -= mean
        data_storage /= std

    else:
        print("Fail to recognize normalization range: %s"%normalization_range)
        Warning("The data has not been normalized!")

