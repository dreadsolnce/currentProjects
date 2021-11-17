#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
from time import sleep
from pathlib import Path

from PyQt5 import QtCore, QtWidgets, QtGui

if __name__ == "__main__":
    from Debug import Ui_Form
else:
    from .Debug import Ui_Form


class Programs(QtWidgets.QDialog):
    def __init__(self, os_ver=None):
        super().__init__()
        self.os_ver = os_ver  # Версия ОС
        self.list_program = None  # Список программ
        self.dg_gui = None  # Переменная для инициализации окна Debug
        self.listProgram()

    # Формирование списка программ
    def listProgram(self):
        if self.os_ver == "Ubuntu 21.04":
            self.list_program = ["pycharm-community", "pyqt5-dev-tools", "timeshift", "игры", "mc", "isomaster"]
        elif self.os_ver == '"AstraLinuxSE" 1.6':
            self.list_program = ["timeshift"]
        print("Доступный список программ для {}: {}".format(self.os_ver, self.list_program))

    # Определение состояния пакета в системе (0 - неустановлен, 1 - установлен)
    def stateProg(self):
        state_program = {}  # Словарь: имя программы:статус программы (0 - не установлен, 1 - установлен)
        # Комманда для snap пакета pycharm-community
        command_snap = "sudo snap list pycharm-community >/dev/null; echo $?"
        # Комманда для встроенных игр Ubuntu
        command_games = "sudo dpkg --list | grep gnome-sudoku | awk '{print $2}' | grep -E ^gnome-sudoku$ >/dev/null; echo $?"
        for name in self.list_program:
            if name == "игры":
                command = command_games
            elif name == "pycharm-community":
                command = command_snap
            else:
                command = "sudo dpkg --list | grep " + name + " | awk '{print $2}' | grep -E ^" + name + "$ >/dev/null; echo $?"

            out = runCommandReturnCode(command)
            state_program[name] = out
            if out:
                print("Программа {} : установлена".format(name))
            elif not out:
                print("Программа {} : не установлена".format(name))
        return state_program

    # Запуск установки либо удаления программы в зависимости от версии ОС
    def actionProg(self, os_ver=None, action=None, lst_name_prog=None):
        if os_ver == "Ubuntu 21.04":
            print("Запускаем функцию опредедения экшена для Ubuntu")
            self.__actionProgUbuntu(action, lst_name_prog)
        elif os_ver == '"AstraLinuxSE" 1.6':
            print("Запускаем функция определения экшена для AstraLinux 1.6")
            self.__actionProgAstra(action, lst_name_prog)

    # Установка либо удаление программ Ubuntu
    def __actionProgUbuntu(self, action=None, lst_name_prog=None):
        self.dg_gui = DebugWin()
        for name in lst_name_prog:
            command = None
            if action == "install":
                print("Устанавливаем программу {}".format(name))
                if name == "pycharm-community":
                    command_snap_ins = "sudo snap install {}"
                    command = command_snap_ins.format(name) + " --classic"
                elif name == "pyqt5-dev-tools":
                    name = "python3-pyqt5 qtcreator pyqt5-dev-tools qttools5-dev-tools"
                    command_2 = " ; sudo rm -rf /usr/share/applications/linguist-qt5.desktop"
                    command = "sudo apt-get install {} -y".format(name) + command_2
                else:
                    if name == "игры":
                        name = "aisleriot gnome-mahjongg gnome-mines gnome-sudoku"
                    command = "sudo apt-get install {} -y".format(name)
            elif action == "remove":
                print("Удаляем программу {}".format(name))
                if name == "pycharm-community":
                    command_snap_rem = "sudo snap remove {}"
                    command = command_snap_rem.format(name)
                else:
                    if name == "pyqt5-dev-tools":
                        name = "qtcreator pyqt5-dev-tools qttools5-dev-tools"
                    elif name == "игры":
                        name = "aisleriot gnome-mahjongg gnome-mines gnome-sudoku"
                    command = "sudo apt-get purge {} -y".format(name)

            process_th = RunProcessUbuntuPrograms(command)
            process_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
            process_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
            process_th.start()
            while process_th.isRunning():
                QtCore.QCoreApplication.processEvents()
                QtCore.QThread.msleep(150)
                self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
            process_th.quit()
        self.debugButtonAct()

    # Установка либо удаление программ AstraLinux 1.6
    def __actionProgAstra(self, action=None, lst_name_prog=None):
        self.dg_gui = DebugWin()
        for name in lst_name_prog:
            if name == "timeshift":
                process_th = SetupTimeshift(act=action)
                process_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                process_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                process_th.start()
                while process_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                process_th.quit()
        self.debugButtonAct()

    def debugButtonAct(self):
        self.dg_gui.dg.pushButton.setEnabled(True)
        self.dg_gui.dg.pushButton_2.setEnabled(True)
        self.dg_gui.dg.pushButton_2.clicked.connect(self.saveLogFile)
        self.dg_gui.dg.pushButton.clicked.connect(lambda: self.dg_gui.close())

    def saveLogFile(self):
        print("Сохранить лог в файл...")
        file_log = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', '{}'.format(str(Path.home())))[0]
        print(file_log)
        if file_log:
            with open(file_log, 'w') as f:
                text = self.dg_gui.dg.textDebug.toPlainText()
                f.write(text)
            f.close()


