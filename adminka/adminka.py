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
pxe_picture = os.path.join(sys.path[0] + "/resources/ico/", "PXE-Logo.png")
print("Иконка программы: {}".format(logo))


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.name_debian = ["Ubuntu 21.04", "Ubuntu 21.10"]  # Список поддерживаемых ОС семейства Ubuntu
        self.name_astra = ['"AstraLinuxSE" 1.6']  # Список поддерживаемы ОС семейства AstraLinux

        self.os_ver = resources.OsVersion()  # Версия ОС

        self.pm = None  # Объект resources.ProgramsModule
        self.msm = None  # Объект resources.MainSettingsModule
        self.csnh = None  # Объект resources.ChangeSettingsNameHost
        self.cse = None  # Объект resources.ChangeSettingsEthernet
        self.pxem = None  # Объект resources.MainPxeModule

        self.gui = resources.Ui_MainWindow()
        self.main_settings = resources.Ui_MainSettingsWindow()
        self.main_change_settings = resources.Ui_MainChangeSettingsWindow()
        self.main_pxe = resources.Ui_MainPxeWindow()
        self.remote_settings = resources.Ui_RemoteSettingsWindow()

        self.width = 1300
        self.height = 600

        self.checkCurrentOs()
        self.mainWin()
        self.winCenter()

    #  Проверка соответствия текущей ОС со списком поддерживаемых ОС
    def checkCurrentOs(self):
        if self.os_ver not in self.name_debian + self.name_astra:
            QMessageBox.critical(self, "Ошибка!", "Не поддерживаемая версия ОС", QMessageBox.Ok)
            sys.exit()

    def mainWin(self):
        self.gui.setupUi(self, self.width, self.height)

        # Создание иконки программы
        self.setIcon()

        self.show()
        self.actionMainWindow()

    # Создание иконки окна
    def setIcon(self):
        # Создание иконки программы
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(logo))
        self.setWindowIcon(icon)

    def actionMainWindow(self):
        self.gui.action_MainSettings.triggered.connect(self.MenuMainSettingsWindows)
        self.gui.action_ChangeSettings.triggered.connect(self.MenuMainChangeSettingsWindows)
        self.gui.action_PXE.triggered.connect(self.MenuPxeWindows)
        self.gui.action_OpenRemoteSettings.triggered.connect(self.MenuRemoteSettingsWindows)
        self.gui.action_Exit.triggered.connect(lambda: sys.exit())

    def MenuMainSettingsWindows(self):
        print("Выбрано меню Локальная настройка > Основные параметры")
        self.main_settings.setupUi(self, self.width, self.height)
        self.setIcon()

        if self.os_ver in self.name_debian:
            self.main_settings.frame_3.setEnabled(False)    # Отключаем не задействованные элементы меню.
            self.main_settings.frame_remote_session.setEnabled(False)

        self.pm = resources.ProgramsModule(os_ver=self.os_ver,
                                           os_debian=self.name_debian, os_astra=self.name_astra,
                                           name_ui=self.main_settings, obj_win=self)
        self.msm = resources.MainSettingsModule(os_ver=self.os_ver,
                                                os_debian=self.name_debian, os_astra=self.name_astra,
                                                name_ui=self.main_settings, obj_win=self)

        self.actionMenuMainSettingsWindows()

    def actionMenuMainSettingsWindows(self):
        self.main_settings.checkBox_autologin.clicked.connect(self.msm.clickAutologinCheckBox)
        self.main_settings.checkBox_networkmanager.clicked.connect(self.msm.clickNetworkManagerCheckBox)
        self.main_settings.checkBox_root.clicked.connect(self.msm.clickSetRootUser)
        self.main_settings.checkBox_ssh.clicked.connect(self.msm.clickSetSSH)
        self.main_settings.checkBox_time.clicked.connect(self.msm.clickSetTimeMode)
        self.main_settings.checkBox_remote_session.clicked.connect(self.msm.clickSetRemoteSession)
        self.main_settings.checkBox_resolv.clicked.connect(self.msm.clickSetResolv)
        self.main_settings.pushButton_apply.clicked.connect(self.msm.clickPushbuttonApply)
        self.main_settings.checkBox_all.clicked.connect(self.pm.clkCheckbox)
        self.main_settings.pushButton_insprog.clicked.connect(lambda: self.pm.clkPushButtonProgram(action="install"))
        self.main_settings.pushButton_delprog.clicked.connect(lambda: self.pm.clkPushButtonProgram(action="remove"))

        # self.main_settings.label_autologin.setFont(QtGui.QBrush(Qt.darkGreen)

        self.main_settings.action_ChangeSettings.triggered.connect(self.MenuMainChangeSettingsWindows)
        self.main_settings.action_PXE.triggered.connect(self.MenuPxeWindows)
        self.main_settings.action_OpenRemoteSettings.triggered.connect(self.MenuRemoteSettingsWindows)
        self.main_settings.action_Exit.triggered.connect(lambda: sys.exit())

    def MenuPxeWindows(self):
        print("Выбрано меню Локальная настройка > Настройка PXE сервера")
        self.main_pxe.setupUi(self, self.width, self.height)
        self.setIcon()
        self.main_pxe.label_pxe_picture.setPixmap(QtGui.QPixmap(pxe_picture))

        self.pxem = resources.PxeModule(os_ver=self.os_ver,
                                        os_debian=self.name_debian, os_astra=self.name_astra,
                                        name_ui=self.main_pxe, obj_win=self)

        self.actionMenuPXE()

    def actionMenuPXE(self):
        self.main_pxe.checkBox_pxe_change.clicked.connect(self.pxem.clickCheckBox)
        self.main_pxe.radioButton_ins.clicked.connect(self.pxem.clickRadioButton)
        self.main_pxe.radioButton_del.clicked.connect(self.pxem.clickRadioButton)
        self.main_pxe.pushButton_pxe_path.clicked.connect(self.pxem.clickPushButtonPath)
        self.main_pxe.pushButton_pxe_apply.clicked.connect(self.pxem.clickPushButtonApply)

        self.main_pxe.action_MainSettings.triggered.connect(self.MenuMainSettingsWindows)
        self.main_pxe.action_ChangeSettings.triggered.connect(self.MenuMainChangeSettingsWindows)
        self.main_pxe.action_OpenRemoteSettings.triggered.connect(self.MenuRemoteSettingsWindows)
        self.main_pxe.action_Exit.triggered.connect(lambda: sys.exit())

    def MenuRemoteSettingsWindows(self):
        print("Выбрано меню Удалённая настройка > Открыть")
        self.remote_settings.setupUi(self, self.width, self.height)
        self.setIcon()
        self.actionMenuRemoteSettingsWindows()

    def actionMenuRemoteSettingsWindows(self):
        self.remote_settings.action_MainSettings.triggered.connect(self.MenuMainSettingsWindows)
        self.remote_settings.action_ChangeSettings.triggered.connect(self.MenuMainChangeSettingsWindows)
        self.remote_settings.action_PXE.triggered.connect(self.MenuPxeWindows)
        self.remote_settings.action_Exit.triggered.connect(lambda: sys.exit())

    def MenuMainChangeSettingsWindows(self):
        print("Выбрано меню Локальная настройка > Настраиваемые параметры ОС")
        self.main_change_settings.setupUi(self, self.width, self.height)
        self.setIcon()

        self.csnh = resources.ChangeSettingsNameHost(name_ui=self.main_change_settings, obj_win=self)
        self.cse = resources.ChangeSettingsEthernet(name_ui=self.main_change_settings, obj_win=self)

        self.actionMenuMainChangeSettingsWindows()

    def actionMenuMainChangeSettingsWindows(self):
        # Отключение выделения текста в строке текущего имени хоста
        self.main_change_settings.lineEdit_currentname.selectionChanged.connect(self.csnh.disableSelection)
        self.main_change_settings.checkBox_change.clicked.connect(self.csnh.clickCheckboxChange)
        self.main_change_settings.pushButton_namehost_cancel.clicked.connect(self.csnh.clickPushbuttonCancel)
        self.main_change_settings.pushButton_namehost_apply.clicked.connect(self.csnh.clickPushbuttonApply)

        self.main_change_settings.action_MainSettings.triggered.connect(self.MenuMainSettingsWindows)
        self.main_change_settings.action_PXE.triggered.connect(self.MenuPxeWindows)
        self.main_change_settings.action_OpenRemoteSettings.triggered.connect(self.MenuRemoteSettingsWindows)
        self.main_change_settings.action_Exit.triggered.connect(lambda: sys.exit())

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
    list_lib = ['python3-six', 'python3-urllib3', 'python3-cffi-backend', 'python3-idna', 'python3-pkg-resources', 'python3-setuptools',
                'python3-pyasn1', 'python3-cryptography', 'python3-paramiko', 'python3-chardet', 'python3-requests', 'python3-bs4']
    os_ver = os_version()  # Версия ОС
    # Делаем общую проверку на наличие библиотек, если тест не проходит, то выполняем проверку по каждому элементу из списка
    ret = check_lib_all(list_lib)
    if ret[0] != '0':   # Проверка не пройдена, проверяем по каждому элементу (библиотеке)
        libs = []
        for i in list_lib:
            a1 = check_lib(i)
            if a1[0] != '0':
                if os_ver == '"AstraLinuxSE"':
                    libs.append(sys.path[0] + '/files/lib/python/' + i + '*')
                elif os_ver == "Ubuntu":
                    libs.append(i)
        t1 = threading.Thread(target=install_lib, name='Thread1', args=(libs, os_ver,))
        t1.start()
        t2 = TimerMessageBox()
        t2.exec_()
        t1.join()


