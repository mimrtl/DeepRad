# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DeepRad_classification.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1116, 644)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.DeepRad = QtWidgets.QTabWidget(self.centralwidget)
        self.DeepRad.setGeometry(QtCore.QRect(40, 50, 1041, 521))
        self.DeepRad.setObjectName("DeepRad")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 481, 281))
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(450, 30, 21, 21))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(290, 120, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_8.setGeometry(QtCore.QRect(140, 30, 301, 21))
        self.lineEdit_8.setText("")
        self.lineEdit_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_10.setGeometry(QtCore.QRect(420, 120, 51, 21))
        self.lineEdit_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setGeometry(QtCore.QRect(20, 30, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(20, 90, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_11.setGeometry(QtCore.QRect(140, 90, 301, 21))
        self.lineEdit_11.setText("")
        self.lineEdit_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_5.setGeometry(QtCore.QRect(450, 90, 21, 21))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_16 = QtWidgets.QLabel(self.groupBox)
        self.label_16.setGeometry(QtCore.QRect(20, 50, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_5.setGeometry(QtCore.QRect(200, 50, 41, 31))
        self.checkBox_5.setChecked(True)
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_6 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_6.setGeometry(QtCore.QRect(260, 50, 61, 31))
        self.checkBox_6.setChecked(True)
        self.checkBox_6.setObjectName("checkBox_6")
        self.checkBox_7 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_7.setGeometry(QtCore.QRect(330, 50, 61, 31))
        self.checkBox_7.setChecked(True)
        self.checkBox_7.setObjectName("checkBox_7")
        self.checkBox_8 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_8.setGeometry(QtCore.QRect(400, 50, 51, 31))
        self.checkBox_8.setChecked(True)
        self.checkBox_8.setObjectName("checkBox_8")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(20, 120, 271, 20))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(60, 140, 171, 20))
        self.radioButton_2.setChecked(False)
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_17 = QtWidgets.QLabel(self.groupBox)
        self.label_17.setGeometry(QtCore.QRect(80, 160, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_12.setGeometry(QtCore.QRect(160, 160, 281, 21))
        self.lineEdit_12.setText("")
        self.lineEdit_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_6.setGeometry(QtCore.QRect(450, 160, 21, 21))
        self.pushButton_6.setObjectName("pushButton_6")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_3.setGeometry(QtCore.QRect(60, 180, 171, 20))
        self.radioButton_3.setObjectName("radioButton_3")
        self.label_18 = QtWidgets.QLabel(self.groupBox)
        self.label_18.setGeometry(QtCore.QRect(80, 200, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_13.setGeometry(QtCore.QRect(160, 200, 281, 21))
        self.lineEdit_13.setText("")
        self.lineEdit_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_7.setGeometry(QtCore.QRect(450, 200, 21, 21))
        self.pushButton_7.setObjectName("pushButton_7")
        self.lineEdit_18 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_18.setGeometry(QtCore.QRect(100, 250, 71, 21))
        self.lineEdit_18.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.label_27 = QtWidgets.QLabel(self.groupBox)
        self.label_27.setGeometry(QtCore.QRect(70, 250, 31, 21))
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.groupBox)
        self.label_28.setGeometry(QtCore.QRect(220, 250, 21, 21))
        self.label_28.setObjectName("label_28")
        self.lineEdit_19 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_19.setGeometry(QtCore.QRect(240, 250, 71, 21))
        self.lineEdit_19.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.label_29 = QtWidgets.QLabel(self.groupBox)
        self.label_29.setGeometry(QtCore.QRect(340, 250, 51, 21))
        self.label_29.setObjectName("label_29")
        self.lineEdit_20 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_20.setGeometry(QtCore.QRect(390, 250, 71, 21))
        self.lineEdit_20.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.checkBox_9 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_9.setGeometry(QtCore.QRect(20, 230, 131, 20))
        self.checkBox_9.setChecked(True)
        self.checkBox_9.setObjectName("checkBox_9")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 310, 481, 111))
        self.groupBox_2.setObjectName("groupBox_2")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(10, 20, 461, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(150, 50, 71, 21))
        self.lineEdit_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(20, 50, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(260, 50, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(390, 50, 71, 21))
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(20, 80, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_6.setGeometry(QtCore.QRect(150, 80, 71, 21))
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(260, 80, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_7.setGeometry(QtCore.QRect(390, 80, 71, 21))
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_3.setGeometry(QtCore.QRect(530, 20, 481, 71))
        self.groupBox_3.setObjectName("groupBox_3")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox.setGeometry(QtCore.QRect(20, 30, 81, 31))
        self.checkBox.setObjectName("checkBox")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 30, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_5.setGeometry(QtCore.QRect(530, 100, 481, 201))
        self.groupBox_5.setObjectName("groupBox_5")
        self.label_3 = QtWidgets.QLabel(self.groupBox_5)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_5)
        self.label_4.setGeometry(QtCore.QRect(20, 140, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_5)
        self.label_5.setGeometry(QtCore.QRect(20, 50, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_5)
        self.label_6.setGeometry(QtCore.QRect(20, 90, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit.setGeometry(QtCore.QRect(110, 90, 51, 21))
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 140, 51, 21))
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox_5)
        self.label_7.setGeometry(QtCore.QRect(20, 170, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_3.setGeometry(QtCore.QRect(110, 170, 51, 21))
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_8.setGeometry(QtCore.QRect(60, 20, 113, 32))
        self.pushButton_8.setObjectName("pushButton_8")
        self.label_19 = QtWidgets.QLabel(self.groupBox_5)
        self.label_19.setGeometry(QtCore.QRect(190, 25, 291, 21))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.pushButton_9 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_9.setGeometry(QtCore.QRect(90, 50, 113, 32))
        self.pushButton_9.setObjectName("pushButton_9")
        self.label_20 = QtWidgets.QLabel(self.groupBox_5)
        self.label_20.setGeometry(QtCore.QRect(220, 50, 261, 31))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.groupBox_5)
        self.label_21.setGeometry(QtCore.QRect(190, 90, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.lineEdit_14 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_14.setGeometry(QtCore.QRect(270, 90, 51, 21))
        self.lineEdit_14.setText("")
        self.lineEdit_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.label_22 = QtWidgets.QLabel(self.groupBox_5)
        self.label_22.setGeometry(QtCore.QRect(350, 90, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.lineEdit_15 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_15.setGeometry(QtCore.QRect(410, 90, 51, 21))
        self.lineEdit_15.setText("")
        self.lineEdit_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.label_23 = QtWidgets.QLabel(self.groupBox_5)
        self.label_23.setGeometry(QtCore.QRect(110, 140, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.groupBox_5)
        self.label_24.setGeometry(QtCore.QRect(310, 140, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.lineEdit_16 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_16.setGeometry(QtCore.QRect(410, 140, 51, 21))
        self.lineEdit_16.setText("")
        self.lineEdit_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.label_25 = QtWidgets.QLabel(self.groupBox_5)
        self.label_25.setGeometry(QtCore.QRect(340, 170, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.lineEdit_17 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_17.setGeometry(QtCore.QRect(410, 170, 51, 21))
        self.lineEdit_17.setText("")
        self.lineEdit_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(910, 450, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.groupBox_8 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_8.setGeometry(QtCore.QRect(530, 310, 481, 111))
        self.groupBox_8.setObjectName("groupBox_8")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_8)
        self.pushButton_4.setGeometry(QtCore.QRect(450, 30, 21, 21))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_8 = QtWidgets.QLabel(self.groupBox_8)
        self.label_8.setGeometry(QtCore.QRect(20, 30, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_8)
        self.checkBox_2.setGeometry(QtCore.QRect(170, 80, 81, 31))
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_8)
        self.checkBox_3.setGeometry(QtCore.QRect(280, 80, 101, 31))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_8)
        self.checkBox_4.setGeometry(QtCore.QRect(400, 80, 51, 31))
        self.checkBox_4.setObjectName("checkBox_4")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.groupBox_8)
        self.lineEdit_9.setGeometry(QtCore.QRect(100, 30, 341, 21))
        self.lineEdit_9.setText("")
        self.lineEdit_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.label_13 = QtWidgets.QLabel(self.groupBox_8)
        self.label_13.setGeometry(QtCore.QRect(40, 80, 101, 31))
        self.label_13.setObjectName("label_13")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_8)
        self.radioButton_5.setGeometry(QtCore.QRect(20, 60, 191, 20))
        self.radioButton_5.setChecked(True)
        self.radioButton_5.setObjectName("radioButton_5")
        self.DeepRad.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.DeepRad.addTab(self.tab_3, "")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1116, 22))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setToolTipsVisible(True)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionBack = QtWidgets.QAction(MainWindow)
        self.actionBack.setObjectName("actionBack")
        self.actionMain_Menu = QtWidgets.QAction(MainWindow)
        self.actionMain_Menu.setObjectName("actionMain_Menu")
        self.menuMenu.addAction(self.actionBack)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.DeepRad.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Step 1: Prepare Data"))
        self.pushButton.setText(_translate("MainWindow", "..."))
        self.label_2.setText(_translate("MainWindow", "Validation data ratio"))
        self.lineEdit_10.setText(_translate("MainWindow", "0.2"))
        self.label_14.setText(_translate("MainWindow", "Data folder path"))
        self.label_15.setText(_translate("MainWindow", "Label folder path"))
        self.pushButton_5.setText(_translate("MainWindow", "..."))
        self.label_16.setText(_translate("MainWindow", "Modalities used in training"))
        self.checkBox_5.setText(_translate("MainWindow", "t1"))
        self.checkBox_6.setText(_translate("MainWindow", "t1ce"))
        self.checkBox_7.setText(_translate("MainWindow", "flair"))
        self.checkBox_8.setText(_translate("MainWindow", "t2"))
        self.radioButton.setText(_translate("MainWindow", "Split into validation and training data"))
        self.radioButton_2.setText(_translate("MainWindow", "Folder of validation data"))
        self.label_17.setText(_translate("MainWindow", "Folder path"))
        self.pushButton_6.setText(_translate("MainWindow", "..."))
        self.radioButton_3.setText(_translate("MainWindow", "Index of validation data"))
        self.label_18.setText(_translate("MainWindow", "File path"))
        self.pushButton_7.setText(_translate("MainWindow", "..."))
        self.lineEdit_18.setText(_translate("MainWindow", "256"))
        self.label_27.setText(_translate("MainWindow", "Row"))
        self.label_28.setText(_translate("MainWindow", "Col"))
        self.lineEdit_19.setText(_translate("MainWindow", "256"))
        self.label_29.setText(_translate("MainWindow", "Channel"))
        self.lineEdit_20.setText(_translate("MainWindow", "256"))
        self.checkBox_9.setText(_translate("MainWindow", "Resize image to:"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Step 2: Choose Models"))
        self.comboBox.setItemText(0, _translate("MainWindow", "VGG16"))
        self.comboBox.setItemText(1, _translate("MainWindow", "VGG19"))
        self.comboBox.setItemText(2, _translate("MainWindow", "DenseNet121"))
        self.comboBox.setItemText(3, _translate("MainWindow", "DenseNet169"))
        self.comboBox.setItemText(4, _translate("MainWindow", "DenseNet201"))
        self.comboBox.setItemText(5, _translate("MainWindow", "ResNet50"))
        self.comboBox.setItemText(6, _translate("MainWindow", "InceptionV3"))
        self.comboBox.setItemText(7, _translate("MainWindow", "Xception"))
        self.comboBox.setItemText(8, _translate("MainWindow", "InceptionResNetV2"))
        self.lineEdit_4.setText(_translate("MainWindow", "256"))
        self.label_9.setText(_translate("MainWindow", "Image row size"))
        self.label_10.setText(_translate("MainWindow", "Image column size"))
        self.lineEdit_5.setText(_translate("MainWindow", "256"))
        self.label_11.setText(_translate("MainWindow", "Image channel size"))
        self.lineEdit_6.setText(_translate("MainWindow", "3"))
        self.label_12.setText(_translate("MainWindow", "Number of labels"))
        self.lineEdit_7.setText(_translate("MainWindow", "2"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Step 3: Data Augmentation"))
        self.checkBox.setText(_translate("MainWindow", "Enable"))
        self.pushButton_2.setText(_translate("MainWindow", "Options..."))
        self.groupBox_5.setTitle(_translate("MainWindow", "Step 4: Training Configuration"))
        self.label_3.setText(_translate("MainWindow", "Loss"))
        self.label_4.setText(_translate("MainWindow", "Batch size:"))
        self.label_5.setText(_translate("MainWindow", "Optimizer"))
        self.label_6.setText(_translate("MainWindow", "Learning rate"))
        self.lineEdit.setText(_translate("MainWindow", "1e-4"))
        self.lineEdit_2.setText(_translate("MainWindow", "32"))
        self.label_7.setText(_translate("MainWindow", "Epoch"))
        self.lineEdit_3.setText(_translate("MainWindow", "10"))
        self.pushButton_8.setText(_translate("MainWindow", "Options..."))
        self.label_19.setText(_translate("MainWindow", "Cross Entropy"))
        self.pushButton_9.setText(_translate("MainWindow", "Options..."))
        self.label_20.setText(_translate("MainWindow", "Adam"))
        self.label_21.setText(_translate("MainWindow", "Drop factor"))
        self.label_22.setText(_translate("MainWindow", "Patience"))
        self.label_23.setText(_translate("MainWindow", "Training data"))
        self.label_24.setText(_translate("MainWindow", "Validation data"))
        self.label_25.setText(_translate("MainWindow", "Early stop"))
        self.pushButton_3.setText(_translate("MainWindow", "Start"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Step 5: Output configuration"))
        self.pushButton_4.setText(_translate("MainWindow", "..."))
        self.label_8.setText(_translate("MainWindow", "Folder path"))
        self.checkBox_2.setText(_translate("MainWindow", "weights"))
        self.checkBox_3.setText(_translate("MainWindow", "Tensorboard"))
        self.checkBox_4.setText(_translate("MainWindow", "logs"))
        self.label_13.setText(_translate("MainWindow", "Training output:"))
        self.radioButton_5.setText(_translate("MainWindow", "Configuration file only"))
        self.DeepRad.setTabText(self.DeepRad.indexOf(self.tab_2), _translate("MainWindow", "Train Model"))
        self.DeepRad.setTabText(self.DeepRad.indexOf(self.tab_3), _translate("MainWindow", "Evaluate Model"))
        self.label.setText(_translate("MainWindow", "Home: Welcome to DeepRad!"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionBack.setText(_translate("MainWindow", "Back"))
        self.actionMain_Menu.setText(_translate("MainWindow", "Main Menu"))

