# -*- coding: utf-8 -*-

from keras import backend as K

def linear_2_softmax(x):
    y = K.exp(x)
    z = x - K.logsumexp(x, axis=1, keepdims=True)
    y = K.exp(z)
    return y

def linear_2_sigmoid(x):
    y = K.sigmoid(x)
    return y

def weighted_dice_coeff_softmax(y_true_all, y_pred_linear, axis = (-3, -2, -1), smooth = 0.00001):
    y_pred_all = linear_2_softmax(y_pred_linear)
    y_pred = y_pred_all[:, 1::, :, :, :]
    y_true = y_true_all[:, 1::, :, :, :]
    return K.mean(2. * (K.sum(y_true * y_pred,
                              axis=axis) + smooth/2)/(K.sum(y_true,
                                                            axis=axis) + K.sum(y_pred,
                                                                               axis=axis) + smooth))

def weighted_dice_loss_softmax(y_true, y_pred_linear):
    return -weighted_dice_coeff_softmax(y_true, y_pred_linear)

def dice_coefficient(y_true, y_pred_linear, smooth=1.):
    y_pred = linear_2_sigmoid(y_pred_linear)
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


def dice_coefficient_loss(y_true, y_pred_linear):
    return -dice_coefficient(y_true, y_pred_linear)


def weighted_dice_coefficient(y_true, y_pred_linear, axis=(-3, -2, -1), smooth=0.00001):
    """
    Weighted dice coefficient. Default axis assumes a "channels first" data structure
    :param smooth:
    :param y_true:
    :param y_pred:
    :param axis:
    :return:
    """
    y_pred = linear_2_sigmoid(y_pred_linear)
    return K.mean(2. * (K.sum(y_true * y_pred,
                              axis=axis) + smooth/2)/(K.sum(y_true,
                                                            axis=axis) + K.sum(y_pred,
                                                                               axis=axis) + smooth))


def weighted_dice_coefficient_loss(y_true, y_pred_linear):
    return -weighted_dice_coefficient(y_true, y_pred_linear)


def label_wise_dice_coefficient(y_true, y_pred_linear, label_index):
    return dice_coefficient(y_true[:, label_index], y_pred_linear[:, label_index])


dice_coef = dice_coefficient
dice_coef_loss = dice_coefficient_loss