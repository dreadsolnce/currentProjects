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
    from .chice_bginfo import Bginfo_Form


class Programs(QtWidgets.QDialog):
    PATH_CONFIG_BGINFO = sys.path[0] + "/files/bginfo/"

    def __init__(self, os_ver=None):
        super().__init__()
        self.name_debian = ["Ubuntu 21.04", "Ubuntu 21.10"]
        self.os_ver = os_ver  # Версия ОС
        self.list_program = None  # Список программ
        self.dg_gui = None  # Переменная для инициализации окна Debug
        self.listProgram()

    # Формирование списка программ
    def listProgram(self):
        if self.os_ver in self.name_debian:
            self.list_program = ["pycharm-community", "pyqt5-dev-tools", "timeshift", "игры", "mc", "git", "cherrytree",
                                 "goodvibes"]
        elif self.os_ver == '"AstraLinuxSE" 1.6':
            self.list_program = ["timeshift", "bginfo"]

        print("Доступный список программ для {}: {}".format(self.os_ver, self.list_program))

    # Определение состояния пакета в системе (0 - неустановлен, 1 - установлен)
    def stateProg(self):
        state_program = {}  # Словарь: имя программы:статус программы (0 - не установлен, 1 - установлен)
        # Комманда для snap пакета pycharm-community
        command_snap = "snap list pycharm-community >/dev/null; echo $?"
        # Комманда для встроенных игр Ubuntu
        command_games = "dpkg --list | grep gnome-sudoku | awk '{print $2}' | grep -E ^gnome-sudoku$ >/dev/null; echo $?"
        # Команда для BgInfo
        command_bginfo = "cat /usr/local/bin/bginfo.bg >/dev/null; echo $?"

        for name in self.list_program:  # Перебираем весь список доступных программ
            if name == "игры":
                command = command_games
            elif name == "pycharm-community":
                command = command_snap
            elif name == "bginfo":
                command = command_bginfo
            else:
                command = "dpkg --list | grep " + name + " | awk '{print $2}' | grep -E ^" + name + "$ >/dev/null; echo $?"

            out = runCommandReturnStateProg(command)    # Код состояния программы

            state_program[name] = out   # Формируем словарь из имени программы и ключа состояния программы
            if not out:
                print("Программа {} : установлена".format(name))
            elif out:
                print("Программа {} : не установлена".format(name))
        return state_program    # Возвращаем словарь, т.к. данная функция вызывается из внешнего класса

    # Запуск установки либо удаления программы в зависимости от версии ОС
    def actionProg(self, os_ver=None, action=None, lst_name_prog=None):
        # if os_ver == "Ubuntu 21.04":
        if os_ver in self.name_debian:
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
                elif name == "mc":
                    command_2 = " ; sudo rm -rf /usr/share/applications/mcedit.desktop"
                    command = "sudo apt-get install {} -y".format(name) + command_2
                else:
                    if name == "игры":
                        name = "aisleriot gnome-mahjongg gnome-mines gnome-sudoku"
                    # command = "sudo apt-get install {} -y".format(name)
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
            if name == "bginfo":
                conf = None  # Переменная пути конфигурационного файла
                print("Выбран BgInfo")
                if action == "install":
                    self.b2 = ChoiceBginfoWin()
                    self.b2.exec()
                    if self.b2.conf_bg == "Богданов":
                        conf = self.PATH_CONFIG_BGINFO + "bginfo.bpb.bg"
                    elif self.b2.conf_bg == "Колчин":
                        conf = self.PATH_CONFIG_BGINFO + "bginfo.kvl.bg"
                proc_th = SetupBginfo(action=action, config=conf)
                proc_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                proc_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                proc_th.start()
                while proc_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                proc_th.quit()
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


