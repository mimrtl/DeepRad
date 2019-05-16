# -*- coding: utf-8 -*-
import tables
import pickle
import os
import glob
import numpy as np
import SimpleITK as sitk
import collections
import nibabel as nib
from nilearn.image import reorder_img, new_img_like
import cv2
from PIL import Image
import h5py
import csv

from include.normalization import normalizeDataStorage

def pickle_dump(item, out_file):
    with open(out_file, "wb") as opened_file:
        pickle.dump(item, opened_file)

def pickle_load(in_file):
    with open(in_file, "rb") as opened_file:
        return pickle.load(opened_file)

def calculateOriginOffset(new_spacing, old_spacing):
    return np.subtract(new_spacing, old_spacing)/2

def dataToSitkImage(data, spacing=(1., 1., 1.)):
    if len(data.shape) == 3:
        data = np.rot90(data, 1, axes=(0, 2))
    image = sitk.GetImageFromArray(data)
    image.SetSpacing(np.asarray(spacing, dtype=np.float))
    return image


def sitkImageToData(image):
    data = sitk.GetArrayFromImage(image)
    if len(data.shape) == 3:
        data = np.rot90(data, -1, axes=(0, 2))
    return data

def createDataFile(out_file, n_modalities, n_samples, image_shape):
    hdf5_file = tables.open_file(out_file, mode='w')
    filters = tables.Filters(complevel=5, complib='blosc')
    data_shape = tuple([0, n_modalities] + list(image_shape))
    truth_shape = tuple([0, 1] + list(image_shape))
    data_storage = hdf5_file.create_earray(hdf5_file.root, 'data', tables.Float32Atom(), shape=data_shape,
                                           filters=filters, expectedrows=n_samples)
    truth_storage = hdf5_file.create_earray(hdf5_file.root, 'truth', tables.UInt8Atom(), shape=truth_shape,
                                            filters=filters, expectedrows=n_samples)
    affine_storage = hdf5_file.create_earray(hdf5_file.root, 'affine', tables.Float32Atom(), shape=(0, 4, 4),
                                             filters=filters, expectedrows=n_samples)
    return hdf5_file, data_storage, truth_storage, affine_storage

def openDataFile(filename, readwrite="r"):
    return tables.open_file(filename, readwrite)

def fetchCSVFiles(data_path, return_subject_ids=False):
    training_data_files = list()
    subject_ids = list()



def fetchTrainingDataFiles(effective_modalities, data_path, return_subject_ids=False):
    training_data_files = list()
    subject_ids = list()
    for subject_dir in glob.glob(os.path.join(data_path, "preprocessed", "*", "*")):
        subject_ids.append(os.path.basename(subject_dir))
        subject_files = list()
        for modality in effective_modalities + ["truth"]:
            subject_files.append(os.path.join(subject_dir, modality + ".nii.gz"))
        training_data_files.append(tuple(subject_files))
    if return_subject_ids:
        return training_data_files, subject_ids
    else:
        return training_data_files

def sitkNewBlankImage(size, spacing, direction, origin, default_value=0.):
    image = sitk.GetImageFromArray(np.ones(size, dtype=np.float).T * default_value)
    image.SetSpacing(spacing)
    image.SetDirection(direction)
    image.SetOrigin(origin)
    return image

def sitkResampleToImage(image, reference_image, default_value=0., interpolator=sitk.sitkLinear, transform=None,
                           output_pixel_type=None):
    if transform is None:
        transform = sitk.Transform()
        transform.SetIdentity()
    if output_pixel_type is None:
        output_pixel_type = image.GetPixelID()
    resample_filter = sitk.ResampleImageFilter()
    resample_filter.SetInterpolator(interpolator)
    resample_filter.SetTransform(transform)
    resample_filter.SetOutputPixelType(output_pixel_type)
    resample_filter.SetDefaultPixelValue(default_value)
    resample_filter.SetReferenceImage(reference_image)
    return resample_filter.Execute(image)

