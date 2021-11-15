#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui
from .Debug import Ui_Form
from time import sleep


class InstallProg(QtWidgets.QDialog, Ui_Form):
    def __init__(self, os_ver):
        super().__init__()
        self.os_ver = os_ver
        self.setupUi(self)

    def installProg(self, action=None, name_program_list=None):
        self.show()
        command = None

        for name_program in name_program_list:
            if self.os_ver == "Ubuntu 21.04":
                if name_program == "игры":
                    name_program = "aisleriot gnome-mahjongg gnome-mines gnome-sudoku"
                elif name_program == "pyqt5-dev-tools":
                    name_program = "python3-pyqt5 qtcreator pyqt5-dev-tools qttools5-dev-tools"

                if action == "install":
                    if name_program == "pycharm-community":
                        command = "sudo snap install pycharm-community --classic"
                    else:
                        command = "sudo apt-get install {} -y".format(name_program)
                elif action == "remove":
                    if name_program == "pyqt5-dev-tools":
                        name_program = "qtcreator pyqt5-dev-tools qttools5-dev-tools"
                    if name_program == "pycharm-community":
                        command = "sudo snap remove pycharm-community"
                    else:
                        command = "sudo apt-get purge {} -y".format(name_program)

            elif self.os_ver == "AstraLinuxSE 1.6":
                if name_program == "timeshift":
                    print("Установка прогрв=аммы timeshift")
            t = ActionProgramOutputData(command)
            t.new_log.connect(self.textDebug.insertPlainText)
            t.progress.connect(self.progressBar.setValue)
            t.start()
            while t.isRunning():
                QtCore.QCoreApplication.processEvents()
                QtCore.QThread.msleep(150)
                self.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
            t.quit()
        self.pushButton.setEnabled(True)
        self.pushButton.clicked.connect(lambda: self.clickPushButtonClose())

    def clickPushButtonClose(self):
        print("Закрываем окно")
        self.close()


class ActionProgramOutputData(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.count = 0

    def run(self):
        print(self.command)
        proc = subprocess.Popen(self.command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        st = proc.stdout.readline()
        # count = 0
        while st:
            st = proc.stdout.readline()
            self.new_log.emit(st.decode('utf-8', 'ignore'))
            self.progress.emit(self.count)
            print(st.decode("utf-8"), end="")
            self.count += 1
            sleep(0.01)
        self.progress.emit(100)
