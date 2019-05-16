# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from keras.models import load_model
from keras import optimizers
from keras.callbacks import ModelCheckpoint, CSVLogger, LearningRateScheduler, ReduceLROnPlateau, EarlyStopping, TerminateOnNaN, TensorBoard
import math
from functools import partial
from keras import applications

from model_zoo.isensee2017 import isensee2017_model
from .metrics import (dice_coef, dice_coef_loss, dice_coefficient, dice_coefficient_loss,
                      weighted_dice_coefficient, weighted_dice_coefficient_loss,
                      weighted_dice_coeff_softmax, weighted_dice_loss_softmax)

def getOptimizer(optimizer, learning_rate, optimizer_config):
    if optimizer == "Adam":
        return optimizers.Adam(lr=learning_rate)
    elif optimizer == "SGD":
        return optimizers.SGD(lr=learning_rate)
    elif optimizer == "RMSprop":
        return optimizers.RMSprop(lr=learning_rate)
    elif optimizer == "Adagrad":
        return optimizers.Adagrad(lr=learning_rate)
    elif optimizer == "Adadelta":
        return optimizers.Adadelta(lr=learning_rate)
    elif optimizer == "Adamax":
        return optimizers.Adamax(lr=learning_rate)
    elif optimizer == "Nadam":
        return optimizers.Nadam(lr=learning_rate)
    else:
        raise ValueError("Fail to recognize optimizer: %s"%optimizer)

def getLossFunction(loss, loss_config):
    if loss.lower() == "dice_coefficient_loss" or loss.lower() == "dice loss":
        return dice_coefficient_loss
    elif loss.lower() == "weighted_dice_coefficient_loss":
        return weighted_dice_coefficient_loss
    elif loss.lower() == "weighted_dice_loss_softmax":
        return  weighted_dice_loss_softmax
    else:
        raise ValueError(" 'Loss' should be chosen from the loss library. '{}' is not recognized".format(
            loss))

# learning rate schedule
def stepDecay(epoch, initial_lrate, drop, epochs_drop):
    return initial_lrate * math.pow(drop, math.floor((1+epoch)/float(epochs_drop)))

def getCallbacks(model_file, save_best_only=True, initial_learning_rate=0.0001, learning_rate_drop=0.5, learning_rate_epochs=None,
                  learning_rate_patience=50, logging_file="./training.log", tensorboard_log_dir='./logs', verbosity=1,
                  early_stopping_patience=None, isTrainingLogs=False, isTensorboard=False):
    callbacks = list()
    callbacks.append(TerminateOnNaN())
    callbacks.append(ModelCheckpoint(model_file, save_best_only=save_best_only))
    if isTrainingLogs:
        callbacks.append(CSVLogger(logging_file, append=True))
    if learning_rate_epochs:
        callbacks.append(LearningRateScheduler(partial(stepDecay, initial_lrate=initial_learning_rate,
                                                       drop=learning_rate_drop, epochs_drop=learning_rate_epochs)))
    '''else:
        callbacks.append(ReduceLROnPlateau(factor=learning_rate_drop, patience=learning_rate_patience,
                                           verbose=verbosity))'''
    if isTensorboard:
        callbacks.append(TensorBoard(log_dir=tensorboard_log_dir))
    if early_stopping_patience:
        callbacks.append(EarlyStopping(verbose=verbosity, patience=early_stopping_patience))
    return callbacks

def createModel(config_class, input_shape, model_type):
    optimizer = getOptimizer(config_class.config["OptimizerConfig"]["optimizer"],
                             learning_rate=config_class.config["learning_rate"],
                             optimizer_config=config_class.config["OptimizerConfig"])
    loss_function = getLossFunction(loss=config_class.config["LossConfig"]["loss"],
                                    loss_config=config_class.config["LossConfig"])
    #print(model_type is 'isensee2017')
    #print(model_type == 'isensee2017')
    if model_type == 'isensee2017':
        model = isensee2017_model(input_shape=input_shape,
                                  n_labels=config_class.config["num_class"])
    #elif model_type == 'VGG16':
    #    model = applications.vgg16.VGG16(include_top=False, input_shape=input_shape,
    #                                     classes)
    else:
        raise ValueError(" 'Model' should be chosen from the model library. '{}' is not recognized".format(
            model_type))
    model.compile(optimizer=optimizer, loss=loss_function)
    return model

