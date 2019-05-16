from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append("..")
from GUI.Data_management_messagebox import Ui_Dialog

class DataManageMessageBox(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(DataManageMessageBox, self).__init__(parent)
        self.setupUi(self)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)