#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from .Programs import Programs


class ProgramsModule(object):
    def __init__(self, os_ver=None, os_debian=None, os_astra=None, name_ui=None, obj_win=None):
        super().__init__()
        self.p = None   # Объект Programs
        self.os_ver = os_ver
        self.os_debian = os_debian
        self.os_astra = os_astra
        self.obj_win = obj_win
        self.name_ui = name_ui
        self.listPrograms()

    # Функции для работы с гаджетами

    # В зависимости от версии ОС формируем список программ
    def listPrograms(self):
        self.p = Programs(self.os_ver, self.os_debian, self.os_astra)  # Инициализируем класс программы
        lst_prog = self.p.list_program  # Список программ
        if not lst_prog:
            QMessageBox.critical(self.obj_win, "Ошибка!", "Не поддерживаемая версия ОС", QMessageBox.Ok)
        else:
            self.fillingProgramList(lst_prog)

    # Формируем словарь с именем программы и ключом (состояние программы)
    def fillingProgramList(self, lst_program):
        self.name_ui.treeWidget_program.clear()
        state_program = self.p.stateProg()  # Словарь: программа:статус программы (0 - не установлена, 1 - установлена)
        self.fillingGadget(state_program, lst_program)

    # Заполняем гаджет со списком программ
    def fillingGadget(self, state_program, lst_program):
        for name in lst_program:
            child = QtWidgets.QTreeWidgetItem(self.name_ui.treeWidget_program)
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
        if self.name_ui.checkBox_all.isChecked():
            self.allCheck(state=True)
            print("Выделяем все чек боксы")
        elif not self.name_ui.checkBox_all.isChecked():
            self.allCheck(state=False)
            print("Снимаем выделение со всех чек боксов")

    def allCheck(self, state):
        count_row = self.name_ui.treeWidget_program.topLevelItemCount()
        print("Количество строк в таблице: {}".format(count_row))
        for count in range(count_row):
            current_element = self.name_ui.treeWidget_program.topLevelItem(count)
            if state:
                current_element.setCheckState(0, Qt.Checked)
            elif not state:
                current_element.setCheckState(0, Qt.Unchecked)

    def clkPushButtonProgram(self, action=None):
        if action == "install":
            print("Нажата кнопка установить")
        elif action == "remove":
            print("Нажата кнопка удалить")
        count_row = self.name_ui.treeWidget_program.topLevelItemCount()
        name_prog_list = []
        for count in range(count_row):
            current_element = self.name_ui.treeWidget_program.topLevelItem(count)
            if current_element.checkState(0):
                name_prog = current_element.text(1)
                name_prog_list.append(name_prog)
        if name_prog_list:
            self.p.actionProg(os_ver=self.os_ver, action=action, lst_name_prog=name_prog_list)
            self.listPrograms()  # Обновляем список состояния программ