def sitkResampleToSpacing(image, new_spacing=(1.0, 1.0, 1.0), interpolator=sitk.sitkLinear, default_value=0.):
    zoom_factor = np.divide(image.GetSpacing(), new_spacing)
    new_size = np.asarray(np.ceil(np.round(np.multiply(zoom_factor, image.GetSize()), decimals=5)), dtype=np.int16)
    offset = calculateOriginOffset(new_spacing, image.GetSpacing())
    reference_image = sitkNewBlankImage(size=new_size, spacing=new_spacing, direction=image.GetDirection(),
                                           origin=image.GetOrigin() + offset, default_value=default_value)
    return sitkResampleToImage(image, reference_image, interpolator=interpolator, default_value=default_value)

def readImageFiles(image_files, image_shape=None, label_indices=None):
    """

    :param image_files:
    :param image_shape:
    :param crop:
    :param use_nearest_for_last_file: If True, will use nearest neighbor interpolation for the last file. This is used
    because the last file may be the labels file. Using linear interpolation here would mess up the labels.
    :return:
    """
    if label_indices is None:
        label_indices = []
    elif not isinstance(label_indices, collections.Iterable) or isinstance(label_indices, str):
        label_indices = [label_indices]
    image_list = list()
    for index, image_file in enumerate(image_files):
        if (label_indices is None and (index + 1) == len(image_files)) \
                or (label_indices is not None and index in label_indices):
            interpolation = "nearest"
        else:
            interpolation = "linear"
        image_list.append(readImage(image_file, image_shape=image_shape, interpolation=interpolation))

    return image_list

def readImage(in_file, image_shape=None, interpolation='linear'):
    print("Reading: {0}".format(in_file))
    image = nib.load(os.path.abspath(in_file))
    image = fixShape(image)
    if image_shape:
        return resize(image, new_shape=image_shape, interpolation=interpolation)
    else:
        return image

def readCSV(in_file):
    labels = list()
    with open(in_file, "r") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            try:
                row = np.asarray(row).astype(np.int32)
            except:
                continue
            labels.append(row)
    return np.squeeze(np.asarray(labels))

def readDictFromCSV(in_file):
    labels = dict()
    with open(in_file, "r") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            try:
                label = np.asarray(row[1:]).astype(np.int32)
            except:
                continue
            labels[row[0]] = np.squeeze(label)
    return labels

def fixShape(image):
    if image.shape[-1] == 1:
        return image.__class__(dataobj=np.squeeze(image.get_data()), affine=image.affine)
    return image

def resampleToSpacing(data, spacing, target_spacing, interpolation="linear", default_value=0.):
    image = dataToSitkImage(data, spacing=spacing)
    if interpolation is "linear":
        interpolator = sitk.sitkLinear
    elif interpolation is "nearest":
        interpolator = sitk.sitkNearestNeighbor
    else:
        raise ValueError("'interpolation' must be either 'linear' or 'nearest'. '{}' is not recognized".format(
            interpolation))
    resampled_image = sitkResampleToSpacing(image, new_spacing=target_spacing, interpolator=interpolator,
                                               default_value=default_value)
    return sitkImageToData(resampled_image)

def resize(image, new_shape, interpolation="linear"):
    image = reorder_img(image, resample=interpolation)
    zoom_level = np.divide(new_shape, image.shape)
    new_spacing = np.divide(image.header.get_zooms(), zoom_level)
    new_data = resampleToSpacing(image.get_data(), image.header.get_zooms(), new_spacing,
                                   interpolation=interpolation)
    new_affine = np.copy(image.affine)
    np.fill_diagonal(new_affine, new_spacing.tolist() + [1])
    new_affine[:3, 3] += calculateOriginOffset(new_spacing, image.header.get_zooms())
    return new_img_like(image, new_data, affine=new_affine)

