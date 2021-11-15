#!/usr/bin/env pyhon3
# -*- coding: utf-8 -*-

import subprocess


class ListProgramForInstall(object):
    def __init__(self, os_ver="Unknown"):
        self.os_version = os_ver

    # Формирование списка доступных программ для установки в зависимости от версии ОС
    def listProgram(self):
        if self.os_version == "Ubuntu 21.04":
            list_program = ["pycharm-community", "pyqt5-dev-tools", "timeshift", "игры", "mc", "isomaster"]
        elif self.os_version == "AstraLinuxSE 1.6":
            list_program = ["timeshift"]
        #  self.stateProgram()
        return list_program

    # Статус программы: установлена или нет
    @staticmethod
    def stateProgram(list_program=None):
        dict_program = {}
        for name_prog in list_program:
            if name_prog == "игры":
                command = "dpkg --list | grep gnome-sudoku | awk '{print $2}' | grep -E '^gnome-sudoku$'>/dev/null; echo $?"
            else:
                command = "dpkg --list | grep " + name_prog + " | awk '{print $2}' | grep -E '^" + name_prog + "$'>/dev/null; echo $?"
            state_prog = action_program_return_code(command)
            dict_program[name_prog] = state_prog
            if not state_prog:
                print("Программа {} установлена".format(name_prog))
            elif state_prog:
                print("Программа {} не установлена".format(name_prog))
        return dict_program


# Запуск на выполнение команды с возвращаемым кодом выполнения
def action_program_return_code(command):
    code = 0    # По умолчанию считаем что программы установлена
    if command:
        proc = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if not out and not err:
            code = None
        elif int(out.decode("utf-8")):
            code = 1
    return code
