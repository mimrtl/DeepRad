# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append("..")

from funcs import task
from GUI.test import Ui_MainWindow

class MainWindow2(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow2, self).__init__(parent)

        self.setupUi(self)
        self.setupMain()

    def setupMain(self):
        #self.MainWindow = MainWindow
        self.pushButton.clicked.connect(self.clickMethod)

    def clickMethod(self):
        self.hide()
        self.taskwindow = task.mainwindow(self)
        #self.DeepRadMain1.setupUi(self.MainWindow)
        #self.DeepRadMain1.setupMain(self.MainWindow)
        self.taskwindow.show()

        #self.setupUi(self)
        #self.setupMain(self)
        #self.MainWindow.show()

