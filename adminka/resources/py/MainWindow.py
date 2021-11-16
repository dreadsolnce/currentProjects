# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(805, 339)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../resources/ico/logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setEnabled(True)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setHighlightSections(True)
        self.gridLayout.addWidget(self.treeWidget, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButtonInstall = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonInstall.setObjectName("pushButtonInstall")
        self.horizontalLayout_3.addWidget(self.pushButtonInstall)
        self.pushButtonRemove = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.horizontalLayout_3.addWidget(self.pushButtonRemove)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 24))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.program = QtWidgets.QMenu(self.menu)
        self.program.setObjectName("program")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.InstallRemove = QtWidgets.QAction(MainWindow)
        self.InstallRemove.setObjectName("InstallRemove")
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.removeProgram = QtWidgets.QAction(MainWindow)
        self.removeProgram.setObjectName("removeProgram")
        self.program.addAction(self.InstallRemove)
        self.menu.addAction(self.program.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.action_Exit)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Настройщик ОС Linux"))
        self.checkBox.setText(_translate("MainWindow", "выделить все"))
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "V"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Название"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "Состояние"))
        self.pushButtonInstall.setText(_translate("MainWindow", "Установить"))
        self.pushButtonRemove.setText(_translate("MainWindow", "Удалить"))
        self.menu.setTitle(_translate("MainWindow", "Локальная настройка"))
        self.program.setTitle(_translate("MainWindow", "Программы"))
        self.menu_3.setTitle(_translate("MainWindow", "Удалённая настройка"))
        self.menu_4.setTitle(_translate("MainWindow", "Сканер сети"))
        self.InstallRemove.setText(_translate("MainWindow", "Установка/Удаление"))
        self.action_Exit.setText(_translate("MainWindow", "Выход"))
        self.removeProgram.setText(_translate("MainWindow", "Удалить"))
