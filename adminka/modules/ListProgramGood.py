#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess
import threading
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QDialog


# Класс формирования списка программ
class Prog(object):
    def __init__(self, version=None):
        super().__init__()
        self.code = None
        self.dict_program = {}  # Словарь содержащий имя программы и ключ (признак установлена ли программа)
        # Версия ОС
        self.os_ver = version
        self.cortege_program = tuple()
        self.listProg()

    def listProg(self):
        if self.os_ver == "Ubuntu 21.04":
            self.cortege_program = ["pycharm-community", "pyqt5-dev-tools", "timeshift", "встроенные игры", "mc", "isomaster"]
        elif self.os_ver == '"AstraLinuxSE" 1.6':
            self.cortege_program = ["inxi"]
        if self.cortege_program:
            self.stateProg(self.cortege_program)

    def stateProg(self, cortege_program):
        for name_prog in cortege_program:
            command = "dpkg --list {}".format(name_prog)
            state_prog = action_program_return_code(command)
            self.dict_program[name_prog] = state_prog
            if not state_prog:
                print("Программа {} установлена".format(name_prog))
            elif state_prog:
                print("Программа {} не установлена".format(name_prog))


# class Debugger(QDialog):
#     def __init__(self):
#         super(Debugger, self).__init__()
#         self.debug_gui = Ui_Form()
#         self.debug_gui.setupUi(self)
#         self.show()


def installProg(action=None, name_program=None):
    command = None
    if action == "install":
        command = "sudo apt-get install {} -y".format(name_program)
    elif action == "remove":
        command = "sudo apt-get remove {} -y".format(name_program)

    t = threading.Thread(target=action_program_output_data, name=name_program,
                         args=(command,))
    t.start()
    t.join()


def action_program_return_code(command):
    code = 0    # По умолчанию считаем что программы установлена
    if command:
        proc = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if err:
            code = 1
    return code


def action_program_output_data(command):
    st = True
    if command:
        proc = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        while st:
            st = proc.stdout.readline()
            print(st.decode("utf-8"), end="")


if __name__ == "__main__":
    Prog(version="Ubuntu 21.04")
    # from Debug import Ui_Form
    # app = QtWidgets.QApplication(sys.argv)
    # d = Debugger()
    # sys.exit(app.exec_())
