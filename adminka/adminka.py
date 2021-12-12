#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import resources

from PyQt5.Qt import Qt
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
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
        # Инициализация переменных
        self.p = None   # Объект класса программ
        self.os_ver = resources.OsVersion()  # Версия ОС
        # self.os_ver = '"AstraLinuxSE" 1.6'

        # Инициализация основного окна
        self.gui = resources.Ui_MainWindow()
        self.initializationMainWindow()

    def initializationMainWindow(self):
        print("Инициализация основного окна программы")
        self.gui.setupUi(self)
        # Задание параметров основного окна
        self.gui.checkBox.setVisible(False)
        self.gui.pushButtonInstall.setVisible(False)
        self.gui.pushButtonRemove.setVisible(False)
        # Создание иконки программы
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(logo))
        self.setWindowIcon(icon)
        # Задание параметров treeWidget
        self.gui.treeWidget.setVisible(False)
        self.gui.treeWidget.setFocusPolicy(Qt.NoFocus)
        self.gui.treeWidget.setIndentation(2)
        self.gui.treeWidget.setColumnWidth(0, 60)
        self.gui.treeWidget.setColumnWidth(1, 250)
        # Изменение статус бара
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

    # В зависимости от версии ОС формируем список программ
    def clkInstallRemove(self):
        print("Нажата кнопка Установка/Удаление")
        self.p = resources.Programs(self.os_ver)  # Инициализируем класс программы
        self.enableWidget()
        lst_prog = self.p.list_program   # Список программ
        if not lst_prog:
            QMessageBox.critical(self, "Ошибка!", "Не поддерживаемая версия ОС", QMessageBox.Ok)
        else:
            self.fillingProgramList(lst_prog)

    # Формируем словарь с именем программы и ключом (состояние программы)
    def fillingProgramList(self, lst_program):
        self.gui.treeWidget.clear()
        state_program = self.p.stateProg()  # Словарь: программа:статус программы (0 - не установлена, 1 - установлена)
        self.fillingGadget(state_program, lst_program)

    # Заполняем гаджет со списком программ
    def fillingGadget(self, state_program, lst_program):
        for name in lst_program:
            child = QtWidgets.QTreeWidgetItem(self.gui.treeWidget)
            child.setCheckState(0, Qt.Unchecked)
            child.setText(1, name)
            if state_program[name] == 0:
                child.setForeground(2, QtGui.QBrush(Qt.darkGreen))
                child.setText(2, "Установлена")
            elif state_program[name] != 0:
                child.setForeground(2, QtGui.QBrush(Qt.darkRed))
                child.setText(2, "Отсутствует")

    def clkCheckbox(self):
        print("Нажат чекбокс")
        if self.gui.checkBox.isChecked():
            self.allCheck(state=True)
            print("Выделяем все чек боксы")
        elif not self.gui.checkBox.isChecked():
            self.allCheck(state=False)
            print("Снимаем выделение со всех чек боксов")

    def allCheck(self, state):
        count_row = self.gui.treeWidget.topLevelItemCount()
        print("Количество строк в таблице: {}".format(count_row))
        for count in range(count_row):
            current_element = self.gui.treeWidget.topLevelItem(count)
            if state:
                current_element.setCheckState(0, Qt.Checked)
            elif not state:
                current_element.setCheckState(0, Qt.Unchecked)

    def clkPushButtonInstall(self, action=None):
        if action == "install":
            print("Нажата кнопка установить")
        elif action == "remove":
            print("Нажата кнопка удалить")
        count_row = self.gui.treeWidget.topLevelItemCount()
        name_prog_list = []
        for count in range(count_row):
            current_element = self.gui.treeWidget.topLevelItem(count)
            if current_element.checkState(0):
                name_prog = current_element.text(1)
                name_prog_list.append(name_prog)
        if name_prog_list:
            self.p.actionProg(os_ver=self.os_ver, action=action, lst_name_prog=name_prog_list)
            self.clkInstallRemove()  # # Обновляем список состояния программ

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
    a = resources.CheckSudo()
    a1 = MainWindow()
    sys.exit(app.exec_())