def loadOldModel(model_file):
    print("Loading pre-trained model")
    custom_objects = {'dice_coefficient_loss': dice_coefficient_loss, 'dice_coefficient': dice_coefficient,
                      'dice_coef': dice_coef, 'dice_coef_loss': dice_coef_loss,
                      'weighted_dice_coefficient': weighted_dice_coefficient,
                      'weighted_dice_coefficient_loss': weighted_dice_coefficient_loss,
                      'weighted_dice_coefficient_softmax': weighted_dice_coeff_softmax,
                      'weighted_dice_loss_softmax': weighted_dice_loss_softmax}
    try:
        from keras_contrib.layers import InstanceNormalization
        custom_objects["InstanceNormalization"] = InstanceNormalization
    except ImportError:
        pass
    try:
        return load_model(model_file, custom_objects=custom_objects)
    except ValueError as error:
        if 'InstanceNormalization' in str(error):
            raise ValueError(str(error) + "\n\nPlease install keras-contrib to use InstanceNormalization:\n"
                                          "'pip install git+https://www.github.com/keras-team/keras-contrib.git'")
        else:
            raise error


def trainModel(model, model_file, training_generator, validation_generator, steps_per_epoch, validation_steps,
                initial_learning_rate=0.001, learning_rate_drop=0.5, learning_rate_epochs=None, n_epochs=500,
                learning_rate_patience=20, early_stopping_patience=None, isTrainingLogs=False, TrainingLogs=None,
               isTensorboard=False, tensorboard_log_dir="./logs"):
    """
    Train a Keras model.
    :param early_stopping_patience: If set, training will end early if the validation loss does not improve after the
    specified number of epochs.
    :param learning_rate_patience: If learning_rate_epochs is not set, the learning rate will decrease if the validation
    loss does not improve after the specified number of epochs. (default is 20)
    :param model: Keras model that will be trained.
    :param model_file: Where to save the Keras model.
    :param training_generator: Generator that iterates through the training data.
    :param validation_generator: Generator that iterates through the validation data.
    :param steps_per_epoch: Number of batches that the training generator will provide during a given epoch.
    :param validation_steps: Number of batches that the validation generator will provide during a given epoch.
    :param initial_learning_rate: Learning rate at the beginning of training.
    :param learning_rate_drop: How much at which to the learning rate will decay.
    :param learning_rate_epochs: Number of epochs after which the learning rate will drop.
    :param n_epochs: Total number of epochs to train the model.
    :return:
    """
    if training_generator is None:
        raise ValueError("No training data is detected!")
    if validation_generator is None:
        save_best_only = False
    else:
        save_best_only = True

    model.fit_generator(generator=training_generator,
                        steps_per_epoch=steps_per_epoch,
                        epochs=n_epochs,
                        validation_data=validation_generator,
                        validation_steps=validation_steps,
                        use_multiprocessing=True,
                        callbacks=getCallbacks(model_file,
                                               save_best_only=save_best_only,
                                                initial_learning_rate=initial_learning_rate,
                                                learning_rate_drop=learning_rate_drop,
                                                learning_rate_epochs=learning_rate_epochs,
                                                learning_rate_patience=learning_rate_patience,
                                                early_stopping_patience=early_stopping_patience,
                                               isTrainingLogs=isTrainingLogs,
                                               logging_file=TrainingLogs,
                                               isTensorboard=isTensorboard,
                                               tensorboard_log_dir=tensorboard_log_dir))