def resizeArray(array, new_size, interpolation):
    # resize an image into new_size (w * h) using specified interpolation
    # opencv has a weird rounding issue & this is a hacky fix
    # ref: https://github.com/opencv/opencv/issues/9096
    mapping_dict = {cv2.INTER_NEAREST: Image.NEAREST}
    if interpolation in mapping_dict:
        pil_img = Image.fromarray(array)
        pil_img = pil_img.resize(new_size,
                             resample=mapping_dict[interpolation])
        img = np.array(pil_img)
    else:
        img = cv2.resize(array, new_size,
                     interpolation=interpolation)
    return img

def resliceImageSet(in_files, image_shape, out_files=None, label_indices=None):
    images = readImageFiles(in_files, image_shape=image_shape, label_indices=label_indices)
    if out_files:
        for image, out_file in zip(images, out_files):
            image.to_filename(out_file)
        return [os.path.abspath(out_file) for out_file in out_files]
    else:
        return images

def writeImageDataToFile(image_files, data_storage, truth_storage, image_shape, n_modalities, affine_storage,
                             truth_dtype=np.uint8):
    for set_of_files in image_files:
        images = resliceImageSet(set_of_files, image_shape, label_indices=len(set_of_files) - 1)
        subject_data = [image.get_data() for image in images]
        addDataToStorage(data_storage, truth_storage, affine_storage, subject_data, images[0].affine, n_modalities,
                            truth_dtype)
    return data_storage, truth_storage


def addDataToStorage(data_storage, truth_storage, affine_storage, subject_data, affine, n_modalities, truth_dtype):
    data_storage.append(np.asarray(subject_data[:n_modalities])[np.newaxis])
    truth_storage.append(np.asarray(subject_data[n_modalities], dtype=truth_dtype)[np.newaxis][np.newaxis])
    affine_storage.append(np.asarray(affine)[np.newaxis])

def preprocessAndSaveDataToFile(training_data_files, out_file, image_shape, truth_dtype=np.uint8, subject_ids=None,
                                normalize=True, normalization_type='standard'):
    """
    Takes in a set of training images and writes those images to an hdf5 file.
    :param training_data_files: List of tuples containing the training data files. The modalities should be listed in
    the same order in each tuple. The last item in each tuple must be the labeled image.
    Example: [('sub1-T1.nii.gz', 'sub1-T2.nii.gz', 'sub1-truth.nii.gz'),
                ('sub2-T1.nii.gz', 'sub2-T2.nii.gz', 'sub2-truth.nii.gz')]
    :param out_file: Where the hdf5 file will be written to.
    :param image_shape: Shape of the images that will be saved to the hdf5 file.
    :param truth_dtype: Default is 8-bit unsigned integer.
    :return: Location of the hdf5 file with the image data written to it.
    """
    n_samples = len(training_data_files)
    n_modalities = len(training_data_files[0]) - 1

    try:
        hdf5_file, data_storage, truth_storage, affine_storage = createDataFile(out_file,
                                                                                  n_modalities=n_modalities,
                                                                                  n_samples=n_samples,
                                                                                  image_shape=image_shape)
    except Exception as e:
        # If something goes wrong, delete the incomplete data file
        os.remove(out_file)
        raise e

    writeImageDataToFile(training_data_files, data_storage, truth_storage, image_shape,
                             truth_dtype=truth_dtype, n_modalities=n_modalities, affine_storage=affine_storage)
    if subject_ids:
        hdf5_file.create_array(hdf5_file.root, 'subject_ids', obj=subject_ids)
    if normalize:
        normalizeDataStorage(data_storage, normalization_type=normalization_type)
    hdf5_file.close()
    return out_file

def nii2hdf5(data_path, out_file):
    hdf5_file = h5py.File(out_file, mode='w')
    group = hdf5_file.create_group("data")
    image = None
    for subject in glob.glob(os.path.join(data_path, "*.nii.gz")):
        if os.path.isfile(subject):
            name = os.path.basename(subject)
            image = nib.load(subject)
            group.create_dataset(name, data=np.asarray(image.get_data()))
    if image:
        hdf5_file.create_dataset("affine", data=np.asarray(image.affine))
    hdf5_file.close()

if __name__ == '__main__':
    nii2hdf5("../data", '../data/test.h5')

