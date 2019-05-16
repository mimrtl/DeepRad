# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
sys.path.append("..")
import os
import glob
import nibabel
import numpy as np
import qimage2ndarray as q2n
import h5py

from GUI.DataManagement import Ui_MainWindow
from funcs.data_management_messagebox import DataManageMessageBox
import funcs.dataUtilities as du
from include.utils import isValidPath, isValidFloatNumberString,\
    str2float, isValidRelation, isValidIntNumberString, str2int
from data_management.data_management import DataManagementClass


def listOfStr2Str(str_list, seperator = ""):
    string = ""
    for item in str_list:
        string += seperator
        string += item
    return string

class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(mainwindow, self).__init__(parent)
        self.setupUi(self)
        self.setupMain()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


    def setupMain(self):
        self.menubar.setNativeMenuBar(False)
        self.actionBack.setShortcut("Ctrl+B")
        self.actionBack.setStatusTip("Back to the main window")
        self.actionBack.triggered.connect(self.clickMethod)

        self.pushButton.clicked.connect(self.setInputPath)
        self.pushButton_2.clicked.connect(self.previousSlice)
        self.pushButton_3.clicked.connect(self.nextSlice)
        self.pushButton_4.clicked.connect(self.firstSlice)
        self.pushButton_5.clicked.connect(self.lastSlice)
        self.pushButton_9.clicked.connect(self.selectedSlice)
        self.pushButton_7.clicked.connect(self.setOutputPath)
        self.pushButton_8.clicked.connect(self.convertData)
        self.pushButton_10.clicked.connect(self.rotate)

        self.comboBox.activated.connect(self.chooseFile)
        self.comboBox_4.activated.connect(self.chooseSliceOrient)

        self.comboBox_3.activated.connect(self.activateMinMaxConfiguration)
        self.comboBox_5.setDisabled(True)
        self.lineEdit_4.setDisabled(True)
        self.lineEdit_5.setDisabled(True)

        self.index = 0
        self.numImagePerVolume = 0
        self.output_path = ''
        self.slice_orient = 'Axial'
        self.current_file_name = ''
        self.rotate_degree = 0

    def activateMinMaxConfiguration(self):
        if self.comboBox_3.currentText() == "None":
            self.comboBox_5.setDisabled(True)
        else:
            self.comboBox_5.setEnabled(True)

        if self.comboBox_3.currentText() == "interval":
            self.lineEdit_4.setEnabled(True)
            self.lineEdit_5.setEnabled(True)
        else:
            self.lineEdit_4.setDisabled(True)
            self.lineEdit_5.setDisabled(True)


    def initializeConfiguration(self):
        self.config = dict()
        self.check_result = list()
        self.check_success = True
        self.transform_success = True

    def getConfiguration(self):
        self.config["data_folder"] = self.lineEdit_8.text()
        self.config["output_folder"] = self.lineEdit_9.text()
        self.config["normalize_mode"] = self.comboBox_3.currentText()
        self.config["normalize_range"] = self.comboBox_5.currentText()
        self.config["min_value"] = self.lineEdit_4.text()
        self.config["max_value"] = self.lineEdit_5.text()
        self.config["row"] = self.lineEdit_6.text()
        self.config["col"] = self.lineEdit_7.text()
        self.config["channel"] = self.lineEdit_10.text()

    def getImageShape(self):
        return (self.config["row"], self.config["col"], self.config["channel"])

    def showErrorDetailInTraining(self, message):
        self.popoutErrorMessageBox("Failed to start training\n Please check the configuration!\n\n %s"%message)


    def checkConfiguration(self):
        if not isValidPath(self.config["data_folder"]):
            self.check_result.append("Data folder does not exist!")
        if not isValidPath(self.config["output_folder"]):
            #self.showInfoInTextBrowser("Warning: output folder does not exist! Will create the folder...")
            self.check_result.append("Output folder does not exist!")
        if not isValidFloatNumberString(self.config["min_value"]):
            self.check_result.append("Invalid input of min value!")
        if not isValidFloatNumberString(self.config["max_value"]):
            self.check_result.append("Invalid input of max value!")
        if not isValidIntNumberString(self.config["row"], min=1):
            self.check_result.append("Invalid input of row number (>=1, integer)!")
        if not isValidIntNumberString(self.config["col"], min=1):
            self.check_result.append("Invalid input of col number (>=1, integer)!")
        if not isValidIntNumberString(self.config["channel"], min=1):
            self.check_result.append("Invalid input of channel number (>=1, integer)!")
        if len(self.check_result)>0:
            self.check_success = False

    def TransformConfiguration(self):
        if self.check_success:
            self.config["min_value"] = str2float(self.config["min_value"])
            self.config["max_value"] = str2float(self.config["max_value"])
            self.config["row"] = str2int(self.config["row"])
            self.config["col"] = str2int(self.config["col"])
            self.config["channel"] = str2int(self.config["channel"])
            if self.config["normalize_mode"] == 'None':
                self.config["normalize_mode"] = None
            if not isValidRelation(min=self.config["min_value"], max=self.config["max_value"]):
                self.check_result.append("Max value is less than min value!")
            if len(self.check_result)>0:
                self.transform_success = False
        else:
            self.showErrorConfigDetail()

    def startConvert(self):
        if self.check_success and self.transform_success:
            data_management = DataManagementClass(data_path=self.config["data_folder"],
                                                  output_path=self.config["output_folder"],
                                                  image_shape=self.getImageShape(),
                                                  min_value=self.config["min_value"],
                                                  max_value=self.config["max_value"],
                                                  normalization_mode=self.config["normalize_mode"],
                                                  normalization_range=self.config["normalize_range"])
            try:
                processing_messagebox = DataManageMessageBox(self)
                processing_messagebox.show()
                data_management.startConvert()
                processing_messagebox.close()
                print("Data HDF5 file successfully generated!")
                self.showInfoInTextBrowser("Data HDF5 file successfully generated!")
            except:
                self.popoutErrorMessageBox(data_management.error_message)

    def popoutErrorMessageBox(self, message):
        QtWidgets.QMessageBox.critical(self, "Error", message)

    def showInfoInTextBrowser(self, message):
        self.textBrowser.append(message)
        QtWidgets.QApplication.processEvents()

    def showErrorConfigDetail(self):
        self.popoutErrorMessageBox(self.getAllMessageString())

    def getAllMessageString(self):
        return listOfStr2Str(self.check_result, seperator='\n')

    def convertData(self):
        self.initializeConfiguration()
        self.getConfiguration()
        self.checkConfiguration()
        self.TransformConfiguration()
        self.startConvert()

    '''def convert(self):
        self.textBrowser.append('-' * 60)
        self.textBrowser.append('Start converting...')
        # overwrite the existing file
        flag = True
        try:
            f = h5py.File(self.filename, 'w')
            f.close()
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Error", '\nWrong output path!\n')
            flag = False

        if flag:
            files = glob.glob(os.path.join(self.download_path, '*.nii.gz'))
            # imageAll = np.zeros(len(files)*self.numImagePerVolume, self.image.shape[0], self.image.shape[1])
            # savefile = os.path.join(self.output_path, 'data.hdf5')
            f = h5py.File(self.filename, 'a')
            count = -1
            for file in files:
                count += 1
                name = file.split('/')[-1]
                self.textBrowser.append(name)
                image = self.loadFile(file)
                f['/%d/slices' % count] = image
                # imageAll[count*self.numImagePerVolume: (count+1)*self.numImagePerVolume] = image
            f.close()
            self.textBrowser.append('Done!')
            self.textBrowser.append('-' * 60)'''

    def showSlice(self):
        self.graphicsView.scene = QtWidgets.QGraphicsScene()
        qimage_tmp = self.image[self.index].copy()
        qimage = q2n.array2qimage(qimage_tmp, normalize=True)
        # qimage = QtGui.QImage(qimage_tmp, qimage_tmp.shape[0], qimage_tmp.shape[1], QtGui.QImage.Format_RGB32)
        p = QtGui.QPixmap.fromImage(qimage)
        item = QtWidgets.QGraphicsPixmapItem(p)
        item.setScale(1)
        item.setTransformOriginPoint(120, 120)
        item.setRotation(self.rotate_degree * 90)
        self.graphicsView.scene.addItem(item)
        self.graphicsView.setScene(self.graphicsView.scene)

    def loadandUpdateFile(self, filename):
        image_raw = nibabel.load(filename)
        if self.slice_orient == 'Axial':
            image = du.resliceToAxial(image_raw.get_data())
        elif self.slice_orient == 'Coronal':
            image = du.resliceToCoronal(image_raw.get_data())
        else:
            image = du.resliceToSagittal(image_raw.get_data())
        #image = du.resliceToAxial(image_raw.get_data())
        #image = du.resliceToSagittal(image_raw.get_data())
        image = image.astype('float32')
        image /= image.max()
        image = du.get25DImage(image, 1)
        image = np.floor(image * 255).astype('int')
        image = np.flipud(image)
        self.image = image
        self.numImagePerVolume = image.shape[0]
        self.index = int(image.shape[0]/2)
        self.label_3.setText('%d of %d' % (self.index, self.numImagePerVolume))
        self.label_5.setText('of %d' % (self.numImagePerVolume))

    def loadFile(self, filename):
        image_raw = nibabel.load(filename)
        image = du.resliceToAxial(image_raw.get_data())
        image = image.astype('float32')
        image /= image.max()
        image = du.get25DImage(image, 1)
        #image = np.floor(image * 255).astype('int')
        image = np.flipud(image)
        return image

    def setInputPath(self):
        self.download_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.lineEdit_8.setText(self.download_path)

        # List all desired files in this folder
        # Set comboBox
            #if not os.path.exists(download_path):
            #    QtWidgets.QMessageBox.critical(self, "Error", '\nFolder does not exist!')
        files = glob.glob(os.path.join(self.download_path, '*.nii.gz'))
        self.textBrowser.append('The input folder is:')
        self.textBrowser.append(self.download_path)
        self.textBrowser.append('loading...')
        self.textBrowser.append('-'*60)
        if len(files) > 0:
            for file in files:
                name = file.split('/')[-1]
                self.textBrowser.append(name)
                self.comboBox.addItem(name)
            self.textBrowser.append('-' * 60)
            defaultFile = files[0]
            self.current_file_name = defaultFile
            self.loadandUpdateFile(defaultFile)

            # Show images in Qgraphics
            self.showSlice()
        else:
            self.textBrowser.append('No NifTi files are found in this folder!')
            self.textBrowser.append('-' * 60)

    def setOutputPath(self):
        self.output_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.lineEdit_9.setText(self.output_path)

    def setSaveFileName(self):
        self.filename, filetype = QtWidgets.QFileDialog.getSaveFileName(self, "Save to file",filter="All Files (*);;HDF5 Files (*.hdf5)")
        self.lineEdit_9.setText(self.filename)



    def chooseFile(self):
        self.textBrowser.append('loading...')
        self.textBrowser.append(self.comboBox.currentText())

        # Load and show slices
        filename = os.path.join(self.download_path, self.comboBox.currentText())
        self.current_file_name = filename
        self.loadandUpdateFile(filename)

        # Show images in Qgraphics
        self.rotate_degree = 0
        self.showSlice()

        self.textBrowser.append('Done!')
    def rotate(self):
        self.rotate_degree = (self.rotate_degree + 1) % 4
        self.showSlice()

    def chooseSliceOrient(self):
        self.slice_orient = self.comboBox_4.currentText()
        if os.path.exists(self.current_file_name):
            self.loadandUpdateFile(self.current_file_name)
            self.rotate_degree = 0
            self.showSlice()

    def nextSlice(self):
        if self.numImagePerVolume > 0:
            self.index += 1
            self.index = self.index % self.numImagePerVolume
            self.showSlice()
            self.label_3.setText('%d of %d' % (self.index, self.numImagePerVolume))

    def previousSlice(self):
        if self.numImagePerVolume > 0:
            self.index -= 1
            self.index = self.index % self.numImagePerVolume
            self.showSlice()
            self.label_3.setText('%d of %d' % (self.index, self.numImagePerVolume))

    def firstSlice(self):
        if self.numImagePerVolume > 0:
            self.index = 0
            self.showSlice()
            self.label_3.setText('%d of %d' % (self.index, self.numImagePerVolume))

    def lastSlice(self):
        if self.numImagePerVolume > 0:
            self.index = self.numImagePerVolume - 1
            self.showSlice()
            self.label_3.setText('%d of %d' % (self.index, self.numImagePerVolume))

    def selectedSlice(self):
        if self.numImagePerVolume > 0:
            try:
                index = int(self.lineEdit.text())
                self.index = index % self.numImagePerVolume
                self.showSlice()
                self.label_3.setText('%d of %d' % (self.index, self.numImagePerVolume))
            except ValueError:
                self.textBrowser.append('Invalid input of selected slice!')

    def clickMethod(self):
        self.close()
        self.parent().show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = mainwindow()
    ui.show()
    #ui.setupMain(MainWindow)
    #ui.setupUi(MainWindow)
    #ui.setupMain(MainWindow)
    #MainWindow.show()
    #ui.show()
    sys.exit(app.exec_())
