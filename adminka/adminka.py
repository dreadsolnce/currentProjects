#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import threading

from PyQt5 import QtWidgets, QtCore, QtGui
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
        self.os_ver = resources.OsVersion()  # Версия ОС
        self.pm = None  # Объект resources.ProgramsModule

        self.gui = resources.Ui_MainWindow()
        self.main_settings = resources.Ui_MainSettingsWindow()
        self.remote_settings = resources.Ui_RemoteSettingsWindow()

        self.width = 809
        self.height = 441

        self.mainWin()

    def mainWin(self):
        self.gui.setupUi(self, self.width, self.height)

        # Создание иконки программы
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(logo))
        self.setWindowIcon(icon)

        self.show()
        self.winCenter()
        self.actionMainWindow()

    def actionMainWindow(self):
        self.gui.action_MainSettings.triggered.connect(self.MenuMainSettingsWindows)
        self.gui.action_OpenRemoteSettings.triggered.connect(self.MenuRemoteSettingsWindows)
        self.gui.action_Exit.triggered.connect(lambda: sys.exit())

    def MenuMainSettingsWindows(self):
        print("Выбрано меню Локальная настройка > Основные параметры")
        self.main_settings.setupUi(self, self.width, self.height)
        self.main_settings.frame_1.setEnabled(False)    # Отключаем не задействованные элементы меню.

        self.pm = resources.ProgramsModule(os_ver=self.os_ver, name_ui=self.main_settings, obj_win=self)

        self.actionMenuMainSettingsWindows()

    def actionMenuMainSettingsWindows(self):
        self.main_settings.checkBox_all.clicked.connect(self.pm.clkCheckbox)
        self.main_settings.pushButton_insprog.clicked.connect(lambda: self.pm.clkPushButtonProgram(action="install"))
        self.main_settings.pushButton_delprog.clicked.connect(lambda: self.pm.clkPushButtonProgram(action="remove"))
        self.main_settings.action_Exit.triggered.connect(lambda: sys.exit())

        self.main_settings.action_OpenRemoteSettings.triggered.connect(self.MenuRemoteSettingsWindows)

    def MenuRemoteSettingsWindows(self):
        print("Выбрано меню Удалённая настройка > Открыть")
        self.remote_settings.setupUi(self, self.width, self.height)
        self.actionMenuRemoteSettingsWindows()

    def actionMenuRemoteSettingsWindows(self):
        self.remote_settings.action_MainSettings.triggered.connect(self.MenuMainSettingsWindows)
        self.remote_settings.action_Exit.triggered.connect(lambda: sys.exit())

    # Центрирование окна относительно экрана
    def winCenter(self):
        qr = self.frameGeometry()
        qp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(qp)
        self.move(qr.topLeft())

    # Событие при изменении размера окна
    def resizeEvent(self, event):
        self.width = self.size().width()
        self.height = self.size().height()


# Окно таймера
class TimerMessageBox(QMessageBox, threading.Thread):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("wait")
        self.time_to_wait = 0
        self.setText("wait (closing automatically) running in {0} second.".format(self.time_to_wait))
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.change_content)
        self.timer.start()

    def change_content(self):
        self.setText("wait (closing automatically) running in {0} second.".format(self.time_to_wait))
        self.time_to_wait += 1
        # if threading.activeCount() == 1:
        if threading.active_count() == 1:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


def test_lib():
    list_lib = ['python3-urllib3', 'python3-paramiko', 'python3-chardet', 'python3-requests', 'python3-bs4']
    for i in list_lib:
        a1 = check_lib(i)
        if a1[0] != '0':
            libs = sys.path[0] + '/files/lib/python3-*'
            t1 = threading.Thread(target=install_lib, name='Thread1', args=(libs,))
            t1.start()
            t2 = TimerMessageBox()
            t2.exec_()
            t1.join()


# Проверка зависимостей для запуска программы
def check_lib(name_lib):
    # name_lib - Имя пакета который необходим для работы программы
    command = "dpkg --list | grep " + name_lib + " | awk '{print $2}' | grep -E ^" + name_lib + "$ >/dev/null; echo $?"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("utf-8").split()


# Установка библиотек для запуска программы
def install_lib(name_lib):
    command = "sudo dpkg -i {}".format(name_lib)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    print(err.decode('utf-8'))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test_lib()
    import resources
    a = resources.CheckSudo()
    a2 = MainWindow()
    sys.exit(app.exec_())
