# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adminka/qt/SshDesktopVnc.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SshDesktopVnc(object):
    def setupUi(self, SshDesktopVnc):
        SshDesktopVnc.setObjectName("SshDesktopVnc")
        SshDesktopVnc.resize(505, 275)
        self.gridLayout = QtWidgets.QGridLayout(SshDesktopVnc)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox = QtWidgets.QCheckBox(SshDesktopVnc)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(SshDesktopVnc)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 4)
        self.label_4 = QtWidgets.QLabel(SshDesktopVnc)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 4)
        self.frame = QtWidgets.QFrame(SshDesktopVnc)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 4)
        self.checkBox_2 = QtWidgets.QCheckBox(SshDesktopVnc)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 3, 1, 1, 1)
        self.line = QtWidgets.QFrame(SshDesktopVnc)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 0, 1, 4)
        self.pushButton = QtWidgets.QPushButton(SshDesktopVnc)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 5, 3, 1, 1)

        self.retranslateUi(SshDesktopVnc)
        QtCore.QMetaObject.connectSlotsByName(SshDesktopVnc)

    def retranslateUi(self, SshDesktopVnc):
        _translate = QtCore.QCoreApplication.translate
        SshDesktopVnc.setWindowTitle(_translate("SshDesktopVnc", "Ярлыки запуска VNCViewer"))
        self.checkBox.setText(_translate("SshDesktopVnc", "VNCAddrBook"))
        self.label_3.setText(_translate("SshDesktopVnc", "который установлен на удаленном компьютере"))
        self.label_4.setText(_translate("SshDesktopVnc", "Создание ярлыка запуска vnc viewer, "))
        self.label.setText(_translate("SshDesktopVnc", "ip адрес:"))
        self.lineEdit.setInputMask(_translate("SshDesktopVnc", "000.000.000.000;_"))
        self.lineEdit.setText(_translate("SshDesktopVnc", "..."))
        self.label_5.setText(_translate("SshDesktopVnc", "Параметры подключения к удаленному компьютеру"))
        self.label_2.setText(_translate("SshDesktopVnc", "имя пользователя:"))
        self.checkBox_2.setText(_translate("SshDesktopVnc", "VNCViewer"))
        self.pushButton.setText(_translate("SshDesktopVnc", "OK"))
