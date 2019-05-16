# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from segmentation.segmentation_train import train
from funcs import testfunc


class SegmentationTrain(QtCore.QObject):
    finished = QtCore.pyqtSignal(str)

    def __init__(self, thread_index=0, config_class=None, parent=None):
        super(self.__class__, self).__init__(parent)
        self.thread_index = thread_index
        self.config_class = config_class

    @QtCore.pyqtSlot()
    def startTraining(self):
        self.trainingFunc()
        self.finished.emit(str(self.thread_index))

    def trainingFunc(self):
        train(self.config_class)
        #testfunc.mnist_cnn_config(self.config_class)

class ClassificationTrain(QtCore.QObject):
    finished = QtCore.pyqtSignal(str)

    def __init__(self, thread_index=0, config_class=None, parent=None):
        super(self.__class__, self).__init__(parent)
        self.thread_index = thread_index
        self.config_class = config_class

    @QtCore.pyqtSlot()
    def startTraining(self):
        self.trainingFunc()
        self.finished.emit(str(self.thread_index))

    def trainingFunc(self):
        #train(self.config_class)
        testfunc.mnist_cnn_config(self.config_class)