class RunProcessUbuntuPrograms(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, command=None):
        super().__init__()
        self.command = command

    def run(self):
        count = 0
        proc = subprocess.Popen(self.command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        st = proc.stdout.readline()
        while st:
            st = proc.stdout.readline()
            self.new_log.emit(st.decode('utf-8', 'ignore'))
            self.progress.emit(count)
            print(st.decode("utf-8"), end="")
            count += 1
            sleep(0.01)
        self.progress.emit(100)


# Класс установки
class SetupTimeshift(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, act=None):
        super().__init__()
        self.act = act
        self.files_path = None
        self.exit_code = 0
        self.count = 0

    def run(self):
        if __name__ == "__main__":
            self.files_path = sys.path[0].rpartition('resources')[0] + "files/"  # Каталог с дистрибутивом
        else:
            self.files_path = sys.path[0]

        self.unrar_arch()
        if not self.exit_code:
            print("Разархивировали! Продолжаем установку...")
            self.dpkg_ins()
            if not self.exit_code:
                self.new_log.emit("Установка выполнена успешно!")
            elif self.exit_code:
                self.new_log.emit("Ошибка при установке!")
        self.progress.emit(100)
        if os.path.isdir("package"):
            try:
                shutil.rmtree("package")
            except PermissionError as e:
                self.new_log.emit("Ошибка удаление временного каталога! {}".format(e))
        sleep(0.2)

    def unrar_arch(self):
        tar_gz_arch = self.files_path + "/files/pack_timeshift.tar.gz"
        print("Путь до архива с программой timeshift: {}".format(tar_gz_arch))
        if os.path.isfile(tar_gz_arch):
            print("Архив существует")
            process = subprocess.Popen("tar xvzf %s" % tar_gz_arch, shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            st = True
            while st:
                st = process.stdout.readline()
                self.new_log.emit(st.decode('utf-8', 'ignore'))
                self.progress.emit(self.count)
                print(st.decode("utf-8"), end="")
                self.count += 1
                sleep(0.01)
            process.communicate()
            self.exit_code = self.exit_code + process.returncode
            sleep(0.2)
        else:
            txt = "Ошибка! Не найден архив с пакетом timeshift"
            self.new_log.emit(txt)
            print(txt)
            self.exit_code = 1

    def dpkg_ins(self):
        deb_pack = sorted((os.listdir("package")))

        for pack in deb_pack:
            process = subprocess.Popen("sudo dpkg -i package/%s" % pack, shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            st = True
            while st:
                st = process.stdout.readline()
                self.count += 1
                self.new_log.emit(str(st.decode('utf-8', 'ignore')))
                self.progress.emit(self.count)
                print(st.decode("utf-8"), end="")
                sleep(0.01)
            process.communicate()
            self.exit_code = self.exit_code + process.returncode
            sleep(0.2)


# Запуск команды с выводом кода выполнения
def runCommandReturnCode(command):
    out = None
    if command:
        proc = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out = proc.communicate()[0].decode('utf-8')
    return int(out)


class DebugWin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.dg = Ui_Form()  # Инициализация окна Debug
        self.dg.setupUi(self)
        self.dg.pushButton.setEnabled(False)
        self.dg.pushButton_2.setEnabled(False)
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # u = Programs("Ubuntu 21.04")
    # u.stateProg()
    # u.actionProg(os_ver="Ubuntu 21.04", action="install", lst_name_prog=["isomaster"])
    a = Programs('"AstraLinuxSE" 1.6')
    a.stateProg()
    a.actionProg(os_ver='"AstraLinuxSE" 1.6', action="install", lst_name_prog=["timeshift"])
    sys.exit(app.exec_())
