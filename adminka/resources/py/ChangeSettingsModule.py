#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import threading
from PyQt5.QtWidgets import QMessageBox, QComboBox, QTreeWidgetItem
from PyQt5 import QtCore


def runProcessReturnErrCode(command):
    process = subprocess.Popen(command, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("utf-8"), err.decode("utf-8"), process.returncode


class ChangeSettingsNameHost(object):
    def __init__(self, name_ui, obj_win):
        super().__init__()
        self.ret_code = None
        self.current_namehost = None
        self.name_ui = name_ui
        self.obj_win = obj_win

        self.currentNameHosts()

    def currentNameHosts(self):
        self.current_namehost = os.uname()[1]
        self.name_ui.lineEdit_currentname.setText(self.current_namehost)

    # Отключение выделения текста
    def disableSelection(self):
        self.name_ui.lineEdit_currentname.deselect()

    def clickCheckboxChange(self):
        bool_state = False
        if self.name_ui.checkBox_change.isChecked():
            bool_state = True
        elif not self.name_ui.checkBox_change.isChecked():
            bool_state = False

        self.name_ui.label_changename.setEnabled(bool_state)
        self.name_ui.lineEdit_changename.setEnabled(bool_state)
        self.name_ui.pushButton_namehost_apply.setEnabled(bool_state)
        self.name_ui.pushButton_namehost_cancel.setEnabled(bool_state)
        self.name_ui.label_currentname.setDisabled(bool_state)
        self.name_ui.lineEdit_currentname.setDisabled(bool_state)

    def clickPushbuttonCancel(self):
        self.name_ui.lineEdit_changename.clear()
        self.name_ui.checkBox_change.setCheckState(False)
        self.clickCheckboxChange()

    def clickPushbuttonApply(self):
        new_name = self.name_ui.lineEdit_changename.text()
        if len(new_name) > 0:
            # Проверка на ошибку unable to resolve host
            command = "sudo ls -al / >/dev/null"
            err_msg = runProcessReturnErrCode(command)
            if err_msg[1]:
                QMessageBox.critical(self.obj_win, "Ошибка!", err_msg[1])
            else:
                os.system("sudo hostname {}".format(new_name))
                t1 = threading.Thread(target=self.changeFileHostname, name='Thread1', args=("/etc/hostname", new_name,))
                # ret_code = changeFileHostname("/etc/hostname", new_name)
                t1.start()
                text = "Изменяем файл /etc/hostname"
                t2 = TimerMessageBox(text=text)
                t2.exec_()
                t1.join()
                if not self.ret_code[2]:
                    # ret_code = changeNameHosts("/etc/hosts", self.current_namehost, new_name)
                    t1 = threading.Thread(target=self.changeNameHosts, name='Thread2', args=("/etc/hosts", self.current_namehost,
                                                                                             new_name,))
                    t1.start()
                    text = "Изменяем файл /etc/hosts"
                    t2 = TimerMessageBox(text=text)
                    t2.exec_()
                    t1.join()
                    if not self.ret_code[2]:
                        QMessageBox.information(self.obj_win, "Успех!", "Имя компьютера изменено успешно!")
                        ask = QMessageBox.information(self.obj_win, "", "Перезапустить графическую сессию?",
                                                      QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Cancel)
                        if ask == QMessageBox.Ok:
                            command = "sudo systemctl restart fly-dm"
                            runProcessReturnErrCode(command)
                    else:
                        QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка изменения файла /etc/hosts")
                else:
                    QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка изменения файла /etc/hostname")
            self.currentNameHosts()
        elif not len(new_name):
            QMessageBox.critical(self.obj_win, "Ошибка!", "Не указано новое имя компьютера!")

    def changeFileHostname(self, file="/etc/hostname", new_str=None):
        f_tmp = "/tmp/temp.tmp"
        with open(f_tmp, "w") as ft:
            ft.writelines(new_str + "\n")
        command = "sudo mv {} {}".format(f_tmp, file)
        self.ret_code = runProcessReturnErrCode(command)
        # return ret_code

    def changeNameHosts(self, file="/etc/hosts", template=None, new_str=None):
        f_tmp = "/tmp/temp.tmp"
        with open(f_tmp, "w") as ft:
            with open(file, "r") as ff:
                list_file_all = ff.readlines()  # Список, каждый элемент которого строка со служебными символами
                for line in list_file_all:
                    consilience = False
                    for i in line.split():  # Перебор строки поэлементно
                        if template == i:  # Один из элементов совпадает с искомым именем компьютера
                            consilience = True
                    if consilience:    # В данной строке найдено точное совпадение с искомым именем компьютера
                        list_for_change = line.split(template)  # Получаем новый список состоящий из двух элементов,
                        # и не включающий элемент с названием искомого имени компьютера
                        list_for_change.insert(1, new_str)
                        line_changed = "".join(list_for_change)  # Объединение измененного списка в строку
                    else:
                        line_changed = line
                    ft.writelines(line_changed)
        command = "sudo mv {} {}".format(f_tmp, file)
        self.ret_code = runProcessReturnErrCode(command)
        # return ret_code


class ChangeSettingsEthernet(object):
    def __init__(self, name_ui, obj_win):
        super().__init__()
        self.name_ui = name_ui
        self.obj_win = obj_win
        self.list_eth = []
        self.list_mac = []
        self.dictEthMac = {}

        self.currentEthName()
        self.currentEthMac()
        self.dictEth()
        self.changeTreeWidgetNetmac()

    def currentEthName(self):
        out = runProcessReturnErrCode("ip a |awk '/state UP/{print $2}' | awk -F: '{print $1}'")
        self.list_eth = out[0].split()

    def currentEthMac(self):
        for el in self.list_eth:
            out = runProcessReturnErrCode("ip link show dev " + el + " |awk '/link/{print $2}'")
            self.list_mac.append(out[0].strip())

    def dictEth(self):
        self.dictEthMac = dict(zip(self.list_eth, self.list_mac))

    def changeTreeWidgetNetmac(self):
        for el in self.dictEthMac:
            item = QTreeWidgetItem(self.name_ui.treeWidget_netmac)
            item.setText(0, el)
            item.setText(1, self.dictEthMac[el])
            if el in "pxe":
                item.setDisabled(True)
                item.setText(2, "not change")
            else:
                box = QComboBox()
                for elc in self.list_mac:
                    # if self.dictEthMac["pxe"] != elc:
                    box.addItem(elc)
                self.name_ui.treeWidget_netmac.setItemWidget(item, 2, box)


class ChangeSettingsServices(object):
    def __init__(self, name_ui, obj_win):
        super().__init__()
        self.name_ui = name_ui
        self.txt_state = "unknown"
        self.obj_win = obj_win
        self.ret_code = None
        self.current_state()

    def current_state(self):
        self.state("ufw")

    def state(self, name_serv=None):
        color_state = None
        command_state_serv = "systemctl is-enabled {}".format(name_serv)
        if name_serv == "ufw":
            ret_code = runProcessReturnErrCode(command_state_serv)
            if ret_code[2]:
                self.txt_state = "Отключена"
                color_state = "QLabel { background-color: lightgreen }"
            elif not ret_code[2]:
                self.txt_state = "Включена"
                color_state = "QLabel { background-color: Tomato }"
            self.name_ui.label_ufw.setText(self.txt_state)
            self.name_ui.label_ufw.setStyleSheet(color_state)

    def clickCheckboxChangeServices(self):
        bool_state_otm = False
        bool_state_prim = False
        if self.name_ui.checkBox_ufw.isChecked() and self.txt_state == "Отключена":
            bool_state_otm = True
            bool_state_prim = False
        elif self.name_ui.checkBox_ufw.isChecked() and self.txt_state == "Включена":
            bool_state_otm = False
            bool_state_prim = True
        elif not self.name_ui.checkBox_ufw.isChecked():
            bool_state_otm = False
            bool_state_prim = False

        self.name_ui.pushButton_serv_otm.setEnabled(bool_state_otm)
        self.name_ui.pushButton_serv_prim.setEnabled(bool_state_prim)

    def clickPushButtonPrim(self):
        ret_code = self.stopServices(name_serv="ufw")
        if not ret_code:
            QMessageBox.information(self.obj_win, "Успех!", "Служба отключена!")
        else:
            QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка!")

        self.current_state()
        self.clickCheckboxChangeServices()

    def clickPushButtonOtm(self):
        ret_code = self.startServices(name_serv="ufw")
        if not ret_code:
            QMessageBox.information(self.obj_win, "Успех!", "Служба включена!")
        else:
            QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка!")

        self.current_state()
        self.clickCheckboxChangeServices()

    @staticmethod
    def stopServices(name_serv=None):
        print("Отключаем службу", name_serv)
        command = "sudo systemctl stop {} ".format(name_serv)
        runProcessReturnErrCode(command)
        command = "sudo systemctl disable {} ".format(name_serv)
        ret_code = runProcessReturnErrCode(command)
        print(ret_code)
        return int(ret_code[2])

    @staticmethod
    def startServices(name_serv=None):
        print("Включаем службу", name_serv)
        command = "sudo systemctl enable {} ".format(name_serv, name_serv)
        ret_code = runProcessReturnErrCode(command)
        command = "sudo systemctl start {} ".format(name_serv)
        runProcessReturnErrCode(command)
        return int(ret_code[2])


class TimerMessageBox(QMessageBox, threading.Thread):
    def __init__(self, text=None):
        super().__init__()
        self.text = text
        self.setWindowTitle("wait")
        self.time_to_wait = 0
        self.setText("{0}.\nWait (closing automatically) running in {1} second.".format(self.text, self.time_to_wait))
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.change_content)
        self.timer.start()

    def change_content(self):
        self.setText("{0}.\nWait (closing automatically) running in {1} second.".format(self.text, self.time_to_wait))
        self.time_to_wait += 1
        # if threading.activeCount() == 1:
        if threading.active_count() == 1:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()
