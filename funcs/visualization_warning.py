# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append("..")

from GUI.VisualizationToolWarning import Ui_Dialog

class VisualizationWarningDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(VisualizationWarningDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        #  Makes Qt delete this widget when the widget has accepted the close event
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
