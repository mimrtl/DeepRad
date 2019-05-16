# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append("..")

from GUI.LossConfiguration import Ui_Dialog


class LossDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(LossDialog, self).__init__(parent)
        self.setupUi(self)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.initializeComboBoxText(parent.loss_list)
        self.LossConfig = {}
        self.initializeLossConfig()
        self.isDestroyed = False

        self.pushButton.clicked.connect(self.getLossConfig)
        self.pushButton_2.clicked.connect(self.cancel)

    def initializeComboBoxText(self, loss_list):
        for loss in loss_list:
            self.comboBox.addItem(loss)

    def initializeLossConfig(self):
        self.LossConfig['loss'] = self.comboBox.currentText()

    def getConfig(self):
        self.LossConfig["loss"] = self.comboBox.currentText()

    def check(self):
        result = dict()
        result['Valid_config'] = True
        return result

    def getLossConfig(self):
        self.getConfig()
        result = self.check()
        if result['Valid_config']:
            print('Loss Config Done!')
            self.parent().updateLossLabelValue()
            self.hide()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", '\nWrong Configuration!\n' + result['Message'])

    def cancel(self):
        self.isDestroyed = True
        self.close()