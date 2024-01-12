#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import time
import shutil
import urllib3
import requests
import threading
import subprocess
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup

from PyQt5 import QtCore, QtWidgets, QtGui

if __name__ == "__main__":
    from Debug import Ui_Form
else:
    from .Debug import Ui_Form
    from .ChoiceBginfo import Bginfo_Form
    from .SshDesktopVnc import Ui_SshDesktopVnc


class Programs(QtWidgets.QDialog):
    PATH_CONFIG_BGINFO = sys.path[0] + "/files/bginfo/"

    def __init__(self, os_ver=None, os_debian=None, os_astra=None):
        super().__init__()
        self.name_debian = os_debian
        self.name_astra = os_astra
        self.os_ver = os_ver  # Версия ОС
        self.list_program = None  # Список программ
        self.dg_gui = None  # Переменная для инициализации окна Debug
        self.listProgram()

    # Формирование списка программ
    def listProgram(self):
        if self.os_ver in self.name_debian:
            self.list_program = ["pycharm-snap", "pycharm-portable", "pyqt5-dev-tools", "timeshift", "игры", "mc", "git",
                                 "cherrytree", "goodvibes", "draw.io", "qemu", "ssh", "gnome-tweaks", "gparted",
                                 "myoffice-standard-home-edition", "snapd", "firefox", "inxi", "lnav"]
        # elif self.os_ver == '"AstraLinuxSE" 1.6':
        elif self.os_ver in self.name_astra:
            self.list_program = ["timeshift", "bginfo", "vnc server 5", "vnc viewer 5", "vnc ярлык", "qemu", "inxi",
                                 "lnav"]

        # print("Доступный список программ для {}: {}".format(self.os_ver, self.list_program))

    # Определение состояния пакета в системе (0 - не установлен, 1 - установлен)
    def stateProg(self):
        state_program = {}  # Словарь: имя программы:статус программы (0 - не установлен, 1 - установлен)
        # Команда для snap пакета pycharm-community
        command_snap = "snap list pycharm-community >/dev/null; echo $?"
        # Команда для pycharm-portable
        command_pycharm_port = "find /home/`logname` -name pycharm.sh >/dev/null; echo $?"
        # Команда для встроенных игр Ubuntu
        command_games = "dpkg --list | grep gnome-sudoku | awk '{print $2}' | grep -E ^gnome-sudoku$ >/dev/null; echo $?"
        # Команда для BgInfo
        command_bginfo = "cat /usr/local/bin/bginfo.bg >/dev/null; echo $?"
        # Команд для vncserver 5.3.1
        command_vnc5server = "dpkg --list | grep realvnc-vnc-server | awk '{print $3}' | grep '5.3.1.17370' >/dev/null; echo $?"
        # Команда дял vncviewer 5.3.3
        command_vnc5viewer = "dpkg --list | grep realvnc-vnc-viewer | awk '{print $3}' | grep '5.3.3' >/dev/null; echo $?"
        # Команда для ярлыков программы vnc
        # command_vnc_desktop = "ls -al ~/Desktop/ | grep _SSH.desktop | grep VNC >/dev/null; echo $?"
        # command_vnc_desktop = "find /home/`logname`/Desktop/ -name 'VNC*' >/dev/null; echo $?"
        command_vnc_desktop = "ls /home/`logname`/Desktop/ | grep 'VNC*' >/dev/null; echo $?"
        # Команда для qemu
        command_qemu = "dpkg-query -L qemu-system-x86 >/dev/null; echo $?"
        # Команда для lnav для AL
        command_lnav = "ls /usr/local/bin | grep lnav >/dev/null; echo $?"

        for name in self.list_program:  # Перебираем весь список доступных программ
            if name == "игры":
                command = command_games
            elif name == "pycharm-snap":
                command = command_snap
            elif name == "pycharm-portable":
                command = command_pycharm_port
            elif name == "bginfo":
                command = command_bginfo
            elif name == "vnc server 5":
                command = command_vnc5server
            elif name == "vnc viewer 5":
                command = command_vnc5viewer
            elif name == "vnc ярлык":
                command = command_vnc_desktop
            elif name == "qemu":
                command = command_qemu
            elif name == "lnav" and self.os_ver in self.name_astra:
                command = command_lnav
            else:
                command = "dpkg --list | grep " + name + " | awk '{print $2}' | grep -E ^" + name + "$ >/dev/null; echo $?"

            out = runCommandReturnStateProg(command)  # Код состояния программы

            state_program[name] = out  # Формируем словарь из имени программы и ключа состояния программы
            # if not out:
            #     print("Программа {} : установлена".format(name))
            # elif out:
            #     print("Программа {} : не установлена".format(name))
        return state_program  # Возвращаем словарь, т.к. данная функция вызывается из внешнего класса

    # Запуск установки либо удаления программы в зависимости от версии ОС
    def actionProg(self, os_ver=None, action=None, lst_name_prog=None):
        # if os_ver == "Ubuntu 21.04":
        print(os_ver)
        if os_ver in self.name_debian:
            print('Запускаем функцию определения действия для Ubuntu')
            self.__actionProgUbuntu(action, lst_name_prog)
        elif os_ver == '"AstraLinuxSE" 1.6' or os_ver == '"AstraLinux" 1.7_x86-64':
            print("Запускаем функция определения действия для AstraLinux 1.6")
            self.__actionProgAstra(action, lst_name_prog, os_ver)

    # Установка либо удаление программ Ubuntu
    def __actionProgUbuntu(self, action=None, lst_name_prog=None):
        self.dg_gui = DebugWin()
        for name in lst_name_prog:
            command = None
            if action == "install":
                print("Устанавливаем программу {}".format(name))
                if name == "pycharm-snap":
                    command_snap_ins = "sudo snap install {}"
                    command = command_snap_ins.format(name) + " --classic"
                elif name == "pyqt5-dev-tools":
                    name = "python3-pyqt5 qtcreator pyqt5-dev-tools qttools5-dev-tools"
                    # command_2 = " ; sudo rm -rf /usr/share/applications/linguist-qt5.desktop" \
                    #             "/usr/share/applications/assistant-qt5.desktop"
                    command_2 = " ; sudo mv /usr/share/applications/linguist-qt5.desktop " \
                                "/usr/share/applications/linguist-qt5.desktop.bak ; " \
                                "sudo mv /usr/share/applications/assistant-qt5.desktop " \
                                "/usr/share/applications/assistant-qt5.desktop.bak ; " \
                                "sudo mv /usr/share/applications/org.qt-project.qtcreator-qt5.desktop " \
                                "/usr/share/applications/org.qt-project.qtcreator-qt5.desktop.bak"
                    command = "sudo apt-get install {} -y".format(name) + command_2
                elif name == "mc":
                    command_2 = " ; sudo rm -rf /usr/share/applications/mcedit.desktop"
                    command = "sudo apt-get install {} -y".format(name) + command_2
                elif name == "qemu":
                    command = "sudo apt-get install qemu-system-x86"
                else:
                    if name == "игры":
                        name = "aisleriot gnome-mahjongg gnome-mines gnome-sudoku"
                    # command = "sudo apt-get install {} -y".format(name)
                    command = "sudo apt-get install {} -y".format(name)
            elif action == "remove":
                print("Удаляем программу {}".format(name))
                if name == "pycharm-snap":
                    command_snap_rem = "sudo snap remove {}"
                    command = command_snap_rem.format(name)
                else:
                    if name == "pyqt5-dev-tools":
                        name = "qtcreator pyqt5-dev-tools qttools5-dev-tools"
                    elif name == "qemu":
                        name = "qemu-system-x86"
                    elif name == "игры":
                        name = "aisleriot gnome-mahjongg gnome-mines gnome-sudoku"
                    command = "sudo apt-get purge {} -y".format(name)
            if name == "draw.io":
                process_th = SetupDiagramNet(act=action)
                process_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                process_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                process_th.start()
                while process_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                process_th.quit()
            if name == "pycharm-portable":
                process_th = SetupPycharmPortable(act=action)
                process_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                process_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                process_th.start()
                while process_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                process_th.quit()
            if name == 'myoffice-standard-home-edition':
                process_th = SetupMyOffice(act=action)
                process_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                process_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                process_th.start()
                while process_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                process_th.quit()
            if name == "snapd":
                process_th = SetupSnapd(act=action)
                process_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                process_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                process_th.start()
                while process_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                process_th.quit()
            if name == "firefox":
                process_th = SetupFirefox(act=action)
                process_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                process_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                process_th.start()
                while process_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                process_th.quit()
            else:
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
    def __actionProgAstra(self, action=None, lst_name_prog=None, os_ver=None):
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
                    elif self.b2.conf_bg == "Колчин №2":
                        conf = self.PATH_CONFIG_BGINFO + "bginfo.kvl2.bg"
                proc_th = SetupBginfo(action=action, config=conf)
                proc_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                proc_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                proc_th.start()
                while proc_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                proc_th.quit()
            if name == "vnc server 5":
                process_th = SetupVncServer5(action=action)
                process_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                process_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                process_th.start()
                while process_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                process_th.quit()
            if name == "vnc viewer 5":
                process_th = SetupVncViewer5(action=action, os_ver=os_ver)
                process_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                process_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                process_th.start()
                while process_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                process_th.quit()
            if name == "vnc ярлык":
                proc_th = None
                if action == "install":
                    self.b4 = SshDesktopVncWin()
                    self.b4.exec()
                    proc_th = SetupVncDesktop(action=action,
                                              vncaddrbook=self.b4.vncaddrbook,
                                              vncviewer=self.b4.vncviewer,
                                              ip_remote_comp=self.b4.ip_remote_comp,
                                              name_login_user=self.b4.name_login_user)
                elif action == "remove":
                    proc_th = SetupVncDesktop(action=action)

                proc_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                proc_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                proc_th.start()
                while proc_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                proc_th.quit()
            if name == "qemu":
                proc_th = SetupQemu(action=action)
                proc_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                proc_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                proc_th.start()
                while proc_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                proc_th.quit()
            if name == "inxi":
                proc_th = SetupInxi(action=action)
                proc_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
                proc_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
                proc_th.start()
                while proc_th.isRunning():
                    QtCore.QCoreApplication.processEvents()
                    QtCore.QThread.msleep(150)
                    self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
                proc_th.quit()
            if name == "lnav":
                proc_th = SetupLnav(action=action)
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
            sleep(0.1)
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
        self.exit_code_forewarning = False
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
                    if os.path.isdir("package"):
                        try:
                            shutil.rmtree("package")
                        except PermissionError as e:
                            self.new_log.emit("Ошибка удаления временного каталога! {}\n".format(e))
                            self.exit_code_forewarning = True
                    res_err = self.copy_file_conf()
                    if res_err:
                        self.new_log.emit("Ошибка при копировании файла настроек!\n")
                        self.exit_code_forewarning = True
                    if self.exit_code_forewarning:
                        self.new_log.emit("Установка выполнена с предупреждениями!\n")
                    else:
                        self.new_log.emit("Установка выполнена успешно!\n")
                else:
                    self.new_log.emit("Ошибка при установке deb пакета!\n")
            else:
                self.new_log.emit("Ошибка при разархивировании архива с программой!\n")
            self.progress.emit(100)
            sleep(0.2)
        elif self.act == "remove":
            print("Удаляем программу timeshift")
            txt = None
            self.dpkg_remove()
            if not self.exit_code:
                txt = "Удаление программы timeshift выполнено успешно!\n"
            elif self.exit_code:
                txt = "Ошибка при удалении программы timeshift!\n"
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

    def copy_file_conf(self):
        file_conf_src = self.files_path + "/files/timeshift/timeshift.json"
        file_conf_dst = '/etc/timeshift.json'
        process = subprocess.Popen("sudo cp {} {}".format(file_conf_src, file_conf_dst), shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()
        return err


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

            # Проверяем установлен ли пакет root-tail
            name_lib = "root-tail"
            command = "dpkg --list | grep " + name_lib + " | awk '{print $2}' | grep -E ^" + name_lib + "$ >/dev/null; echo $?"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if out.decode("utf-8").split()[0] != '0':
                package = sys.path[0] + "/files/bginfo/root-tail*"
                #  Устанавливаем пакет так как его нет в системе
                self.count += 1
                self.new_log.emit("Устанавливаем пакет root-tail\n")
                self.progress.emit(self.count)
                sleep(0.01)
                process = subprocess.Popen("sudo dpkg -i %s" % package, shell=True,
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
            if not self.exit_code:
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
                        if self.config == sys.path[0] + "/files/bginfo/" + "bginfo.kvl2.bg":
                            source_file = sys.path[0] + "/files/bginfo/" + "start_stop_bginfo.sh"
                            out, err = runCommandReturnErr("sudo cp -R {} /usr/local/bin/".format(source_file))
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
                        # desktop_file = None
                        if self.config == sys.path[0] + "/files/bginfo/" + "bginfo.kvl2.bg":
                            desktop_file = sys.path[0] + "/files/bginfo/bginfo.kvl2.desktop"
                        else:
                            desktop_file = sys.path[0] + "/files/bginfo/bginfo.desktop"
                        # out, err = runCommandReturnErr("sudo cp -R {} {}".format(self.config, dist_file))
                        out, err = runCommandReturnErr("sudo cp -R {} {}".format(desktop_file, dist_file))
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
                        print("Запускаем программу")
                        os.system("/usr/local/bin/bginfo.bg &")
                    if not self.exit_code:
                        txt = "Установка программы Bginfo выполнена успешно!"
                        self.count += 1
                        self.new_log.emit(str(txt))
                        self.progress.emit(self.count)
                        sleep(0.01)
                else:
                    self.errNotFindFile()
            else:
                txt = "Ошибка установки пакета root-tail!"
                self.count += 1
                self.new_log.emit(str(txt))
                self.progress.emit(self.count)
                sleep(0.01)
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
                os.system("pkill root-tail")
                txt = "Удаление программы Bginfo выполнена успешно!\n"
            elif self.exit_code:
                txt = "Ошибка при удалении программы BgInfo\n"
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


# Установка программы Vnc Server 5
class SetupVncServer5(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, action=None):
        super().__init__()
        self.count = 0
        self.exit_code = 0
        self.action = action
        self.tar_gz_arch = sys.path[0] + "/files/vnc/vncserver5/VNC-5.3.1-Linux-x64-DEB.tar.gz"

    def run(self):
        if self.action == "install":
            if os.path.isfile(self.tar_gz_arch):
                text = "Разархивируем архив с программой в папку /tmp\n"
                self.new_log.emit(text)
                self.run_process("tar xvzf %s -C /tmp/" % self.tar_gz_arch)
                if self.exit_code:
                    text = "Ошибка при распаковке!"
                    self.new_log.emit(text)
                elif not self.exit_code:
                    command = "sudo dpkg -i /tmp/VNC-Server*.deb"
                    self.run_process(command)
                    if self.exit_code:
                        text = "Ошибка при установке!"
                        self.new_log.emit(text)
                    elif not self.exit_code:
                        command = "sudo vnclicense -add YMDFH-2BU2P-E4L4E-HRQ4S-PHTDA"
                        self.run_process(command)
                        if self.exit_code:
                            text = "Ошибка активации сервера vnc"
                            self.new_log.emit(text)
                        elif not self.exit_code:
                            text = "Добавляем службу в автозагрузку\n"
                            self.new_log.emit(text)
                            sleep(1)
                            command = "sudo systemctl enable vncserver-x11-serviced"
                            self.run_process(command)
                            if self.exit_code:
                                text = "Ошибка добавления службы в автозагрузку"
                                self.new_log.emit(text)
                            elif not self.exit_code:
                                text = "Запускаем службу\n"
                                self.new_log.emit(text)
                                sleep(1)
                                command = "sudo systemctl start vncserver-x11-serviced.service"
                                self.run_process(command)
                                if self.exit_code:
                                    text = "Ошибка запуска службы"
                                    self.new_log.emit(text)
                                elif not self.exit_code:
                                    text = "Копируем файл с настройками программы common.custom в /etc/vnc/config.d/\n"
                                    self.new_log.emit(text)
                                    sleep(1)
                                    command = "sudo mv /tmp/common.custom /etc/vnc/config.d/common.custom"
                                    self.run_process(command)
                                    if self.exit_code:
                                        text = "Ошибка применения настроек!"
                                        self.new_log.emit(text)
                                    elif not self.exit_code:
                                        text = "Удаляем временные файлы\n"
                                        self.new_log.emit(text)
                                        sleep(1)
                                        self.delete_file_for_install()
                                        if self.exit_code:
                                            text = "Ошибка при удалении временных файлов!"
                                            self.new_log.emit(text)
                                        elif not self.exit_code:
                                            text = "Установка выполнена успешно!"
                                            self.new_log.emit(text)
            else:
                text = "Ошибка! Не найден архив с программой!"
                self.new_log.emit(text)
                self.exit_code = 1
        elif self.action == "remove":
            text = "Останавливаем службу\n"
            self.new_log.emit(text)
            command = "sudo systemctl stop vncserver-x11-serviced"
            self.run_process(command)
            if self.exit_code:
                text = "Ошибка остановки службы"
                self.new_log.emit(text)
            elif not self.exit_code:
                text = "Служба остановлена\n"
                self.new_log.emit(text)
            if not self.exit_code:
                command = "sudo dpkg --purge realvnc-vnc-server"
                self.run_process(command)
            if self.exit_code:
                text = "Ошибка удаления программы!"
                self.new_log.emit(text)
            else:
                text = "Пакет удален!\n"
                self.new_log.emit(text)
            text = "Удаляем следы программы\n"
            self.new_log.emit(text)
            self.delete_file()
            text = "Удаление программы завершено успешно!\n"
            self.new_log.emit(text)
        self.progress.emit(100)

    def run_process(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        line_out = True
        while line_out:
            line_out = process.stdout.readline()
            self.new_log.emit(line_out.decode('utf-8', 'ignore'))
            self.progress.emit(self.count)
            print(line_out.decode("utf-8"), end="")
            self.count += 1
            sleep(0.01)
        process.communicate()
        self.exit_code = self.exit_code + process.returncode
        sleep(0.2)

    # Удаление следов программы
    def delete_file(self):
        file1 = "/etc/vnc"
        file2 = "/home/*/.vnc"
        file3 = "/root/.vnc"
        file4 = "/run/vncserver-x11-serviced.pid"
        file5 = "/etc/systemd/system/multi-user.target.wants/vncserver-x11-serviced.service"
        file6 = "/usr/lib/systemd/system/vncserver-virtuald.service /usr/lib/systemd/system/vncserver-x11-serviced.service"
        command = "sudo rm -rf {0} {1} {2} {3} {4} {5}".format(file1, file2, file3, file4, file5, file6)
        self.run_process(command)

        for f in glob.iglob("/home/*/.fly/startmenu/*/realvnc-vnclicense*"):  # generator, search immediate subdirectories
            command = "sudo rm -rf {0}".format(f)
            self.run_process(command)

        for f in glob.iglob("/home/*/.fly/startmenu/*/realvnc-vncserver*"):  # generator, search immediate subdirectories
            command = "sudo rm -rf {0}".format(f)
            self.run_process(command)

    # Удаление временных, которые создаются при установке программы
    def delete_file_for_install(self):
        # Удаление ярлыков из меню пуск
        for f in glob.iglob("/home/*/.fly/startmenu/*/realvnc-vnclicense*"):  # generator, search immediate subdirectories
            command = "sudo rm -rf {0}".format(f)
            self.run_process(command)
        for f in glob.iglob("/home/*/.fly/startmenu/*/realvnc-vncserver*"):  # generator, search immediate subdirectories
            command = "sudo rm -rf {0}".format(f)
            self.run_process(command)

        # Удаление временных файлов
        file1 = "/tmp/common.custom"
        file2 = "/tmp/key_vnc.txt"
        file3 = "/tmp/realvnc-vncviewer.desktop"
        file4 = "/tmp/VNC-Server-5.3.1-Linux-x64.deb"
        file5 = "/tmp/VNC-Viewer-5.3.1-Linux-x64.deb"
        command = "sudo rm -rf {0} {1} {2} {3} {4}".format(file1, file2, file3, file4, file5)
        self.run_process(command)


# Установка программы Vnc Viewer 5
class SetupVncViewer5(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, action=None, os_ver=None):
        super().__init__()
        self.count = 0
        self.exit_code = 0
        self.action = action
        self.os_ver = os_ver
        self.dir_vnc_addrbook = "/usr/share/VNCAddressBook"
        self.deb_pack = sys.path[0] + "/files/vnc/vncviewer5/VNC-Viewer-5.3.3-Linux-x64.deb"
        self.tag_desk = sys.path[0] + "/files/vnc/vncviewer5/realvnc-vncaddrbook.desktop"
        self.tar_xvnc4viewer = sys.path[0] + "/files/vnc/vncviewer5/xvnc4viewer.tar.gz"

    def run(self):
        if self.action == "install":
            if self.os_ver == '"AstraLinuxSE" 1.6' or self.os_ver == '"AstraLinux" 1.7_x86-64':
                if os.path.isfile(self.deb_pack):
                    # command = "sudo dpkg -i {}".format(self.deb_pack)
                    # self.run_process(command)
                    self.exit_code = 0
                    if self.exit_code:
                        text = "Ошибка при установке!"
                        self.new_log.emit(text)
                    elif not self.exit_code:
                        # if not os.path.isdir(self.dir_vnc_addrbook):
                        #     command = "sudo mkdir {} && sudo chmod -R 777 {}".format(self.dir_vnc_addrbook, self.dir_vnc_addrbook)
                        #     self.run_process(command)
                        #     if self.exit_code:
                        #         text = "Ошибка создания каталога для vnc addrbook"
                        #         self.new_log.emit(text)
                        # text = "Изменяем ярлык VNC Address Book\n"
                        # self.new_log.emit(text)
                        # sleep(1)
                        # if os.path.isfile(self.tag_desk):
                        #     command = "sudo cp -R {} ~/.fly/startmenu/network/".format(self.tag_desk)
                        #     self.run_process(command)
                        # else:
                        #     text = "Ошибка! Не найден файл ярлыка!"
                        #     self.new_log.emit(text)
                        # text = "Изменяем настройки ОС для корректного запуска программы\n"
                        # self.new_log.emit(text)
                        # sleep(1)
                        # if not os.path.isfile("/etc/X11/trusted.bak"):
                        #     command = "sudo cp /etc/X11/trusted /etc/X11/trusted.bak"
                        #     self.run_process(command)
                        #     if self.exit_code:
                        #         text = "Ошибка создания резервной копии файла /etc/X11/trusted\n"
                        #         self.new_log.emit(text)
                        # if os.path.isfile("/etc/X11/trusted.bak"):
                        #     exit_code = find_string(file="/etc/X11/trusted", string="/usr/bin/vncviewer(NESTED_R)")
                        #     if exit_code == 0:
                        #         change_string(file="/etc/X11/trusted",
                        #                       old_str="/usr/bin/vncviewer(NESTED_R)",
                        #                       new_str="/usr/bin/vncviewer")
                        #         if os.path.isfile("/tmp/trusted.tmp"):
                        #             command = "sudo mv /tmp/trusted.tmp /etc/X11/trusted"
                        #             self.run_process(command)
                        #             if self.exit_code:
                        #                 text = "Ошибка копирования файла /tmp/trusted.tmp\n"
                        #                 self.new_log.emit(text)
                        #         else:
                        #             text = "Ошибка применения настроек ОС!\n"
                        #             self.new_log.emit(text)
                        #             sleep(1)
                        if self.os_ver == '"AstraLinux" 1.7_x86-64':
                            print("Установка для Astra Linux 1.7")
                            command = "tar -xvf {} -C /tmp/".format(self.tar_xvnc4viewer)
                            print (command)
                            self.run_process(command)
                            if self.exit_code:
                                text = "Ошибка распаковки архива xvnc4viewer!"
                                self.new_log.emit(text)
                            else:
                                command = "sudo dpkg -i /tmp/xvnc4viewer/libfltk1* /tmp/xvnc4viewer/libfltk-* " \
                                          "/tmp/xvnc4viewer/tigervnc* /tmp/xvnc4viewer/xvnc4viewer* && sudo dpkg --purge " \
                                          "xvnc4viewer tigervnc-viewer libfltk-images1.3 libfltk1.3"
                                print(command)
                                self.run_process(command)
                                if self.exit_code:
                                    text = "Ошибка при установке доп. пакетов!"
                                    self.new_log.emit(text)
                        text = "Установка завершена!"
                        self.new_log.emit(text)
                else:
                    text = "Ошибка! Не найден deb пакет с программой!"
                    self.new_log.emit(text)
                    self.exit_code = 1
        elif self.action == "remove":
            if self.os_ver == '"AstraLinuxSE" 1.6' or self.os_ver == '"AstraLinux" 1.7_x86-64':
                command = "sudo dpkg --purge realvnc-vnc-viewer"
                self.run_process(command)
                if self.exit_code:
                    text = "Ошибка при удалении пакета!"
                    self.new_log.emit(text)
                elif not self.exit_code:
                    text = "Удаляем следы программы\n"
                    self.new_log.emit(text)
                    sleep(1)
                    self.delete_file()
                    text = "Удаление программы завершено успешно!\n"
                    self.new_log.emit(text)
        self.progress.emit(100)

    def run_process(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        line_out = True
        while line_out:
            line_out = process.stdout.readline()
            self.new_log.emit(line_out.decode('utf-8', 'ignore'))
            self.progress.emit(self.count)
            print(line_out.decode("utf-8"), end="")
            self.count += 1
            sleep(0.01)
        process.communicate()
        self.exit_code = self.exit_code + process.returncode
        sleep(0.2)

    # Удаление следов программы
    def delete_file(self):
        for f in glob.iglob("/home/*/.fly/startmenu/*/realvnc-vncviewer*"):  # generator, search immediate subdirectories
            command = "sudo rm -rf {0}".format(f)
            self.run_process(command)

        for f in glob.iglob("/home/*/Desktop/realvnc-vncviewer*"):
            command = "sudo rm -rf {0}".format(f)
            self.run_process(command)

        for f in glob.iglob("/home/*/Desktop/realvnc-vncaddr*"):
            command = "sudo rm -rf {0}".format(f)
            self.run_process(command)

        for f in glob.iglob("/home/*/.fly/startmenu/*/realvnc-vncaddr*"):
            command = "sudo rm -rf {0}".format(f)
            self.run_process(command)


# Установка ярлыков программы vnc viewer
class SetupVncDesktop(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, action=None, vncaddrbook=False, vncviewer=False, ip_remote_comp=None, name_login_user=None):
        super().__init__()
        self.count = 0
        self.exit_code = 0
        self.file_etalon_addrbook = sys.path[0] + "/files/vnc/vncdesktop/VNCAddrBook_SSH.desktop"
        print(self.file_etalon_addrbook)
        self.file_etalon_viewer = sys.path[0] + "/files/vnc/vncdesktop/VNCViewer_SSH.desktop"
        print(self.file_etalon_viewer)
        self.action = action
        self.vncaddrbook = vncaddrbook
        self.vncviewer = vncviewer
        self.ip_remote_comp = ip_remote_comp
        self.name_login_user = name_login_user

    def run(self):
        if self.action == "install":
            text = "Устанавливаем ярлыки для запуска vncviewer!\n"
            self.new_log.emit(text)
            if self.vncaddrbook is True:
                self.install_desktop(name="vncaddrbook")
            if self.vncviewer is True:
                self.install_desktop(name="vncviewer")
        elif self.action == "remove":
            self.remove_desktop()
        self.progress.emit(100)

    def install_desktop(self, name=None):
        file = None
        if name == "vncaddrbook":
            file = self.file_etalon_addrbook
        elif name == "vncviewer":
            file = self.file_etalon_viewer
        self.cp_file(file)
        if self.exit_code == 0:
            self.count += 1
            self.progress.emit(self.count)
            text = "Скопировали эталонный файл на рабочий стол!\n"
            self.new_log.emit(text)
            sleep(1)
        else:
            text = "Ошибка копирования файла эталонного файла на рабочий стол'\n"
            self.new_log.emit(text)
            sleep(1)
        if self.exit_code == 0:
            self.count += 1
            self.progress.emit(self.count)
            name_file = file.split("/")[-1]
            if file == self.file_etalon_addrbook:
                change_string("{}/Desktop/{}".format(os.getenv("HOME"), name_file), "Exec=",
                              "Exec=ssh {}@{} vncaddrbook AddressBook=/usr/share/VNCAddressBook/"
                              .format(self.name_login_user, self.ip_remote_comp))
            elif file == self.file_etalon_viewer:
                change_string("{}/Desktop/{}".format(os.getenv("HOME"), name_file), "Exec=",
                              "Exec=ssh {}@{} vncviewer"
                              .format(self.name_login_user, self.ip_remote_comp))
            self.mv_file(file_destination="{}/Desktop/{}".format(os.getenv("HOME"), name_file))
            if self.exit_code:
                text = "Ошибка копирования временного измененного файла\n"
                self.new_log.emit(text)
            if self.exit_code == 0:
                self.count += 1
                self.progress.emit(self.count)
                text = "Ярлык запуска для {} успешно создан на рабочем столе!\n".format(name_file)
                self.new_log.emit(text)

    def remove_desktop(self):
        command = "rm -rf ~/Desktop/VNCAddrBook_SSH.desktop ~/Desktop/VNCViewer_SSH.desktop"
        self.run_process(command)
        if self.exit_code == 0:
            self.count += 1
            self.progress.emit(self.count)
            text = "Ярлыки успешно удалены!\n"
            self.new_log.emit(text)
            sleep(2)
        else:
            self.count += 1
            self.progress.emit(self.count)
            text = "Ошибка при удалении ярлыков!\n"
            self.new_log.emit(text)
            sleep(2)

    def cp_file(self, file=None):
        command = "cp -R {} ~/Desktop/".format(file)
        self.run_process(command)

    def mv_file(self, file_destination=None):
        command = "sudo mv /tmp/trusted.tmp {}".format(file_destination)
        self.run_process(command)

    def run_process(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        line_out = True
        while line_out:
            line_out = process.stdout.readline()
            self.new_log.emit(line_out.decode('utf-8', 'ignore'))
            self.progress.emit(self.count)
            print(line_out.decode("utf-8"), end="")
            self.count += 1
            sleep(0.01)
        process.communicate()
        self.exit_code = self.exit_code + process.returncode
        sleep(0.2)


# Установка программы inxi для AL16
class SetupInxi(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, action=None):
        super().__init__()
        self.count = 0
        self.exit_code = 0
        self.action = action
        self.deb_pack = sys.path[0] + "/files/inxi/inxi.deb"

    def run(self):
        if self.action == "install":
            if os.path.isfile(self.deb_pack):
                command = "sudo dpkg -i {}".format(self.deb_pack)
                self.run_process(command)
                if self.exit_code:
                    text = "Ошибка при установке!"
                    self.new_log.emit(text)
                elif not self.exit_code:
                    text = "Установка завершена!"
                    self.new_log.emit(text)
            else:
                text = "Ошибка! Не найден deb пакет с программой!"
                self.new_log.emit(text)
                self.exit_code = 1
        elif self.action == "remove":
            command = "sudo dpkg --purge inxi"
            self.run_process(command)
            if self.exit_code:
                text = "Ошибка при удалении пакета!"
                self.new_log.emit(text)
            elif not self.exit_code:
                text = "Удаление программы завершено успешно!\n"
                self.new_log.emit(text)
        self.progress.emit(100)

    def run_process(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        line_out = True
        while line_out:
            line_out = process.stdout.readline()
            self.new_log.emit(line_out.decode('utf-8', 'ignore'))
            self.progress.emit(self.count)
            print(line_out.decode("utf-8"), end="")
            self.count += 1
            sleep(0.01)
        process.communicate()
        self.exit_code = self.exit_code + process.returncode
        sleep(0.2)


# Установка программы lnav
class SetupLnav(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, action=None):
        super().__init__()
        self.action = action
        self.count = 0
        self.exit_code = 0
        self.file_path = sys.path[0] + "/files/lnav/lnav"

    def run(self):
        if self.action == "install":
            text = "Устанавливаем программу lnav\n"
            self.new_log.emit(text)
            command = "sudo cp -R {} /usr/local/bin/".format(self.file_path)
            self.run_process(command)
            if self.exit_code == 0:
                self.count += 1
                self.progress.emit(self.count)
                text = "Программа установлена успешно!\n"
                self.new_log.emit(text)
                sleep(1)
            else:
                text = "Ошибка при установке'\n"
                self.new_log.emit(text)
                sleep(1)
        elif self.action == "remove":
            text = "Удаляем программу lnav\n"
            self.new_log.emit(text)
            command = "sudo rm -rf /usr/local/bin/lnav"
            self.run_process(command)
            if self.exit_code == 0:
                self.count += 1
                self.progress.emit(self.count)
                text = "Программа удалена успешно успешно!\n"
                self.new_log.emit(text)
                sleep(1)
            else:
                text = "Ошибка при удалении'\n"
                self.new_log.emit(text)
                sleep(1)
        self.progress.emit(100)


    def run_process(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        line_out = True
        while line_out:
            line_out = process.stdout.readline()
            self.new_log.emit(line_out.decode('utf-8', 'ignore'))
            self.progress.emit(self.count)
            print(line_out.decode("utf-8"), end="")
            self.count += 1
            sleep(0.01)
        process.communicate()
        self.exit_code = self.exit_code + process.returncode
        sleep(0.2)

# Установка программы pycharm-portable
class SetupPycharmPortable(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, act=None):
        super().__init__()
        self.act = act
        self.link_to_download = "unknown"
        self.dir_for_pycharm = "/opt/pycharm"  # Каталог установки программы
        self.current_user = os.getlogin()  # Текущий пользователь системы
        self.exit_code = 0
        self.count = 0
        self.return_code_download = None
        self.full_path_tmp_arch = None  # Полный путь до скачанного архива с программой

    def run(self):
        if self.act == "install":
            self.new_log.emit("Устанавливаем программу pycharm в папку /opt\n")
            self.progress.emit(self.count)
            sleep(1)
            self.link_to_download = self.parsingWebsitePycharm()
            print("Ссылка для скачивания программы: ", self.link_to_download)
            out = self.check_targz_pycharm(package=self.link_to_download.split("/")[-1])
            if not out:
                txt = "Файл еще не скачен!\n"
                self.count_and_text(txt)
                print(txt)
                if self.link_to_download != "unknown":
                    self.downloadPackage()
                    self.count_and_text()
                    if self.return_code_download == 0:
                        txt = "Загрузка завершена!\n"
                        print(txt)
                        self.count_and_text(txt)
                        self.install_pycharm()
                    else:
                        txt = "Ошибка при загрузке!\n"
                        print(txt)
                        self.count_and_text(txt)
                        self.progress.emit(100)
            elif out:
                txt = "Файл уже скачен!"
                print(txt, end="\n")
                self.count_and_text(txt)
                self.install_pycharm()
        elif self.act == "remove":
            txt = "Удаляем программу pycharm из папки /opt"
            print(txt)
            self.count_and_text(txt)
            self.remove_pycharm()

    # Парсинг сайта для получения ссылки для скачивания
    def parsingWebsitePycharm(self):
        url = "https://www.jetbrains.com/pycharm/whatsnew/"
        user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"
        headers = {"Accept": "*/*", "user_agent": user_agent}
        urllib3.disable_warnings()
        text_html_for_parser = requests.get(url, headers=headers)

        soup = BeautifulSoup(text_html_for_parser.content, "html.parser")

        text_ver_pycharm = soup.title.text.split()[-1]
        print("Версия PyCharm для скачивания: ", text_ver_pycharm)

        url_for_download_wget = "https://download.jetbrains.com/python/pycharm-community-{}.tar.gz".format(text_ver_pycharm)

        self.new_log.emit("Ссылка для скачивания: {}\n".format(url_for_download_wget))
        return url_for_download_wget

    # Функция проверки скачен пакет или
    def check_targz_pycharm(self, package=None):
        self.full_path_tmp_arch = "/tmp/{}".format(package)
        print("Полный путь к архиву на компьютере: {}".format(self.full_path_tmp_arch))
        if os.path.isfile(self.full_path_tmp_arch):
            return True
        else:
            return False

    # Скачивание пакета по ссылке
    def downloadPackage(self):
        self.new_log.emit("Скачиваем пакет!\n")
        sleep(1)
        t = threading.Thread(target=self.runDownload, name="Thread1")
        t.start()
        sleep(1)
        self.readDataRunProcess()
        t.join()

    # Запуск процесса скачивания
    def runDownload(self):
        command = "wget --no-check-certificate --output-file=/tmp/data_out.txt -P /tmp " + self.link_to_download
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.communicate()

        self.return_code_download = proc.returncode

    # Чтение файла лога загрузки
    def readDataRunProcess(self):
        file_path = "/tmp/data_out.txt"
        s = 0
        with open(file_path, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    s += 1
                    time.sleep(0.1)
                    if s > 5:
                        f.close()
                        break
                else:
                    s = 0
                self.new_log.emit(line)
        os.remove(file_path)

    # Установка программы
    def install_pycharm(self):
        txt = "Разархивируем скаченный архив в системную папку /opt/"
        print(txt)
        self.count_and_text(txt)
        err = self.mkdir_pycharm()
        if not err:
            err = self.unrar_pycharm()
            if not err:
                self.create_label()
                self.copy_label()

    # Создание папки куда будет извлечён архив
    def mkdir_pycharm(self):
        err = None

        if not os.path.isdir(self.dir_for_pycharm):
            out, err = runCommandReturnErr("sudo mkdir {}".format(self.dir_for_pycharm))
        if not err:
            out, err = runCommandReturnErr("sudo chown -R {}:{} {}".format(
                self.current_user,
                self.current_user,
                self.dir_for_pycharm))
            if not err:
                txt = "Общий каталог для установки {} успешно создан".format(self.dir_for_pycharm)
                print(txt)
                self.count_and_text(txt)
            else:
                txt = "Ошибка! {}\n".format(err)
                print(txt)
                self.count_and_text(txt)
        else:
            txt = "Ошибка! {}\n".format(err)
            print(txt)
            self.count_and_text(txt)

        return err

    # Распаковка скачанного архива
    def unrar_pycharm(self):
        process = subprocess.Popen("tar xvzf {} -C {}".format(self.full_path_tmp_arch, self.dir_for_pycharm),
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out = True
        j = 0
        while out:
            out = process.stdout.readline()
            self.new_log.emit(out.decode('utf-8', 'ignore'))
            if j > 100:
                self.progress.emit(self.count)
                self.count += 1
                j = 0
            j += 1

        process.communicate()
        exit_code = process.returncode
        sleep(0.2)

        if exit_code == 0:
            txt = "Распаковка архива выполнена успешно!"
        else:
            txt = "Ошибка при распаковке!"
        print(txt)
        self.count_and_text(txt)

        return exit_code

    # Создание ярлыка для запуска
    def create_label(self):
        # Путь к исполняемому файлу
        path_to_exec = self.full_path_tmp_arch.split("/")[-1].split(".tar.gz")[0]

        txt = "Каталог c версией программы {}".format(path_to_exec)
        print(txt)
        # self.count_and_text(txt)

        file_tmp = "/tmp/PyCharm.desktop.tmp"
        with open(file_tmp, "w") as f:
            txt_for_write = "[Desktop Entry]\n" \
                            "Type=Application\n" \
                            "Name=PyCharm\n" \
                            "GenericName=PyCharm\n" \
                            "Comment=Editor\n" \
                            "Exec=" + self.dir_for_pycharm + "/" + path_to_exec + "/bin/pycharm.sh\n" \
                            "TryExec=" + self.dir_for_pycharm + "/" + path_to_exec + "/bin/pycharm.sh\n" \
                            "Terminal=false\n" \
                            "Icon=" + self.dir_for_pycharm + "/" + path_to_exec + "/bin/pycharm.png\n" \
                            "Categories=Development;\n" \
                            "StartupNotify=true\n" \
                            "# MimeType=image/bmp;image/jpeg;image/png;image/tiff;image/gif;\n"

            f.write(txt_for_write)

    # Перемещение временного ярлыка в папку с ярлыками
    def copy_label(self):
        file_tmp = "/tmp/PyCharm.desktop.tmp"
        runCommandReturnErr("sudo mv {} /usr/share/applications/PyCharm.desktop".format(file_tmp))
        if not os.path.isfile("/usr/share/applications/PyCharm.desktop"):
            txt = "Ошибка при создании ярлыка программы!\n"
        else:
            txt = "Ярлык программы создан успешно!\nПрограмма установлена!"
        print(txt)
        self.count_and_text(txt)
        self.progress.emit(100)

    # Удаление программы
    def remove_pycharm(self):
        err = self.remove_dir_opt()
        if not err:
            self.remove_label()
        self.progress.emit(100)

    def remove_dir_opt(self):
        out, err = runCommandReturnErr("sudo rm -rf {}".format(self.dir_for_pycharm))
        if not err:
            txt = "Удаление папки {} выполнено!".format(self.dir_for_pycharm)
            print(txt)
            self.count_and_text(txt)
        elif err:
            txt = "Ошибка при удалении папки {}!".format(self.dir_for_pycharm)
            print(txt)
            self.count_and_text()
        return err

    def remove_label(self):
        txt = None
        label = "/usr/share/applications/PyCharm.desktop"
        out, err = runCommandReturnErr("sudo rm -rf {}".format(label))
        if not err:
            txt = "Удаление ярлыка выполнено!\nУдаление программы выполнено успешно!"
        elif err:
            txt = "Ошибка при удалении ярлыка!\nОшибка при удалении программы!"
        print(txt)
        self.count_and_text(txt)
        return err

    def count_and_text(self, txt=None):
        sleep(0.1)
        if txt:
            self.new_log.emit(txt + "\n")
        self.count += 1
        self.progress.emit(self.count)


# Установка программы Diagram.net для Ubuntu
class SetupDiagramNet(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, act=None):
        super().__init__()
        self.act = act
        self.link = "unknown"
        self.exit_code = 0
        self.count = 0
        self.return_code_download = None

    def run(self):
        if self.act == "install":
            self.new_log.emit("Устанавливаем программу diagram.net\n")
            self.progress.emit(self.count)
            sleep(1)
            self.link = self.parsing_diagram_net()
            sleep(1)
            if self.link != "unknown":
                self.count += 1
                self.progress.emit(self.count)
                self.download_package()
                self.count += 1
                self.progress.emit(self.count)
                if self.return_code_download == 0:
                    self.new_log.emit("Загрузка завершена!\n")
                    return_code_install = self.dpkg_diagram_net_install()
                    if return_code_install == 0:
                        self.new_log.emit("Установка завершена успешно!")
                    else:
                        self.new_log.emit("Ошибка при установке!")
                else:
                    self.new_log.emit("Ошибка при скачивании")
                self.progress.emit(100)
        elif self.act == "remove":
            txt = None
            self.dpkg_diagram_net_remove()
            if not self.exit_code:
                txt = "Удаление программы diagram.net выполнено успешно!\n"
            elif self.exit_code:
                txt = "Ошибка при удалении программы diagram.net\n"
            self.new_log.emit(txt)
            self.progress.emit(100)

    # Парсим сайт программы, чтобы узнать текущую версию программы на данный момент
    def parsing_diagram_net(self):
        link = "unknown"
        dn_http = "https://github.com/jgraph/drawio-desktop/releases/latest"
        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
        headers = {"user agent": user_agent}
        urllib3.disable_warnings()
        html = requests.get(dn_http, headers)

        soup = BeautifulSoup(html.content, "html.parser")
        price = soup.find("div", {"class": "markdown-body my-3"}).find("p").find_all('a')

        for i in price:
            if "deb" in i.get("href"):
                link = i.get("href")

        print("Ссылка для скачивания: ", link)
        self.new_log.emit("Ссылка для скачивания: \n" + link)
        return link

    # Скачивание пакета по ссылке
    def download_package(self):
        self.new_log.emit("\nСкачиваем пакет!\n")
        sleep(1)
        t = threading.Thread(target=self.run_down, name='Thread1')
        t.start()
        sleep(1)
        self.run_read()
        t.join()

    # Запуск процесса скачивания
    def run_down(self):
        process = subprocess.Popen("wget --no-check-certificate --output-file=/tmp/test.txt " + self.link,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.communicate()
        self.return_code_download = process.returncode

    # Чтение фала лога загрузки
    def run_read(self):
        file_path = "/tmp/test.txt"
        s = 0
        with open(file_path, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    s += 1
                    time.sleep(0.1)
                    if s > 5:
                        f.close()
                        break
                else:
                    s = 0
                self.new_log.emit(line)

    # Установка deb пакета
    def dpkg_diagram_net_install(self):
        package_name = self.link.split("/")[-1]
        process = subprocess.Popen("sudo dpkg -i %s" % package_name,
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
        sleep(0.2)
        os.remove(package_name)
        return process.returncode

    # Удаление программы diagram.net
    def dpkg_diagram_net_remove(self):
        process = subprocess.Popen("sudo dpkg --purge draw.io",
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


class SetupQemu(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(float)

    def __init__(self, action=None):
        super().__init__()
        self.libs = ["libibverbs1", "ibverbs-providers", "ipxe-qemu", "libaio1", "libbrlapi0.6", "libcacard0",
                     "libcapstone4", "libpmem1", "librdmacm1", "libslirp0", "libspice-server1", "libusbredirparser1",
                     "libvdeplug2", "libvirglrenderer0", "ovmf", "seabios", "qemu-utils", "libfdt1", "qemu-system-common",
                     "qemu-system-data", "qemu-system-x86"]
        self.action = action
        self.count = 0
        self.exit_code = 0

    def run(self):
        if self.action == "install":
            print("Установка пакета qemu")
            self.insQemu()
        elif self.action == "remove":
            print("Удаление пакета qemu")
            self.delQemu()

    def delQemu(self):
        text = None
        command = "sudo apt-get purge qemu-system-x86 qemu-system-data qemu-system-common qemu-utils -y"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        line_out = True
        while line_out:
            line_out = process.stdout.readline()
            self.new_log.emit(line_out.decode('utf-8', 'ignore'))
            self.progress.emit(self.count)
            self.count += 2
            sleep(0.01)
        process.communicate()
        self.exit_code = self.exit_code + process.returncode
        sleep(0.2)
        if not self.exit_code:
            text = "Удаление программы qemu-system-x86 выполнено УСПЕШНО!\n"
        elif self.exit_code:
            text = "Непредвиденная ОШИБКА!\n"
        self.new_log.emit(text)
        self.progress.emit(100)

    def insQemu(self):
        text = None
        for i in self.libs:
            full_path_lib = sys.path[0] + "'/files/lib/qemu/" + i + "'*"
            command = "sudo dpkg -i {}".format(full_path_lib)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            line_out = True
            while line_out:
                line_out = process.stdout.readline()
                self.new_log.emit(line_out.decode('utf-8', 'ignore'))
                self.progress.emit(self.count)
                self.count += 0.5
                sleep(0.01)
            process.communicate()
            self.exit_code = self.exit_code + process.returncode
            sleep(0.2)
        if not self.exit_code:
            text = "Установка программы qemu-system-x86 выполнено УСПЕШНО!\n"
        elif self.exit_code:
            text = "Непредвиденная ОШИБКА!\n"
        self.new_log.emit(text)
        self.progress.emit(100)


# Установка программы Мой офис
class SetupMyOffice(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, act=None):
        super().__init__()
        self.count = 0
        self.return_code_download = None
        self.exit_code = 0
        self.act = act
        self.link_download = None

    def run(self):
        if self.act == "install":
            self.new_log.emit("Устанавливаем программу myoffice-standard-home-edition\n")
            self.progress.emit(self.count)
            sleep(1)
            self.link_download = self.parsing_site()
            sleep(2)
            if self.link_download:
                self.count += 1
                self.progress.emit(self.count)
                self.download_package()
                self.count += 1
                self.progress.emit(self.count)
                if self.return_code_download == 0:
                    self.new_log.emit("Загрузка завершена!\n")
                    return_code_install = self.dpkg_myoffice_install()
                    if return_code_install == 0:
                        self.new_log.emit("Установка завершена успешно!")
                    else:
                        self.new_log.emit("Ошибка при установке!")
                else:
                    self.new_log.emit("Ошибка при скачивании")
                self.progress.emit(100)
        elif self.act == "remove":
            txt = None
            self.dpkg_myoffice_remove()
            if not self.exit_code:
                txt = "Удаление программы myoffice-standard-home-edition выполнено успешно!\n"
            elif self.exit_code:
                txt = "Ошибка при удалении программы myoffice-standard-home-edition\n"
            self.new_log.emit(txt)
            self.progress.emit(100)

    def parsing_site(self):
        link_f = None
        dn_http = "https://myoffice.ru/products/standard-home-edition/"
        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
        headers = {"user agent": user_agent}
        urllib3.disable_warnings()
        html = requests.get(dn_http, headers)

        soup = BeautifulSoup(html.content, "html.parser")

        links = soup.find(class_="operant-modal").find_all("a")
        for j in links:
            link_parser = j.get("href")
            if link_parser[-4:] == '.deb':
                link_f = link_parser

        print("Ссылка для скачивания: ", link_f)
        self.new_log.emit("Ссылка для скачивания: " + link_f)

        return link_f

    def download_package(self):
        self.new_log.emit("\nСкачиваем пакет!\n")
        sleep(2)
        t = threading.Thread(target=self.run_down, name='Thread1')
        t.start()
        sleep(1)
        self.run_read()
        t.join()

    # Запуск процесса скачивания
    def run_down(self):
        process = subprocess.Popen("wget -P /tmp/ --no-check-certificate --output-file=/tmp/test.txt " + self.link_download,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.communicate()
        self.return_code_download = process.returncode

    # Чтение фала лога загрузки
    def run_read(self):
        file_path = "/tmp/test.txt"
        s = 0
        with open(file_path, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    s += 1
                    time.sleep(0.1)
                    if s > 5:
                        f.close()
                        break
                else:
                    s = 0
                self.new_log.emit(line)

    # Установка deb пакета
    def dpkg_myoffice_install(self):
        package_name = self.link_download.split("/")[-1]
        process = subprocess.Popen("sudo dpkg -i /tmp/%s" % package_name,
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
        sleep(0.2)
        os.remove("/tmp/" + package_name)
        return process.returncode

    def dpkg_myoffice_remove(self):
        process = subprocess.Popen("sudo dpkg --purge myoffice-standard-home-edition",
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


# Установка пакета snapd
class SetupSnapd(QtCore.QThread):
    count = 0
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, act=None):
        super().__init__()
        self.act = act

    def change_progress_new_log(self, txt=None):
        self.count += 1
        if txt:
            self.new_log.emit(txt)
        self.progress.emit(self.count)
        sleep(1)

    def run(self):
        if self.act == "install":
            txt = 'Функция не поддерживается'
            self.change_progress_new_log(txt=txt)
            self.progress.emit(100)
        elif self.act == "remove":
            txt = "Будет выполнено удаление пакета snapd"
            self.change_progress_new_log(txt=txt)
            for j in range(2):
                list_package = self.list_package_for_remove()
                self.change_progress_new_log()
                self.uninstall_snapd(list_pack=list_package)
                self.change_progress_new_log()

            self.clear_snap()

            error = self.disable_returninstall_snapd()
            list_package = self.list_package_for_remove()

            if not list_package and not error:
                txt = "\nПакет snapd полностью удален из системы"
            else:
                txt = "\nПакет snapd удалён частично! Попробуйте удалить ещё раз"
            self.change_progress_new_log(txt=txt)
            self.progress.emit(100)

    @staticmethod
    def list_package_for_remove():
        command = "snap list | awk '/1./{print $1}'"
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        list_package = proc.stdout.readlines()
        return list_package

    def uninstall_snapd(self, list_pack=None):
        if list_pack:
            for package in list_pack:
                command = 'sudo snap remove --purge ' + str(package.decode('utf-8'))
                self.change_progress_new_log(txt='\nУдаляем пакет ' + str(package.decode('utf-8')))
                txt = self.run_command(command=command)
                self.change_progress_new_log(txt=txt)

    def clear_snap(self):
        self.change_progress_new_log(txt='\nВычищаем оснастку Snap\n')
        command = 'sudo apt-get remove --purge --autoremove snapd gnome-software-plugin-snap -y'
        self.change_progress_new_log()
        txt = self.run_command(command=command)
        self.change_progress_new_log(txt=txt)

    def disable_returninstall_snapd(self):
        out_data = True
        txt = '\nОтключаем возможность повторной установки snapd\n'
        self.change_progress_new_log(txt=txt)
        file = '/tmp/nosnap.tmp'
        file_dest = "/etc/apt/preferences.d/nosnap.pref"
        txt = "Package: snapd\nPin: release a=*\nPin-Priority: -10\n"
        command = "sudo mv {} {}".format(file, file_dest)
        with open(file, 'w') as f:
            f.write(txt)
        self.run_command(command)

        if os.path.isfile(file_dest):
            out_data = False
            txt = None
        else:
            txt = "Ошибка!"
        self.change_progress_new_log(txt=txt)

        return out_data

    @staticmethod
    def run_command(command=None):
        proc = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()
        error = err.decode('utf-8').strip()
        if error:
            print('Ошибка:', error)
            txt = error
        else:
            txt = 'Удалено'
        return txt


# Установка FireFox
class SetupFirefox(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, act=None):
        super().__init__()
        self.act = act
        self.count = 0
        self.error = None

    def run(self):
        if self.act == "install":
            self.change_progress_new_log(txt="Установка FireFox\n")
            self.error = self.add_repo()  # Добавляем репозиторий
            if not self.error:
                self.change_progress_new_log(txt='Настраиваем высокий приоритет для deb пакета\n')
                self.error = self.add_apt_99mozillateamppa()
                if not self.error:
                    self.change_progress_new_log(txt='Устанавливаем firefox\n')
                    self.error = self.apt_firefox(act='install')
        elif self.act == "remove":
            self.change_progress_new_log(txt='Удаляем firefox\n')
            self.error = self.apt_firefox(act='purge')

        if not self.error:
            txt = 'Успех!'
        else:
            txt = "Ошибка"
        self.change_progress_new_log(txt=txt, pause=2)
        self.progress.emit(100)

    def add_repo(self):
        self.change_progress_new_log(txt="Добавляем репозиторий!\n")
        command = 'sudo add-apt-repository ppa:mozillateam/ppa -y'
        return_code = self.run_process_view_data(command)
        return return_code

    def add_apt_99mozillateamppa(self):
        file_ppa_tmp = "/tmp/ppamozilla.tmp"
        file_destination = "/etc/apt/preferences.d/99mozillateamppa"
        txt = 'Package: firefox*\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 501\n' \
              '\nPackage: firefox*\nPin: release o=Ubuntu\nPin-Priority: -1\n'
        with open(file_ppa_tmp, 'w') as f:
            f.write(txt)
        command = 'sudo mv {} {}'.format(file_ppa_tmp, file_destination)
        return_code = self.run_process_view_data(command=command)
        return return_code

    def apt_firefox(self, act=None):
        if act:
            command = "sudo apt {} -t 'o=LP-PPA-mozillateam' firefox firefox-locale-ru -y".format(act)
            return_code = self.run_process_view_data(command=command)
            return return_code

    def change_progress_new_log(self, txt=None, pause=None):
        if not pause:
            pause = 1
        self.count += 1
        if txt:
            self.new_log.emit(txt)
        self.progress.emit(self.count)
        sleep(pause)

    def run_process_view_data(self, command=None):
        process = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        st = True
        while st:
            st = process.stdout.readline()
            self.change_progress_new_log(txt=str(st.decode('utf-8', 'ignore')), pause=0.1)
            print(st.decode("utf-8"), end="")
            sleep(0.01)
        process.communicate()
        sleep(0.2)
        return process.returncode


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


# Функция замены строки
def change_string(file=None, old_str=None, new_str=None):
    tmp_file = "/tmp/trusted.tmp"
    ln_str = ''.join(old_str.split())
    with open(tmp_file, 'w') as f1:
        with open(file, 'r') as f:
            for line in f:
                ln = ''.join(line.split())
                if ln_str == ln:
                    f1.writelines(new_str + '\n')
                else:
                    f1.writelines(line)


# Функция поиска строки в файле
def find_string(file=None, string=None):
    exit_code = -1
    string = ''.join(string.split())
    with open(file, 'r') as f:
        for line in f:
            ln = ''.join(line.split())
            if ln == string:
                exit_code = 0
    return exit_code


class DebugWin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.dg = Ui_Form()  # Инициализация окна Debug
        self.dg.setupUi(self)
        self.dg.pushButton.setEnabled(False)
        self.dg.pushButton_2.setEnabled(False)
        # Создание иконки программы
        logo = os.path.join(sys.path[0] + "/resources/ico/", "debug.svg")
        icon = QtGui.QIcon()
        print(logo)
        icon.addPixmap(QtGui.QPixmap(logo))
        self.setWindowIcon(icon)
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


class SshDesktopVncWin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ip_remote_comp = None
        self.name_login_user = None
        self.vncaddrbook = False
        self.vncviewer = False
        self.b3 = Ui_SshDesktopVnc()
        self.b3.setupUi(self)
        self.b3.pushButton.setDisabled(True)
        self.b3.pushButton.clicked.connect(self.act)
        self.b3.checkBox.clicked.connect(self.clck_check)
        self.b3.checkBox_2.clicked.connect(self.clck_check)

    def act(self):
        if self.b3.checkBox.isChecked():
            self.vncaddrbook = True
        elif not self.b3.checkBox.isChecked():
            self.vncaddrbook = False
        if self.b3.checkBox_2.isChecked():
            self.vncviewer = True
        elif not self.b3.checkBox_2.isChecked():
            self.vncviewer = False
        self.conversion_ip()
        self.name_login_user = self.b3.lineEdit_2.text()
        self.close()

    def clck_check(self):
        if self.b3.checkBox.isChecked() or self.b3.checkBox_2.isChecked():
            self.b3.pushButton.setEnabled(True)
        elif not self.b3.checkBox.isChecked() and not self.b3.checkBox_2.isChecked():
            self.b3.pushButton.setDisabled(True)

    # Преобразование ip адреса
    def conversion_ip(self):
        list1 = self.b3.lineEdit.text().split(".")
        list2 = []
        for i in list1:
            list2.append(str(int(i)))
        self.ip_remote_comp = '.'.join(list2)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    a = Programs('"AstraLinuxSE" 1.6')
    a.stateProg()
    a.actionProg(os_ver='"AstraLinuxSE" 1.6', action="install", lst_name_prog=["timeshift"])
    sys.exit(app.exec_())
