# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGridLayout
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append("..")
import numpy as np

from GUI.DeepRad_classification import Ui_MainWindow
from funcs.configuration import Config_Classification
from include.thread import ClassificationTrain
from funcs import dataAug, LossConfig, OptimizerConfig
from funcs.visualization import VisualizationMainWindow, VisualizationDialog

MAINWINDOW = 0
QOBJECT = 1
QTHREAD = 2


class NewStdout(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        do_nothing = 1



def listOfStr2Str(str_list, seperator = ""):
    string = ""
    for item in str_list:
        string += seperator
        string += item
    return string

class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent):
        super(mainwindow, self).__init__(parent)
        self.setupUi(self)
        self.setupMain()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        #  Makes Qt delete this widget when the widget has accepted the close event
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def setupMain(self):
        self.loss_list = ["cross entropy", "MSE", "KL divergence"]
        self.DataAugConfig = dataAug.dialog(self)
        self.LossConfig = LossConfig.LossDialog(self)
        self.OptimizerConfig = OptimizerConfig.OptimizerDialog(self)
        self.config_classification = Config_Classification()
        self.thread_dict = {}  # {'thread_index': [MainWindow, QObject, QThread]}
        self.new_thread_index = None
        self.MAX_INT = sys.maxsize

        self.train_status = {}

        self.old_stdout = sys.stdout

        self.menubar.setNativeMenuBar(False)
        self.actionBack.setShortcut("Ctrl+B")
        self.actionBack.setStatusTip("Back to the main window")
        self.actionBack.triggered.connect(self.clickMethod)

        self.pushButton_2.clicked.connect(self.openDataAugDialog)
        self.pushButton_3.clicked.connect(self.clickStart)
        self.pushButton_8.clicked.connect(self.openLossDialog)
        self.pushButton_9.clicked.connect(self.openOptimizerDialog)

        #self.pushButton.clicked.connect(self.setDataFolderPath)
        self.pushButton.clicked.connect(self.setDataFilePath)
        self.pushButton_6.clicked.connect(self.setValidationFolderPath)
        self.pushButton_7.clicked.connect(self.setValidationIndexFolderPath)
        self.pushButton_4.clicked.connect(self.setOutputFolderPath)

        self.lineEdit_18.textChanged.connect(self.showImageRow)
        self.lineEdit_19.textChanged.connect(self.showImageCol)
        self.lineEdit_4.setDisabled(True)
        self.lineEdit_5.setDisabled(True)

    def showImageRow(self):
        self.lineEdit_4.setText(self.lineEdit_18.text())

    def showImageCol(self):
        self.lineEdit_5.setText(self.lineEdit_19.text())

    def setDataFilePath(self):
        data_path, file_type= QtWidgets.QFileDialog.getOpenFileName(self)
        if isinstance(data_path, str):
            self.lineEdit_8.setText(data_path)

    def setDataFolderPath(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.lineEdit_8.setText(download_path)

    def setValidationFolderPath(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.lineEdit_12.setText(download_path)

    def setValidationIndexFolderPath(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.lineEdit_13.setText(download_path)

    def setOutputFolderPath(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.lineEdit_9.setText(download_path)

    def clickStart(self):
        self.changeStdout()
        self.getCurrentConfigFromGUI()
        self.startTask()

    def startTask(self):
        if self.isValidConfig():
            self.transformConfig()
            self.runSegmentationCallbackFunc()
        else:
            self.showErrorConfigDetail()

    def isValidConfig(self):
        self.config_classification.configCheck()
        return self.config_classification.is_valid_config

    def transformConfig(self):
        self.config_classification.configTransform()

    def runSegmentationCallbackFunc(self):
        self.segmentationTrain()
        '''try:
            self.segmentationTrain()
        except:
            self.showErrorDetailInTraining()'''

    def segmentationTrain(self):
        self.generateThreadIndex()
        self.createNewItemInThreadDict()
        self.addVisualizationWindowToNewItem()
        self.addObjectAndThreadToNewItem()
        self.initializeNewItem()
        self.runNewThreadForTraining()

    def generateThreadIndex(self):
        index = np.random.randint(self.MAX_INT)
        while str(index) in self.thread_dict.keys():
            index = np.random.randint(self.MAX_INT)
        self.new_thread_index = index

    def createNewItemInThreadDict(self):
        self.thread_dict[str(self.new_thread_index)] = list()

    def addVisualizationWindowToNewItem(self):
        self.thread_dict[str(self.new_thread_index)].append(
            VisualizationMainWindow(self.new_thread_index, self))

    def addObjectAndThreadToNewItem(self):
        self.thread_dict[str(self.new_thread_index)].append(
            ClassificationTrain(self.new_thread_index, self.config_classification)
        )
        self.thread_dict[str(self.new_thread_index)].append(
            QtCore.QThread()
        )

    def initializeNewItem(self):
        new_thread_name = str(self.new_thread_index)
        train_object = self.thread_dict[new_thread_name][QOBJECT]
        train_thread = self.thread_dict[new_thread_name][QTHREAD]
        train_object.moveToThread(train_thread)
        train_object.finished.connect(self.terminateTrainingThread)
        train_thread.started.connect(train_object.startTraining)

    def runNewThreadForTraining(self):
        self.initializeTrainStatus()
        self.openNewVisualizationMainWindow()
        self.runNewThread()

    def terminateTrainingThread(self, thread_index):
        # Only close the window, the training process will continue until it stops
        self.thread_dict[thread_index][QTHREAD].setTerminationEnabled(True)
        self.thread_dict[thread_index][QTHREAD].terminate()
        self.recoverStdout()
        self.thread_dict[thread_index][MAINWINDOW].pushButton_2.setEnabled(True)

    def removeItemFromThreadDict(self, thread_index):
        self.thread_dict.pop(thread_index)

    ''''# Not perform as expected!
    def terminateAll(self, thread_index):
        self.thread_dict[thread_index][QTHREAD].sleep(10)
        self.thread_dict[thread_index][QTHREAD].terminate()
        self.recoverStdout()'''

    def terminateSystem(self, thread_index):
        sys.exit()

    def changeStdout(self):
        sys.stdout = NewStdout(textWritten = self.showResultInRealTime)

    def recoverStdout(self):
        sys.stdout = self.old_stdout

    def runNewThread(self):
        self.runThread(str(self.new_thread_index))

    def runThread(self, thread_name):
        self.thread_dict[thread_name][QTHREAD].start()

    def openNewVisualizationMainWindow(self):
        self.openVisualizationMainWindow(str(self.new_thread_index))

    def openVisualizationMainWindow(self, thread_index):
        self.thread_dict[thread_index][MAINWINDOW].show()

    def initializeTrainStatus(self):
        self.train_status['current_epoch'] = 'None'
        self.train_status['total_epoch'] = 'None'
        self.train_status['current_batch'] = 'None'
        self.train_status['total_batch'] = 'None'
        self.train_status['ETA'] = 'None'
        self.train_status['speed'] = 'None'
        self.train_status['loss'] = 'None'
        self.train_status['acc'] = 'None'
        self.train_status['val_loss'] = 'None'
        self.train_status['val_acc'] = 'None'
        self.train_status['progress_batch'] = 0.0
        self.train_status['progress_epoch'] = 0.0
        self.train_status['x_axis'] = list()
        self.train_status['y_axis'] = list()
        self.train_status['x_label'] = 'Epoch'
        self.train_status['y_label'] = 'Train Loss'
        self.train_status['status_info'] = 'Ready'

    def showResultInRealTime(self, message):
        # slot function
        self.processMessageFromTrainingThread(message)
        self.showResultInPlot()
        self.showTrainingProgress()

    def processMessageFromTrainingThread(self, message):
        self.getCurrentAndTotalEpoch(message)
        self.getCurrentAndTotalBatch(message)
        self.getEstimatedTime(message)
        self.getTrainingSpeed(message)
        self.getLoss(message)
        self.getAccuracy(message)
        self.getValidationLoss(message)
        self.getValidationAccuracy(message)
        self.getProgressValues(message)
        self.getXYValuesForPlot(message)
        self.getStatusInfo(message)

    def isContainStatusInfo(self, string):
        if "Status" in string:
            return True
        else:
            return False

    def testGetStatusInfo(self, message):
        self.train_status['status_info'] = message

    def getStatusInfo(self, message):
        if self.isContainStatusInfo(message):
            self.train_status['status_info'] = message.split(': ')[1]

    def showResultInPlot(self):
        if self.isValidXYValues():
            self.plotTrainLoss()

    def plotTrainLoss(self):
        x_value = self.train_status['x_axis']
        y_value = self.train_status['y_axis']
        self.thread_dict[str(self.new_thread_index)][MAINWINDOW].plotFigure(x_value, y_value)

    def isValidXYValues(self):
        if (len(self.train_status['x_axis']) == len(self.train_status['y_axis'])) and\
                (len(self.train_status['x_axis']) > 0):
            return True
        else:
            return False

    def getXYValuesForPlot(self, string):
        if self.isContainEpoch(string):
            self.getXValue()
        if self.isCurrentEpochEnds(string):
            self.getYValue()

    def isCurrentEpochEnds(self, string):
        return self.isTrainingSpeed(string)

    def getXValue(self):
        self.train_status['x_axis'].append(int(self.train_status['current_epoch']))

    def getYValue(self):
        self.train_status['y_axis'].append(float(self.train_status['loss']))

    def showTrainingProgress(self):
        self.thread_dict[str(self.new_thread_index)][MAINWINDOW].label_2.setText(
            self.train_status['current_epoch']+'/'+self.train_status['total_epoch'])
        self.thread_dict[str(self.new_thread_index)][MAINWINDOW].label_5.setText(self.train_status['ETA'])
        self.thread_dict[str(self.new_thread_index)][MAINWINDOW].label_7.setText(self.train_status['speed'])
        self.thread_dict[str(self.new_thread_index)][MAINWINDOW].label_9.setText(self.train_status['loss'])
        self.thread_dict[str(self.new_thread_index)][MAINWINDOW].label_11.setText(self.train_status['acc'])
        self.thread_dict[str(self.new_thread_index)][MAINWINDOW].label_13.setText(self.train_status['val_loss'])
        self.thread_dict[str(self.new_thread_index)][MAINWINDOW].label_15.setText(self.train_status['val_acc'])
        self.thread_dict[str(self.new_thread_index)][MAINWINDOW].progressBar.setValue(self.train_status['progress_batch'])
        self.thread_dict[str(self.new_thread_index)][MAINWINDOW].progressBar_2.setValue(self.train_status['progress_epoch'])
        self.thread_dict[str(self.new_thread_index)][MAINWINDOW].label_18.setText(self.train_status['status_info'])
        #self.thread_dict[str(self.new_thread_index)][MAINWINDOW].label_18.setText(self.train_status['status_info'])
        QtWidgets.QApplication.processEvents()

    def showErrorDetailInTraining(self):
        self.popoutErrorMessageBox("Failed to start training\n Please check the configuration!")

    def showErrorConfigDetail(self):
        self.popoutErrorMessageBox(self.getAllMessageString())

    def getAllMessageString(self):
        return listOfStr2Str(self.config_classification.check_result, seperator='\n')

    def getCurrentConfigFromGUI(self):
        self.getCurrentPrepareDataConfigFromGUI()
        self.getCurrentChooseModelConfigFromGUI()
        self.getCurrentDataAugConfigFromGUI()
        self.getCurrentTrainingConfigFromGUI()
        self.getCurrentOutputConfigFromGUI()

    def getCurrentPrepareDataConfigFromGUI(self):
        self.config_classification.config['data_file_path'] = self.lineEdit_8.text()
        #self.config_classification.config['modality_t1'] = self.checkBox_5.isChecked()
        #self.config_classification.config['modality_t1ce'] = self.checkBox_6.isChecked()
        #self.config_classification.config['modality_flair'] = self.checkBox_7.isChecked()
        #self.config_classification.config['modality_t2'] = self.checkBox_8.isChecked()
        #self.config_classification.config['label_folder'] = self.lineEdit_11.text()
        self.config_classification.config['is_split'] = self.radioButton.isChecked()
        self.config_classification.config['is_validation_folder'] = self.radioButton_2.isChecked()
        self.config_classification.config['is_validation_index'] = self.radioButton_3.isChecked()
        self.config_classification.config['validation_ratio'] = self.lineEdit_10.text()
        self.config_classification.config['validation_folder'] = self.lineEdit_12.text()
        self.config_classification.config['validation_index'] = self.lineEdit_13.text()
        self.config_classification.config['is_resize'] = self.checkBox_9.isChecked()
        self.config_classification.config['resize_row'] = self.lineEdit_18.text()
        self.config_classification.config['resize_col'] = self.lineEdit_19.text()
        self.config_classification.config['resize_channel'] = self.lineEdit_20.text()

    def getCurrentChooseModelConfigFromGUI(self):
        self.config_classification.config['model'] = self.comboBox.currentText()
        self.config_classification.config['input_size_row'] = self.lineEdit_4.text()
        self.config_classification.config['input_size_col'] = self.lineEdit_5.text()
        self.config_classification.config['input_size_channel'] = self.lineEdit_6.text()
        self.config_classification.config['num_class'] = self.lineEdit_7.text()

    def getCurrentDataAugConfigFromGUI(self):
        self.config_classification.config['isDataAug'] = self.checkBox.isChecked()
        self.config_classification.config['data_aug_config'] = self.DataAugConfig.DataAugConfig

    def getCurrentTrainingConfigFromGUI(self):
        self.config_classification.config['learning_rate'] = self.lineEdit.text()
        self.config_classification.config['drop_factor'] = self.lineEdit_14.text()
        self.config_classification.config['patience'] = self.lineEdit_15.text()
        self.config_classification.config['batch_size_training'] = self.lineEdit_2.text()
        self.config_classification.config['batch_size_validation'] = self.lineEdit_16.text()
        self.config_classification.config['epoch'] = self.lineEdit_3.text()
        self.config_classification.config['early_stop'] = self.lineEdit_17.text()

        self.config_classification.config['LossConfig'] = self.LossConfig.LossConfig
        self.config_classification.config['OptimizerConfig'] = self.OptimizerConfig.OptimizerConfig

    def getCurrentOutputConfigFromGUI(self):
        self.config_classification.config['output_folder'] = self.lineEdit_9.text()
        self.config_classification.config['is_file_only'] = self.radioButton_5.isChecked()
        self.config_classification.config['isWeight'] = self.checkBox_2.isChecked()
        self.config_classification.config['isTensorboard'] = self.checkBox_3.isChecked()
        self.config_classification.config['isLogs'] = self.checkBox_4.isChecked()

    def clickMethod(self):
        self.close()
        self.parent().show()

    def openDataAugDialog(self):
        if self.checkBox.isChecked():
            self.getDataAugConfigFromDialog()
        else:
            self.popoutErrorMessageBox('\nWrong Configuration!\nPlease enable data augmentation first')

    def openLossDialog(self):
        self.updateLossConfig()

    def updateLossConfig(self):
        if self.LossConfig.isDestroyed:
            self.LossConfig = LossConfig.LossDialog(self)
        self.LossConfig.show()

    def updateLossLabelValue(self):
        self.label_19.setText(self.LossConfig.LossConfig["loss"])

    def updateOptimizerLabelValue(self):
        self.label_20.setText(self.OptimizerConfig.OptimizerConfig["optimizer"])

    def openOptimizerDialog(self):
        self.updateOptimizerConfig()

    def updateOptimizerConfig(self):
        if self.OptimizerConfig.isDestroyed:
            self.OptimizerConfig = OptimizerConfig.OptimizerDialog(self)
        self.OptimizerConfig.show()

    def popoutErrorMessageBox(self, message):
        QtWidgets.QMessageBox.critical(self, "Error", message)

    def getDataAugConfigFromDialog(self):
        if self.DataAugConfig.isDestroyed:
            self.DataAugConfig = dataAug.dialog(self)
        self.DataAugConfig.show()

    def isContainEpoch(self, string):
        if 'Epoch' in string:
            return True
        else:
            return False

    def isContainLoss(self, string):
        if ('loss' in string) and not ('val_loss' in string):
            return True
        else:
            return False

    def isContainAccuracy(self, string):
        if ('acc' in string) and not ('val_acc' in string):
            return True
        else:
            return False

    def isContainValidationLoss(self, string):
        if 'val_loss' in string:
            return True
        else:
            return False

    def isContainValidationAccuracy(self, string):
        if 'val_acc' in string:
            return True
        else:
            return False

    def isContainEstimatedTime(self, string):
        if 'ETA' in string:
            return True
        else:
            return False

    def isTrainingSpeed(self, string):
        if 'step' in string:
            return True
        else:
            return False
    def isContainBatch(self, string):
        if ('[' in string) and (']' in string) and ('/' in string):
            return True
        else:
            return False

    def getCurrentAndTotalBatch(self, string):
        # ' 128/6000 [.................................]'
        if self.isContainBatch(string):
            current_and_total_batch = string.split(' [')[0]
            self.train_status['current_batch'] = current_and_total_batch.split('/')[0]
            self.train_status['total_batch'] = current_and_total_batch.split('/')[1]

    def getCurrentAndTotalEpoch(self, string):
        # 'Epoch 1/10'
        if self.isContainEpoch(string):
            current_and_total_epoch = string.split(' ')[1]
            self.train_status['current_epoch'] = current_and_total_epoch.split('/')[0]
            self.train_status['total_epoch'] = current_and_total_epoch.split('/')[1]

    def getEstimatedTime(self, string):
        # ' - ETA: 44s - loss: 2.3194 - acc: 0.0703'
        # ' - ETA: 21:51 - loss: 2.3194 - acc: 0.0703'
        if self.isContainEstimatedTime(string):
            time_value = string.split('ETA: ')[1].split(' - loss')[0]
            self.train_status['ETA'] = time_value

    def getLoss(self, string):
        # ' - ETA: 44s - loss: 2.3194 - acc: 0.0703'
        if self.isContainLoss(string):
            loss = string.split('loss: ')[1].split(' - ')[0].replace("\n", "")
            self.train_status['loss'] = loss

    def getAccuracy(self, string):
        # ' - ETA: 44s - loss: 2.3194 - acc: 0.0703'
        if self.isContainAccuracy(string):
            acc = string.split('acc: ')[1]
            self.train_status['acc'] = acc

    def getValidationLoss(self, string):
        # ' - 571s 95ms/step - loss: 1.0055 - acc: 0.6755 - val_loss: 0.3645 - val_acc: 0.8860\n'
        if self.isContainValidationLoss(string):
            val_loss = string.split('val_loss: ')[1].split(' - val_acc')[0]
            self.train_status['val_loss'] = val_loss

    def getValidationAccuracy(self, string):
        # ' - 571s 95ms/step - loss: 1.0055 - acc: 0.6755 - val_loss: 0.3645 - val_acc: 0.8860\n'
        if self.isContainValidationAccuracy(string):
            val_acc = string.split('val_acc: ')[1].split('\n')[0]
            self.train_status['val_acc'] = val_acc

    def getTrainingSpeed(self, string):
        # ' - 571s 95ms/step - loss: 1.0055 - acc: 0.6755 - val_loss: 0.3645 - val_acc: 0.8860\n'
        if self.isTrainingSpeed(string):
            speed = string.split(' - ')[1].split(' ')[1]
            self.train_status['speed'] = speed

    def getProgressValues(self, string):
        if self.isContainBatch(string):
            self.getBatchProgress()
            self.getEpochProgress()

    def getBatchProgress(self):
        current_batch = float(self.train_status['current_batch'])
        total_batch = float(self.train_status['total_batch'])
        self.train_status['progress_batch'] = min(1.0, current_batch/total_batch)*100

    def getEpochProgress(self):
        current_batch = float(self.train_status['current_batch'])
        total_batch = float(self.train_status['total_batch'])
        current_epoch = float(self.train_status['current_epoch'])
        total_epoch = float(self.train_status['total_epoch'])
        self.train_status['progress_epoch'] = min(1.0, ((current_epoch - 1)*total_batch + current_batch)/(total_batch*total_epoch))*100

    def loadExistingConfigFromFile(self):
        print('In construction')

if __name__ == '__main__':
    index = '1'
    x = SegmentationTrain()
    y = QtCore.QThread()
    thread = {index:[x,y]}
    print(thread)

