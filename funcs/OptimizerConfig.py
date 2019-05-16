# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append("..")

from GUI.OptimizerConfiguration import Ui_Dialog

class OptimizerDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(OptimizerDialog, self).__init__(parent)
        self.setupUi(self)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.OptimizerConfig = {}
        self.initializeOptimizerConfig()
        self.isDestroyed = False

        self.pushButton.clicked.connect(self.getOptimizerConfig)
        self.pushButton_2.clicked.connect(self.cancel)


    def initializeOptimizerConfig(self):
        self.OptimizerConfig['optimizer'] = self.getSelectedOptimizer()

    def getSelectedOptimizer(self):
        radiobuttons = self.groupBox.findChildren(QtWidgets.QRadioButton)
        for items in radiobuttons:
            if items.isChecked():
                return items.text()


    def getConfig(self):
        self.OptimizerConfig["optimizer"] = self.getSelectedOptimizer()

    def check(self):
        result = dict()
        result['Valid_config'] = True
        return result

    def getOptimizerConfig(self):
        self.getConfig()
        result = self.check()
        if result['Valid_config']:
            print('Optimizer Config Done!')
            self.parent().updateOptimizerLabelValue()
            self.hide()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", '\nWrong Configuration!\n' + result['Message'])

    def cancel(self):
        self.isDestroyed = True
        self.close()