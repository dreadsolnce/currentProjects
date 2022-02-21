#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
from time import sleep
import threading
from .Debug import Ui_Form
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog
from PyQt5 import QtGui, QtWidgets, QtCore


def runCommandReturnListOut(command):
    list_out = []
    proc = subprocess.Popen(command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=open("/dev/null", "w"))
    s = proc.stdout.readline()
    while s:
        list_out.append(s.decode('utf-8'))
        s = proc.stdout.readline()

    return list_out


def runProcessReturnOutErrCode(command):
    process = subprocess.Popen(command, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("utf-8"), err.decode("utf-8"), process.returncode


def changeFile(file=None, template=None, new_str=None):
    file_tmp = "/tmp/temp.tmp"
    with open(file_tmp, 'w') as ft:
        with open(file, 'r') as f:
            for line in f:
                # if " ".join(line.split()) == " ".join(template.split()):
                if " ".join(template.split()) in " ".join(line.split()):
                    ft.writelines(new_str + '\n')
                else:
                    ft.writelines(line)
    command = "sudo mv -f {} '{}'".format(file_tmp, file)
    out = runProcessReturnOutErrCode(command)
    return out[2]


def findTemplateFile(file=None, template=None):
    with open(file, 'r') as f:
        for line in f:
            # if " ".join(line.split()) == " ".join(template.split()):
            if " ".join(template.split()) in " ".join(line.split()):
                return True
    return False


# Удаление пыстых строк из файла
def deleteNullStringFile(file):
    file_tmp = "/tmp/temp.tmp"
    with open(file, 'r') as fr, open(file_tmp, 'w') as fw:
        for line in fr:
            if line.strip():
                fw.write(line)
    command = "sudo mv -f '{}' '{}'".format(file_tmp, file)
    out = runProcessReturnOutErrCode(command)
    return out[2]


class PxeModule(object):
    def __init__(self, os_ver=None, os_debian=None, os_astra=None, name_ui=None, obj_win=None):
        super().__init__()
        self.os_ver = os_ver
        self.os_debian = os_debian
        self.os_astra = os_astra
        self.name_ui = name_ui
        self.obj_win = obj_win

        self.file_start_pxe = "/usr/local/bin/StartPXE.py"
        self.name_package_qemu = "qemu-system-x86"

        self.currentState()
        self.__viewEthernet()

    # Текущий состояние установки программы
    def currentState(self):
        if os.path.isfile(self.file_start_pxe):
            self.name_ui.label_pxe_state.setText("Состояние:\tУстановлен")
        else:
            self.name_ui.label_pxe_state.setText("Состояние:\tОтсутствует")

    def clickCheckBox(self):
        bool_state = None
        if self.name_ui.checkBox_pxe_change.isChecked():
            bool_state = True
        elif not self.name_ui.checkBox_pxe_change.isChecked():
            bool_state = False
            self.name_ui.pushButton_pxe_apply.setEnabled(bool_state)

        self.name_ui.radioButton_ins.setEnabled(bool_state)
        self.name_ui.radioButton_del.setEnabled(bool_state)
        self.name_ui.label_pxe_state.setDisabled(bool_state)

        if self.name_ui.radioButton_ins.isChecked() and self.name_ui.checkBox_pxe_change.isChecked():
            bool_state = True
            self.name_ui.pushButton_pxe_apply.setEnabled(True)
        elif self.name_ui.radioButton_del.isChecked() and self.name_ui.checkBox_pxe_change.isChecked():
            self.name_ui.pushButton_pxe_apply.setEnabled(True)
            bool_state = False
        elif not self.name_ui.checkBox_pxe_change.isChecked():
            bool_state = False
        self.__stateElementsGuiPXE(bool_state=bool_state)

    def clickRadioButton(self):
        bool_state = False
        if self.name_ui.radioButton_ins.isChecked():
            bool_state = True
            self.name_ui.pushButton_pxe_apply.setEnabled(True)
        elif self.name_ui.radioButton_del.isChecked():
            bool_state = False
            self.name_ui.pushButton_pxe_apply.setEnabled(True)
        else:
            self.name_ui.pushButton_pxe_apply.setEnabled(False)
        self.__stateElementsGuiPXE(bool_state=bool_state)

    #  Нажата кнопка выбора файла
    def clickPushButtonPath(self):
        file_pxe = QFileDialog.getOpenFileName(self.obj_win, 'Open file', '/home/kvl')[0]
        self.name_ui.lineEdit_pxe_path.setText(file_pxe)

    # Надажата кнопка применть
    def clickPushButtonApply(self):
        act = None
        if self.name_ui.radioButton_ins.isChecked():
            act = "install"
        elif self.name_ui.radioButton_del.isChecked():
            act = "remove"
        self.__runProcessAction(act=act)
        self.currentState()

    #  В зависимости от выбранных чекбоксов изменяем сотояние графических элементов
    def __stateElementsGuiPXE(self, bool_state=False):
        self.name_ui.label_pxe_eth.setEnabled(bool_state)
        self.name_ui.comboBox_pxe_eth.setEnabled(bool_state)
        self.name_ui.label_pxe_auto.setEnabled(bool_state)
        self.name_ui.checkBox_pxe_auto.setEnabled(bool_state)
        self.name_ui.label_pxe_desktop.setEnabled(bool_state)
        self.name_ui.checkBox_pxe_desktop.setEnabled(bool_state)
        self.name_ui.label_pxe_eth.setEnabled(bool_state)
        self.name_ui.pushButton_pxe_path.setEnabled(bool_state)
        self.name_ui.label_pxe_path.setEnabled(bool_state)
        self.name_ui.lineEdit_pxe_path.setEnabled(bool_state)

    #  Формируем список с именами сетевых интерфейсов и передаем выполнение функции заполняющий combobox
    def __viewEthernet(self):
        list_eth = runCommandReturnListOut("ip -o link show | awk '{print $2}' | awk -F: '{print $1}'")
        self.__addComboboxEth(list_eth)

    # Заполняем сетевыми именами combobox
    def __addComboboxEth(self, list_eth):
        i = 0
        for j in list_eth:
            self.name_ui.comboBox_pxe_eth.addItem(None)
            self.name_ui.comboBox_pxe_eth.setItemText(i, j.strip())
            i += 1

    # Запуск процесса установки или удаления
    def __runProcessAction(self, act=None):
        if act == "install":
            self.__getAttrPxe()
            e = self.checkQemuSystem()
            if not e:
                if self.file_pxe:
                    err = False
                    while not err:
                        err = self.__copyQemuEthernet()
                        if err:
                            break
                        err = self.__copyStartPXE()
                        if err:
                            break
                        if self.autostart_pxe == "enable":
                            err = self.__autoStartPXE()
                            if err:
                                break
                        if self.desktop_pxe == "enable":
                            err = self.__copyDesktopPXE()
                            if err:
                                break
                        QMessageBox.information(self.obj_win, "Информация!", "Установка программы для запуска PXE сервера выполнена успешно!")
                        err = True
        elif act == "remove":
            err = False
            # t = Qemu(os_ver=self.os_ver)
            while not err:
                err = self.__delFileQemu()
                if err:
                    break
                err = self.__deleteAutostart()
                if err:
                    break
                QMessageBox.information(self.obj_win, "Информация!", "Удаление выполнено успешно!")
                err = True

    # Получаем параметры PXE сервера
    def __getAttrPxe(self):
        self.file_pxe = None
        self.eth_pxe = self.name_ui.comboBox_pxe_eth.currentText()
        if self.name_ui.checkBox_pxe_auto.isChecked():
            self.autostart_pxe = "enable"
        elif not self.name_ui.checkBox_pxe_auto.isChecked():
            self.autostart_pxe = "disable"
        if self.name_ui.checkBox_pxe_desktop.isChecked():
            self.desktop_pxe = "enable"
        elif not self.name_ui.checkBox_pxe_desktop.isChecked():
            self.desktop_pxe = "disable"
        if os.path.isfile(self.name_ui.lineEdit_pxe_path.text()):
            self.file_pxe = self.name_ui.lineEdit_pxe_path.text()
        else:
            QMessageBox.critical(self.obj_win, "Ошибка!", "Не правильно указан путь к файлу!")

    # Копирование файлов сети
    def __copyQemuEthernet(self):
        command = "sudo cp " + sys.path[0] + "/files/pxe/qemu-if* /etc/"
        out = runProcessReturnOutErrCode(command)
        if out[2]:
            QMessageBox.critical(self.obj_win, "Ошибка", "Ошибка копирования файлов qemu-if*.PNOSKO в /etc/")
        return out[2]

    # Копирование исполняемого файла
    def __copyStartPXE(self):
        command = "sudo cp " + sys.path[0] + "/files/pxe/StartPXE.py /usr/local/bin/StartPXE.py"
        out = runProcessReturnOutErrCode(command)
        if out[2]:
            QMessageBox.critical(self.obj_win, "Ошибка", "Ошибка копирования StartPXE.py в /usr/local/bin")
        return out[2]

    # Добавление в автозагрузку через файл .xsessionrc
    def __autoStartPXE(self):
        err = 0
        file_autostart = "/home/" + os.getlogin() + "/.xsessionrc"
        file_autostart_bak = "/home/" + os.getlogin() + "/.xsessionrc.PNOSKO.bak"
        template = "/usr/local/bin/StartPXE.py"
        new_str = "exec /usr/local/bin/StartPXE.py " + self.eth_pxe + " '" + self.file_pxe + "' &"

        # Делаем копию файла, если еще не сделана
        if os.path.isfile(file_autostart) and not os.path.isfile(file_autostart_bak):
            shutil.copyfile(file_autostart, file_autostart_bak)

        # Создаем новый файл .xsessionrc если его нет
        if not os.path.isfile(file_autostart):
            with open(file_autostart, 'w') as f:
                f.writelines(new_str + "\n")

        # Файл .xsessionrc присутствует
        elif os.path.isfile(file_autostart):
            if findTemplateFile(file_autostart, template):
                err = changeFile(file_autostart, template, new_str)
                if err:
                    QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка замены строки в файле .xsessionrc")
            else:
                try:
                    # deleteNullStringFile(file_autostart)
                    with open(file_autostart, "a") as f:
                        f.writelines("\n" + new_str + "\n")
                    deleteNullStringFile(file_autostart)
                except PermissionError as e:
                    QMessageBox.critical(self.obj_win, "Ошибка!", str(e))
                    err = 1
        return err

    # Копирование ярлыка программы на рабочий стол
    def __copyDesktopPXE(self):
        err = 0
        # Копирование иконки программы
        dir_ico = "/home/" + os.getlogin() + "/.local/share/icons"
        file_ico = sys.path[0] + "/files/pxe/qemu_start.png"
        file_desktop_pxe = sys.path[0] + "/files/pxe/start_pxe.desktop"
        file_desktop_os = "/home/" + os.getlogin() + "/Desktop/start_pxe.desktop"
        if os.path.isdir("/home/" + os.getlogin() + "/Рабочий стол"):
            file_desktop_os = "/home/" + os.getlogin() + "/Рабочий стол/start_pxe.desktop"

        try:
            if not os.path.isdir(dir_ico):
                os.mkdir(dir_ico)
            shutil.copyfile(file_ico, dir_ico + "/qemu_start.png")
        except PermissionError as e:
            QMessageBox.critical(self.obj_win, "Ошибка", str(e))
            err = 1
        except FileNotFoundError as e:
            QMessageBox.critical(self.obj_win, "Ошибка", str(e))
            err = 1

        # Копируем ярлык
        if not os.path.isfile(file_desktop_os):
            try:
                shutil.copyfile(file_desktop_pxe, file_desktop_os)
            except PermissionError as e:
                QMessageBox.critical(self.obj_win, "Ошибка", str(e))
                err = 1
            except FileNotFoundError as e:
                QMessageBox.critical(self.obj_win, "Ошибка", str(e))
                err = 1
        if not err:
            err = changeFile(file_desktop_os, "Exec=", "Exec=/usr/local/bin/StartPXE.py " + self.eth_pxe + " '" + self.file_pxe + "'")
            if err:
                QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка изменения файла рабочего стола!")
        return err

    #  Удаляем файлы от Qemu
    def __delFileQemu(self):
        file_desktop_os = "/home/" + os.getlogin() + "/Desktop/start_pxe.desktop"
        if os.path.isdir("/home/" + os.getlogin() + "/Рабочий стол"):
            file_desktop_os = "/home/" + os.getlogin() + "/Рабочий стол/start_pxe.desktop"

        files = ["/etc/qemu-ifup.PNOSKO /etc/qemu-ifup.PNOSKO",
                 "/etc/qemu-ifup.PNOSKO /etc/qemu-ifdown.PNOSKO",
                 "/usr/local/bin/StartPXE.py", file_desktop_os
                 ]

        command = "sudo rm -rf '{}' '{}' '{}' '{}'".format(files[0], files[1], files[2], files[3])
        e = runProcessReturnOutErrCode(command)
        if e[2]:
            QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка удаления файлов от PXE!")
        return e[2]

    # Удаление из автозагрузки
    def __deleteAutostart(self):
        err = 0
        file_autostart = "/home/" + os.getlogin() + "/.xsessionrc"
        file_autostart_bak = "/home/" + os.getlogin() + "/.xsessionrc.PNOSKO.bak"
        template = "/usr/local/bin/StartPXE.py"
        # Делаем копию файла, если еще не сделана
        if os.path.isfile(file_autostart) and not os.path.isfile(file_autostart_bak):
            shutil.copyfile(file_autostart, file_autostart_bak)

        if os.path.isfile(file_autostart):
            if findTemplateFile(file_autostart, template):
                err = changeFile(file_autostart, template, "")
                deleteNullStringFile(file_autostart)
                if err:
                    QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка отключения из автозагрузки!")
        return err

    # Проверка установлен ли пакет qemu-system-x86_64 в системе
    def checkQemuSystem(self):
        command = "dpkg-query -L '{}'".format(self.name_package_qemu)
        e = runProcessReturnOutErrCode(command)
        if e[2]:
            text_err = "Не найден пакет qemu-system-x86_64.\nУстановите его из меню программы\nЛокальная настройка > Основные параметры"
            QMessageBox.critical(self.obj_win, "Ошибка", text_err)
        return e[2]

# class Qemu(object):
#     def __init__(self, os_ver=None, os_debian=None, os_astra=None, obj_win=None):
#         super().__init__()
#         self.os_ver = os_ver
#         self.os_debian = os_debian
#         self.os_astra = os_astra
#         self.obj_win = obj_win
#         self.name_os = None
#         self.dg_gui = None
#         self.name_package = "qemu-system-x86"
#         self.full_path_lib = None
#         self.checkQemuPackage()
#
#     def checkQemuPackage(self):
#         command = "dpkg-query -L '{}'".format(self.name_package)
#         e = runProcessReturnOutErrCode(command)
#         if e[2]:
#             print("Пакет qemu-system-x86_64 не установлен!")
#             self.install()
#         else:
#             print("Пакет qemu-system-x86_64 установлен!")
#
#     def install(self):
#         self.dg_gui = DebugWin()
#         if self.os_ver in self.os_debian:
#             print("Установка библиотек qemu для Ubuntu")
#             self.name_os = "Ubuntu"
#             self.runProcessTH()
#         elif self.os_ver in self.os_astra:
#             print("Установка библиотек qemu для Astra Linux")
#             self.name_os = "Astra"
# #         self.dg_gui = DebugWin()
# #         if self.os_ver == '"AstraLinuxSE" 1.6':
# #             # list_lib = ["libibverbs1", "ibverbs-providers", "ipxe-qemu", "libaio1", "libbrlapi0.6", "libcacard0", "libcapstone4", "libpmem1",
# #             #             "librdmacm1", "libslirp0", "libspice-server1", "libusbredirparser1", "libvdeplug2", "libvirglrenderer0", "ovmf",
# #             #             "qemu-system-common", "qemu-system-data", "qemu-utils", "seabios"]
#             list_lib = ["libibverbs1", "ibverbs-providers"]
#             for i in list_lib:
#                 self.full_path_lib = sys.path[0] + '/files/lib/qemu/' + i + '*'
#                 self.runProcessTH()
#         self.debugButtonAct()
#
#     def debugButtonAct(self):
#         self.dg_gui.dg.pushButton.setEnabled(True)
#         self.dg_gui.dg.pushButton_2.setEnabled(True)
#         self.dg_gui.dg.pushButton_2.clicked.connect(self.saveLogFile)
#         self.dg_gui.dg.pushButton.clicked.connect(lambda: self.dg_gui.close())
#
#     def saveLogFile(self):
#         print("Сохранить лог в файл...")
#         file_log = QtWidgets.QFileDialog.getSaveFileName(self.obj_win, 'Save file', "/")[0]
#         print(file_log)
#         if file_log:
#             with open(file_log, 'w') as f:
#                 text = self.dg_gui.dg.textDebug.toPlainText()
#                 f.write(text)
#             f.close()
#
#     def runProcessTH(self):
#         process_th = InstallLib(name_os=self.name_os, lib=self.full_path_lib)
#         process_th.new_log.connect(self.dg_gui.dg.textDebug.insertPlainText)
#         process_th.progress.connect(self.dg_gui.dg.progressBar.setValue)
#         process_th.start()
#         while process_th.isRunning():
#             QtCore.QCoreApplication.processEvents()
#             QtCore.QThread.msleep(150)
#             self.dg_gui.dg.textDebug.moveCursor(QtGui.QTextCursor.EndOfBlock)
#         process_th.quit()
#
#
# class InstallLib(QtCore.QThread):
#     new_log = QtCore.pyqtSignal(str)
#     progress = QtCore.pyqtSignal(int)
#
#     def __init__(self, name_os=None, lib=None):
#         super().__init__()
#         self.full_path_for_lib = lib
#         self.name_os = name_os
#         self.count = 0
#
#     def run(self):
#         command = None
#         if self.name_os == "Ubuntu":
#           command = "sudo apt-get install qemu-system-x86 -y"
#         process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
#                                    stderr=subprocess.PIPE)
#         st = True
#         while st:
#             st = process.stdout.readline()
#             self.count += 1
#             self.new_log.emit(str(st.decode('utf-8', 'ignore')))
#             self.progress.emit(self.count)
#             sleep(0.01)
#         process.communicate()
#         # self.progress.emit(100)
#         sleep(0.2)
# #         text_command_1 = ""
# #         text_command_2 = ""
# #         if self.os_ver == '"AstraLinuxSE" 1.6':
# #             text_command_1 = "sudo dpkg -i "
# #             text_command_2 = " ; sudo apt-get install -f -y"
# #         process = subprocess.Popen(text_command_1 + self.full_path_for_lib + text_command_2, shell=True,
# #                                    stdout=subprocess.PIPE,
# #                                    stderr=subprocess.PIPE)
# #         st = True
# #         while st:
# #             st = process.stdout.readline()
# #             # self.count += 1
# #             self.new_log.emit(str(st.decode('utf-8', 'ignore')))
# #             # self.progress.emit(self.count)
# #             print(st.decode("utf-8"), end="")
# #             sleep(0.01)
# #         process.communicate()
# #         # self.exit_code = self.exit_code + process.returncode
# #         sleep(0.2)
# #
# #
# class DebugWin(QtWidgets.QDialog):
#     def __init__(self):
#         super().__init__()
#         self.dg = Ui_Form()  # Инициализация окна Debug
#         self.dg.setupUi(self)
#         self.dg.pushButton.setEnabled(False)
#         self.dg.pushButton_2.setEnabled(False)
#         # Создание иконки программы
#         logo = os.path.join(sys.path[0] + "/resources/ico/", "debug.svg")
#         icon = QtGui.QIcon()
#         print(logo)
#         icon.addPixmap(QtGui.QPixmap(logo))
#         self.setWindowIcon(icon)
#         self.show()