# Класс установки программы TimeShift
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

        if self.act == "install":
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
        elif self.act == "remove":
            print("Удаляем программу timeshift")
            txt = None
            self.dpkg_remove()
            if not self.exit_code:
                txt = "Удаление программы timeshift выполнено успешно!"
            elif self.exit_code:
                txt = "Ошибка при удалении программы timeshift!"
            print(txt)
            self.new_log.emit(txt)
            self.progress.emit(100)

    def unrar_arch(self):
        tar_gz_arch = self.files_path + "/files/timeshift/pack_timeshift.tar.gz"
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

    def dpkg_remove(self):
        process = subprocess.Popen("sudo dpkg --purge timeshift",
                                   shell=True,
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


# Класс установки программы BgInfo
class SetupBginfo(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, action=None, config=None):
        super().__init__()
        self.count = 0
        self.act = action
        self.config = config
        self.exit_code = 0

    def run(self):
        if self.act == "install":
            txt = None  # Переменная содержащая текст для вывода
            print("Устанавливаем программу Bginfo с конф файлом {}".format(self.config))
            if os.path.isfile(self.config):
                dist_file = "/usr/local/bin/bginfo.bg"
                out, err = runCommandReturnErr("sudo cp -R {} {}".format(self.config, dist_file))
                if err:
                    # txt = err.decode('utf-8', 'ignore')
                    txt = err
                    self.exit_code = 1
                elif not err:
                    txt = "Выполнено копирование конфигурационного файла \n"
                self.count += 1
                self.new_log.emit(str(txt))
                self.progress.emit(self.count)
                sleep(0.01)
                if not self.exit_code:
                    print("Изменяем разрешение на файл ", dist_file)
                    out, err = runCommandReturnErr("sudo chmod 777 {}".format(dist_file))
                    if err:
                        # txt = err.decode("utf-8", "ignore")
                        txt = err
                        self.exit_code = 1
                    elif not err:
                        txt = "Выполнено изменение разрешений на файл \n"
                    print("txt = ", txt)
                    self.count += 1
                    self.new_log.emit(str(txt))
                    self.progress.emit(self.count)
                    sleep(0.01)
                if not self.exit_code:
                    # os.system(dist_file + "&")
                    dist_file = "/etc/xdg/autostart/bginfo.desktop"
                    out, err = runCommandReturnErr("sudo cp -R {} {}".format(self.config, dist_file))
                    if err:
                        # txt = err.decode("utf-8", "ignore")
                        txt = err
                        self.exit_code = 1
                    elif not err:
                        txt = "Программа BgInfo добавлена в автозагрузку \n"
                    self.count += 1
                    self.new_log.emit(str(txt))
                    self.progress.emit(self.count)
                    sleep(0.01)
                if not self.exit_code:
                    txt = "Установка программы Bginfo выполенна успешно!"
                    self.count += 1
                    self.new_log.emit(str(txt))
                    self.progress.emit(self.count)
                    sleep(0.01)
            else:
                self.errNotFindFile()
        elif self.act == "remove":
            txt = None
            print("Удаляем программу Bginfo с конф файлом {}".format(self.config))
            dist_file = "/usr/local/bin/bginfo.bg"
            if os.path.isfile(dist_file):
                out, err = runCommandReturnErr("sudo rm -rf {}".format(dist_file))
                if err:
                    txt = err
                    self.exit_code = 1
                elif not err:
                    txt = "Выполнено удаление конфигурационного файла \n"
                self.count += 1
                self.new_log.emit(str(txt))
                self.progress.emit(self.count)
                sleep(0.01)

            dist_file = "/etc/xdg/autostart/bginfo.desktop"
            if os.path.isfile(dist_file):
                out, err = runCommandReturnErr("sudo rm -rf -R {}".format(dist_file))
                if err:
                    txt = err
                    self.exit_code = 1
                elif not err:
                    txt = "Программа BgInfo удалена из автозагрузки! \n"
                self.count += 1
                self.new_log.emit(str(txt))
                self.progress.emit(self.count)
                sleep(0.01)
            if not self.exit_code:
                txt = "Удаление программы Bginfo выполенна успешно!"
            elif self.exit_code:
                txt = "Ошибка при удалении программы BgInfo"
            self.count += 1
            self.new_log.emit(str(txt))
            self.progress.emit(self.count)
            sleep(0.01)
        self.progress.emit(100)

    def errNotFindFile(self):
        txt = "Ошибка! Не найден конфигурационный файл"
        self.new_log.emit(txt)
        print(txt)
        self.exit_code = 1


# Запуск команды с выводом данных выполнения
def runCommandReturnErr(command):
    process = subprocess.Popen(command, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("utf-8"), err.decode("utf-8")


# Запуск команды с выводом кода состояния программы
def runCommandReturnStateProg(command):
    out = None
    if command:
        proc = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()
    return int(out)


class DebugWin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.dg = Ui_Form()  # Инициализация окна Debug
        self.dg.setupUi(self)
        self.dg.pushButton.setEnabled(False)
        self.dg.pushButton_2.setEnabled(False)
        self.show()


class ChoiceBginfoWin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.conf_bg = None
        self.b1 = Bginfo_Form()
        self.b1.setupUi(self)

        self.b1.pushButton.clicked.connect(self.act)

    def act(self):
        self.conf_bg = self.b1.comboBox.currentText()
        print("Выбрана конфигурация товарища {0}а".format(self.conf_bg))
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # u = Programs("Ubuntu 21.04")
    # u.stateProg()
    # u.actionProg(os_ver="Ubuntu 21.04", action="install", lst_name_prog=["isomaster"])
    a = Programs('"AstraLinuxSE" 1.6')
    a.stateProg()
    a.actionProg(os_ver='"AstraLinuxSE" 1.6', action="install", lst_name_prog=["timeshift"])
    sys.exit(app.exec_())
