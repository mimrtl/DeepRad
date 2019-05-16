# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from PyQt5 import QtCore, QtGui, QtWidgets

from GUI.dataAugmentation import Ui_Dialog

class dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(dialog, self).__init__(parent)
        self.setupUi(self)
        #self.setupMain()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        #self.pushButton_2.setStyleSheet("background-color: blue")
        self.pushButton.clicked.connect(self.getDataAugConfig)
        self.pushButton_2.clicked.connect(self.cancel)

        self.DataAugConfig = {}
        '''self.DataAugConfig['rotation_range'] = 10
        self.DataAugConfig['width_shift_range'] = 0.4
        self.DataAugConfig['zoom_range'] = 0.4
        self.DataAugConfig['height_shift_range'] = 0.4
        self.DataAugConfig['horizontal_flip'] = True
        self.DataAugConfig['vertical_flip'] = True
        self.DataAugConfig['shear_range'] = 5.0
        self.DataAugConfig['fill_mode'] = 'nearest'
        self.DataAugConfig['cval'] = 0.0
        self.DataAugConfig['featurewise_center'] = False
        self.DataAugConfig['featurewise_std_normalization'] = False
        self.DataAugConfig['samplewise_center'] = False
        self.DataAugConfig['samplewise_std_normalization'] = False
        self.DataAugConfig['ZCA_whitening'] = False
        self.DataAugConfig['ZCA_epsilon'] = 1e-6
        self.DataAugConfig['rescale'] = None
        self.DataAugConfig['brightness_range'] = None
        self.DataAugConfig['channel_shift_range'] = 0.0'''
        self.isDestroyed = False

    def getDataAugConfig(self):
        self.getConfig()
        result = self.check()
        if result['Valid_config']:
            print('Data Augmentation Done!')
            self.hide()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", '\nWrong Configuration!\n' + result['Message'])

    def cancel(self):
        self.isDestroyed = True
        self.close()
    def getConfig(self):
        self.DataAugConfig['rotation_range'] = self.lineEdit_2.text()
        self.DataAugConfig['width_shift_range'] = self.lineEdit_3.text()
        self.DataAugConfig['zoom_range'] = self.lineEdit_4.text()
        self.DataAugConfig['height_shift_range'] = self.lineEdit_5.text()
        self.DataAugConfig['horizontal_flip'] = self.checkBox_6.isChecked()
        self.DataAugConfig['vertical_flip'] = self.checkBox_7.isChecked()
        self.DataAugConfig['shear_range'] = self.lineEdit_6.text()
        self.DataAugConfig['fill_mode'] = self.comboBox.currentText()
        self.DataAugConfig['cval'] = self.lineEdit_7.text()
        self.DataAugConfig['featurewise_center'] = self.checkBox.isChecked()
        self.DataAugConfig['featurewise_std_normalization'] = self.checkBox_3.isChecked()
        self.DataAugConfig['samplewise_center'] = self.checkBox_2.isChecked()
        self.DataAugConfig['samplewise_std_normalization'] = self.checkBox_4.isChecked()
        self.DataAugConfig['ZCA_whitening'] = self.checkBox_5.isChecked()
        self.DataAugConfig['ZCA_epsilon'] = self.lineEdit.text()
        self.DataAugConfig['rescale'] = self.lineEdit_8.text()
        self.DataAugConfig['brightness_range'] = [self.lineEdit_9.text(), self.lineEdit_10.text()]
        self.DataAugConfig['channel_shift_range'] = self.lineEdit_11.text()

    def check(self):
        check_result = {}
        try:
            self.DataAugConfig['rotation_range'] = int(self.DataAugConfig['rotation_range'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Maximum rotation degree should be a integer'
            return check_result
        #if self.DataAugConfig['rotation_range'] < 0:
        #    check_result['Valid_config'] = False
        #    check_result['Message'] = 'Invalid maximum rotation degree (should be a non-negative integer)'
        #    return check_result

        try:
            self.DataAugConfig['width_shift_range'] = float(self.DataAugConfig['width_shift_range'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Maximum fraction of width shift should be a non-negative real number'
            return check_result
        if self.DataAugConfig['width_shift_range'] < 0 or self.DataAugConfig['width_shift_range'] > 1.0:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Invalid maximum fraction of width shift (should be a real number in [0.0, 1.0])'
            return check_result

        try:
            self.DataAugConfig['zoom_range'] = float(self.DataAugConfig['zoom_range'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Zoom range should be a non-negative real number'
            return check_result
        if self.DataAugConfig['zoom_range'] < 0:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Invalid zoom range (should be a non-negative real number)'
            return check_result

        try:
            self.DataAugConfig['height_shift_range'] = float(self.DataAugConfig['height_shift_range'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Maximum fraction of height shift should be a non-negative real number'
            return check_result
        if self.DataAugConfig['height_shift_range'] < 0 or self.DataAugConfig['height_shift_range'] > 1.0:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Invalid maximum fraction of height shift (should be a real number in [0.0, 1.0])'
            return check_result

        try:
            self.DataAugConfig['shear_range'] = float(self.DataAugConfig['shear_range'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Maximum shear degree should be a real number'
            return check_result
        #if self.DataAugConfig['shear_range'] < 0:
        #    check_result['Valid_config'] = False
        #    check_result['Message'] = 'Invalid maximum shear degree (should be a non-negative integer)'
        #    return check_result

        try:
            self.DataAugConfig['cval'] = float(self.DataAugConfig['cval'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Constant value should be a real number'
            return check_result

        try:
            self.DataAugConfig['ZCA_epsilon'] = float(self.DataAugConfig['ZCA_epsilon'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'ZCA epsilon should be a real number'
            return check_result

        if len(self.DataAugConfig['rescale']) == 0:
            self.DataAugConfig['rescale'] = None
        else:
            try:
                self.DataAugConfig['rescale'] = float(self.DataAugConfig['rescale'])
            except ValueError:
                check_result['Valid_config'] = False
                check_result['Message'] = 'Rescaling factor should be a real number'
                return check_result

        if len(self.DataAugConfig['brightness_range'][0]) == 0:
            if len(self.DataAugConfig['brightness_range'][1]) == 0:
                self.DataAugConfig['brightness_range'] = None
            else:
                check_result['Valid_config'] = False
                check_result['Message'] = 'Invalid brightness range configuration'
                return check_result
        else:
            if len(self.DataAugConfig['brightness_range'][1]) == 0:
                check_result['Valid_config'] = False
                check_result['Message'] = 'Invalid brightness range configuration'
                return check_result
            else:
                try:
                    self.DataAugConfig['brightness_range'][0] = float(self.DataAugConfig['brightness_range'][0])
                    self.DataAugConfig['brightness_range'][1] = float(self.DataAugConfig['brightness_range'][1])
                except ValueError:
                    check_result['Valid_config'] = False
                    check_result['Message'] = 'Brightness range should be real numbers'
                    return check_result
        try:
            self.DataAugConfig['channel_shift_range'] = float(self.DataAugConfig['channel_shift_range'])
        except ValueError:
            check_result['Valid_config'] = False
            check_result['Message'] = 'Channel shift range should be a real number'
            return check_result

        check_result['Valid_config'] = True
        check_result['Message'] = 'Valid configuration!'
        return  check_result
