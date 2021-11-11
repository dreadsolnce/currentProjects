#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess


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
            self.cortege_program = ["pycharm-community", "pyqt5-dev-tools", "timeshift", "встроенные игры", "mc"]
        elif self.os_ver == '"AstraLinuxSE" 1.6':
            self.cortege_program = ["inxi"]
        if self.cortege_program:
            self.stateProg(self.cortege_program)

    def stateProg(self, cortege_program):
        for name_prog in cortege_program:
            command = "dpkg --list {}".format(name_prog)
            state_prog = action_program(command)
            self.dict_program[name_prog] = state_prog
            if not state_prog:
                print("Программа {} установлена".format(name_prog))
            elif state_prog:
                print("Программа {} не установлена".format(name_prog))


def action_program(command):
    code = 0    # По умолчанию считаем что программы установлена
    if command:
        proc = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if err:
            code = 1
    return code


if __name__ == "__main__":
    Prog(version="Ubuntu 21.04")
