#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from modules import OsVersion, ListProgramForInstall, InstallProg
from resources import Ui_MainWindow

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
        self.l1 = None  # Экземпляр класса списка программ
        print("Инициализация основного окна программы")
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        # Задание параметров основного окна
        self.gui.checkBox.setVisible(False)
        self.gui.pushButtonInstall.setVisible(False)
        self.gui.pushButtonRemove.setVisible(False)
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
        self.gui.pushButtonInstall.setStatusTip("Установка отмеченных программ")
        self.gui.pushButtonRemove.setStatusTip("Удаление отмеченных программ")
        self.gui.action_Exit.setStatusTip("Выход из программы")
        # Центрирование окна
        self.winCenter()
        self.show()
        self.action()

    def action(self):
        self.gui.InstallRemove.triggered.connect(self.clkInstallRemove)
        self.gui.checkBox.clicked.connect(self.clkCheckbox)
        self.gui.pushButtonInstall.clicked.connect(lambda: self.clkPushButtonInstall(action="install"))
        self.gui.pushButtonRemove.clicked.connect(lambda: self.clkPushButtonInstall(action="remove"))
        self.gui.action_Exit.triggered.connect(lambda: sys.exit())

    def clkInstallRemove(self):
        print("Нажата кнопка Установка/Удаление")
        self.enableWidget()
        # Версия ОС
        self.os_version = OsVersion()
        print("Версия ОС: {}".format(self.os_version))
        # Список программ
        self.l1 = ListProgramForInstall(self.os_version)
        s = self.l1.listProgram()
        print("Доступный список программ для установки: {}".format(s))
        self.fillingProgramList(s)

    def fillingProgramList(self, list_program):
        self.gui.treeWidget.clear()
        list_state_program = self.l1.stateProgram(list_program)
        for name_prog in list_program:
            child = QtWidgets.QTreeWidgetItem(self.gui.treeWidget)
            child.setCheckState(0, Qt.Unchecked)
            child.setText(1, name_prog)
            if list_state_program[name_prog] == 0:
                child.setForeground(2, QtGui.QBrush(Qt.darkGreen))
                child.setText(2, "Установлена")
            elif list_state_program[name_prog] == 1:
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

    def clkPushButtonInstall(self, action=None):
        text = None
        if action == "install":
            print("Нажата кнопка установить")
            text = "Устанавливаем программу: {}"
        elif action == "remove":
            print("Нажата кнопка удалить")
            text = "Удаляем программу: {}"
        count_row = self.gui.treeWidget.topLevelItemCount()
        name_prog_list = []
        for count in range(count_row):
            current_element = self.gui.treeWidget.topLevelItem(count)
            if current_element.checkState(0):
                name_prog = current_element.text(1)
                name_prog_list.append(name_prog)
                print(text.format(name_prog))
        ins = InstallProg(self.os_version)
        ins.installProg(action, name_prog_list)
        self.clkInstallRemove()  # Обновляем список состояния программ

    # Показ виджетов
    def enableWidget(self):
        self.gui.treeWidget.setVisible(True)
        self.gui.checkBox.setVisible(True)
        self.gui.pushButtonInstall.setVisible(True)
        self.gui.pushButtonRemove.setVisible(True)

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
