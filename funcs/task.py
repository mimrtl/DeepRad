# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append("..")

from GUI.tasksGUI import Ui_MainWindow
from funcs import DeepRad_classification_func, DeepRad_segmentation_func, DataManage

class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent):
        super(mainwindow, self).__init__(parent)
        self.setupUi(self)
        self.setupMain()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def setupMain(self):
        #self.pushButton.clicked.connect(self.openClassification)
        self.pushButton.setIcon(QtGui.QIcon('./image/classification.png'))
        self.pushButton.setIconSize(QtCore.QSize(171, 171))

        self.pushButton_2.clicked.connect(self.openSegmentation)
        self.pushButton_2.setIcon(QtGui.QIcon('./image/segmentation.png'))
        self.pushButton_2.setIconSize(QtCore.QSize(171, 171))

        self.pushButton_4.setIcon(QtGui.QIcon('./image/synthesis.jpeg'))
        self.pushButton_4.setIconSize(QtCore.QSize(171, 171))

        self.pushButton_3.setIcon(QtGui.QIcon('./image/regression.png'))
        self.pushButton_3.setIconSize(QtCore.QSize(171, 171))

        self.menubar.setNativeMenuBar(False)
        self.actionBack.setShortcut("Ctrl+B")
        self.actionBack.setStatusTip("Back to the main window")
        self.actionBack.triggered.connect(self.clickMethod)
        self.actionData_Management.triggered.connect(self.openDataManagement)

    def clickMethod(self):
        self.close()
        self.parent().show()

    def openClassification(self):
        self.hide()
        self.DeepRad_Classification_Main = DeepRad_classification_func.mainwindow(self)
        self.DeepRad_Classification_Main.show()

    def openSegmentation(self):
        self.hide()
        self.DeepRad_Segmentation_Main = DeepRad_segmentation_func.mainwindow(self)
        self.DeepRad_Segmentation_Main.show()

    def openDataManagement(self):
        self.hide()
        self.DataManageMain = DataManage.mainwindow(self)
        self.DataManageMain.show()
