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