# Обобщенная проверка на наличие необходимых библиотек
def check_lib_all(list_lib):
    command = "dpkg-query -L " + ' '.join(list_lib) + ' >/dev/null; echo $?'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("utf-8").split()


# Проверка зависимостей для запуска программы по каждому элементу из списка
def check_lib(name_lib):
    # name_lib - Имя пакета который необходим для работы программы
    # command = "dpkg --list | grep " + name_lib + " | awk '{print $2}' | grep -E ^" + name_lib + "$ >/dev/null; echo $?"
    command = "dpkg --list | grep " + name_lib + " | awk '{print $2}' | grep -E ^" + name_lib + " >/dev/null; echo $?"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("utf-8").split()


# Установка библиотек для запуска программы
def install_lib(name_lib, os_ver):
    text_command_1 = ""
    text_command_2 = ""
    if os_ver == "Ubuntu":
        text_command_1 = "sudo apt-get install -y "
        text_command_2 = ""
    elif os_ver == '"AstraLinuxSE"':
        text_command_1 = "sudo dpkg -i "
        text_command_2 = " ; sudo apt-get install -f"
    for i in name_lib:
        command = text_command_1 + i + text_command_2
        print(text_command_1 + i)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()


def os_version():
    command = "cat /etc/lsb-release | grep DISTRIB_ID | awk -F= '{print $2}'"
    proc = subprocess.Popen(command, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    st = proc.stdout.readline().decode("utf-8").strip()
    return st


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test_lib()
    import resources
    a = resources.CheckSudo()
    a2 = MainWindow()
    sys.exit(app.exec_())
