# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append("..")

from GUI.VisualizationTool import Ui_Dialog
from GUI.VisualizationToolMainWindow import Ui_MainWindow
from funcs.visualization_warning import VisualizationWarningDialog as VTWarning

from include.figure import MyFigure


class VisualizationMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, index=None, parent=None):
        super(VisualizationMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setupMain()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        #  Makes Qt delete this widget when the widget has accepted the close event
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.GUIindex = index

    def setupMain(self):
        self.warning = VTWarning(self)
        self.initializeWarningDialog()

        self.F = MyFigure(width=3, height=2, dpi=100)
        self.gridlayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridlayout.addWidget(self.F)

        self.pushButton.clicked.connect(self.askterminate)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.clicked.connect(self.closeWindowAfterThreadFinished)

    def plotFigure(self, x, y):
        self.F.axes.clear()
        self.F.axes.plot(x, y)
        self.F.fig.suptitle("Train Loss")
        self.F.axes.grid()
        self.F.draw()

    def closeWindowAfterThreadFinished(self):
        self.close()

    def initializeWarningDialog(self):
        self.warning.buttonBox.rejected.connect(self.CancelClickedInWarning)
        self.warning.buttonBox.accepted.connect(self.OKClickedInWarning)

    def askterminate(self):
        self.popOutWarningDialog()

    def popOutWarningDialog(self):
        self.warning.show()

    def CancelClickedInWarning(self):
        self.warning = VTWarning(self)
        self.initializeWarningDialog()

    def OKClickedInWarning(self):
        self.terminate()

    def terminate(self):
        self.parent().terminateSystem(str(self.GUIindex))


class VisualizationDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, index=None, parent=None):
        super(VisualizationDialog, self).__init__(parent)
        self.setupUi(self)
        self.setupMain()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        #  Makes Qt delete this widget when the widget has accepted the close event
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.GUIindex = index

    def setupMain(self):
        self.warning = VTWarning(self)
        self.initializeWarningDialog()

        self.pushButton.clicked.connect(self.askterminate)

    def initializeWarningDialog(self):
        self.warning.buttonBox.rejected.connect(self.CancelClickedInWarning)
        self.warning.buttonBox.accepted.connect(self.OKClickedInWarning)

    def askterminate(self):
        self.popOutWarningDialog()

    def popOutWarningDialog(self):
        self.warning.show()

    def CancelClickedInWarning(self):
        self.warning = VTWarning(self)
        self.initializeWarningDialog()

    def OKClickedInWarning(self):
        self.terminate()

    def terminate(self):
        self.parent().terminateTrainingThread(str(self.GUIindex))
        self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    classtmp = VisualizationDialog()
    classtmp.popOutWarningDialog()
    sys.exit(app.exec_())
