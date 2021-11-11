#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import resources
from modules import OsVersion, Prog

from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDesktopWidget

"""
    Программа для настройки и администрирования 
    ОС семейства Linux (Ubuntu, AstraLinux)
"""

logo = os.path.join(sys.path[0] + "/resources/ico/", "logo.svg")
print("Иконка программы: {}".format(logo))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.sp = None  # Объект списка программ
        print("Инициализация основного окна программы")
        self.gui = resources.Ui_MainWindow()
        self.gui.setupUi(self)
        # Задание параметров основного окна
        self.gui.checkBox.setVisible(False)
        # Создание иконки программы
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        # Задание параметров treeWidget
        self.gui.treeWidget.setVisible(False)
        self.gui.treeWidget.setFocusPolicy(Qt.NoFocus)
        self.gui.treeWidget.setIndentation(2)
        self.gui.treeWidget.setColumnWidth(0, 60)
        self.gui.treeWidget.setColumnWidth(1, 250)
        # Изменение статубара
        self.gui.statusbar.showMessage("Основное окно программы")
        self.gui.centralwidget.setStatusTip("Основное окно программы")
        self.gui.InstallRemove.setStatusTip("Установка и удаление программ")
        self.gui.treeWidget.setStatusTip("Список программ для установки и удаления")
        self.gui.checkBox.setStatusTip("Выделить всё")
        self.gui.action_Exit.setStatusTip("Выход из программы")
        # Центрирование окна
        self.winCenter()
        self.show()
        self.action()

    def action(self):
        self.gui.InstallRemove.triggered.connect(self.clkInstallRemove)
        self.gui.checkBox.clicked.connect(self.clkCheckbox)
        self.gui.action_Exit.triggered.connect(lambda: sys.exit())

    def clkInstallRemove(self):
        print("Нажата кнопка Установка/Удаление")
        self.gui.treeWidget.setVisible(True)
        self.gui.checkBox.setVisible(True)
        # Список программ
        os_ver = OsVersion()
        print("Версия ОС: {}".format(os_ver))
        self.sp = Prog(os_ver)
        print("Доступный список программ для установки: {}".format(self.sp.cortege_program))
        self.fillingProgramList()

    def fillingProgramList(self):
        self.gui.treeWidget.clear()
        for name_prog in self.sp.cortege_program:
            child = QtWidgets.QTreeWidgetItem(self.gui.treeWidget)
            child.setCheckState(0, Qt.Unchecked)
            child.setText(1, name_prog)
            if self.sp.dict_program[name_prog] == 0:
                child.setForeground(2, QtGui.QBrush(Qt.darkGreen))
                child.setText(2, "Установлена")
            elif self.sp.dict_program[name_prog] == 1:
                child.setForeground(2, QtGui.QBrush(Qt.darkRed))
                child.setText(2, "Отсутствует")

    def clkCheckbox(self):
        print("Нажат чекбокс")
        if self.gui.checkBox.isChecked():
            self.allCheck(state=True)
            print("Выделяем все чекбоксы")
        elif not self.gui.checkBox.isChecked():
            self.allCheck(state=False)
            print("Снимаем выделение со всех чекбоксов")

    def allCheck(self, state):
        count_row = self.gui.treeWidget.topLevelItemCount()
        print("Колличество строк в таблице: {}".format(count_row))
        for count in range(count_row):
            current_element = self.gui.treeWidget.topLevelItem(count)
            if state:
                current_element.setCheckState(0, Qt.Checked)
            elif not state:
                current_element.setCheckState(0, Qt.Unchecked)

    # Центрирование окна относительно экрана
    def winCenter(self):
        qr = self.frameGeometry()
        qp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(qp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app1 = MainWindow()
    sys.exit(app.exec_())
