#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
from PyQt5.QtWidgets import QMessageBox


def runProcess(command=None, returncode=False):
    out = None
    err = None
    if command:
        proc = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if returncode is True:
            return proc.returncode
    return out, err


def stateAutoLogin(file, template):
    with open(file, 'r') as f:
        name_user = None
        exit_code = False
        for line in f:
            if template in line:
                list_line = list(line.split())
                for i in list_line:
                    if i == template and list_line[0] == template:
                        exit_code = True
                        name_user = list_line[2]
                        break
    return exit_code, name_user


def stateAutoLoginAstra(file, template):
    with open(file, 'r') as f:
        exit_code = False
        name_user = None
        for line in f:
            if template in line:
                list_line = list(line.split("="))
                for i in list_line:
                    if template == "AutoLoginEnable":
                        if i.strip() == template and list_line[0].strip() == template and list_line[1].lower().strip() == "true":
                            exit_code = True
                            break
                    elif template == "AutoLoginUser":
                        if i.strip() == template and list_line[0].strip() == template:
                            exit_code = True
                            name_user = list_line[1]
                            break
    return exit_code, name_user


def changeFile(file=None, template=None, new_str=None):
    file_tmp = "/tmp/temp.tmp"
    with open(file_tmp, 'w') as ft:
        with open(file, 'r') as f:
            for line in f:
                ex = False
                list_line = list(line.split())
                for i in list_line:
                    if i == template and not ex:
                        ft.writelines(new_str + '\n')
                        ex = True
                if not ex:
                    ft.writelines(line)
    out, err = runProcess("sudo cp {} {}".format(file_tmp, file))
    return out, err


def changeFileAstra(file=None, template=None, new_str=None):
    file_tmp = "/tmp/temp.tmp"
    with open(file_tmp, 'w') as ft:
        with open(file, 'r') as f:
            ex = False
            for line in f:
                if template in line and not ex:
                    ft.writelines(new_str + '\n')
                    ex = True
                else:
                    ft.writelines(line)
    out, err = runProcess("sudo cp {} {}".format(file_tmp, file))
    return out, err


def copyFile(file_src=None, file_bak=None):
    out, err = None, None
    if not os.path.isfile(file_bak):
        process = subprocess.Popen("sudo cp {} {}".format(file_src, file_bak), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
    return out, err


class MainSettingsModule(object):
    def __init__(self, os_ver=None, os_debian=None, os_astra=None, name_ui=None, obj_win=None):
        super().__init__()
        self.os_ver = os_ver
        self.os_debian = os_debian
        self.os_astra = os_astra
        self.name_ui = name_ui
        self.obj_win = obj_win

        self.currentUserAutologin()
        self.currentStateNetworkManager()
        self.currentStateSuperUser()

    def clickAutologinCheckBox(self):
        bool_state = False
        if self.name_ui.checkBox_autologin.isChecked():
            bool_state = True
        elif not self.name_ui.checkBox_autologin.isChecked():
            bool_state = False

        self.name_ui.label_2.setEnabled(bool_state)
        self.name_ui.comboBox_nameuser.setEnabled(bool_state)
        self.name_ui.label_autologin.setDisabled(bool_state)

        # Если текущвая ОС принадлежит астре, то открываем пункт выбора уровня доступа
        if self.os_ver in self.os_astra:
            self.name_ui.comboBox_mac.setEnabled(bool_state)
            self.name_ui.label_3.setEnabled(bool_state)

        # self.name_ui.pushButton_apply.setEnabled(bool_state)
        self.stateApplyPushButton()

        # Формируем список пользователей и добавляем в comboBox_nameuser
        self.userList()

        # При изменении comboBox_nameuser формируем список с mac доступом выбранного пользователя
        self.name_ui.comboBox_nameuser.currentTextChanged.connect(self.userMac)

    def clickNetworkManagerCheckBox(self):
        bool_state = False
        if self.name_ui.checkBox_networkmanager.isChecked():
            bool_state = True
        elif not self.name_ui.checkBox_networkmanager.isChecked():
            bool_state = False

        self.name_ui.radioButton_netdisable.setEnabled(bool_state)
        self.name_ui.radioButton_netenable.setEnabled(bool_state)

        self.stateApplyPushButton()
        self.currentStateNetworkManager()

    def clickSetRootUser(self):
        bool_state = False
        if self.name_ui.checkBox_root.isChecked():
            bool_state = True
        elif not self.name_ui.checkBox_root.isChecked():
            bool_state = False

        self.name_ui.label_root_pass.setEnabled(bool_state)
        self.name_ui.lineEdit_pass.setEnabled(bool_state)
        self.name_ui.label_root_pass_confirm.setEnabled(bool_state)
        self.name_ui.lineEdit_pass_confirm.setEnabled(bool_state)
        self.name_ui.plainTextEdit_root.setEnabled(bool_state)

        self.stateApplyPushButton()

    def stateApplyPushButton(self):
        if self.name_ui.checkBox_networkmanager.isChecked() or self.name_ui.checkBox_autologin.isChecked() or self.name_ui.checkBox_root.isChecked():
            self.name_ui.pushButton_apply.setEnabled(True)
        elif not self.name_ui.checkBox_networkmanager.isChecked() and not self.name_ui.checkBox_autologin.isChecked() and not self.name_ui.checkBox_root.isChecked():
            self.name_ui.pushButton_apply.setEnabled(False)

    # Добавляем пользователей в combobox
    def userList(self):
        ul = ["", "Выключить автовход"]  # Список пользователей
        proc = subprocess.run("sudo cat /etc/passwd | grep '/bin/bash' | awk -F: '{print $1}'", shell=True,
                              stdout=subprocess.PIPE)
        for line in proc.stdout.split():
            if line and line.decode("utf-8") != "root":
                ul.append(line.decode("utf-8"))
        self.name_ui.comboBox_nameuser.clear()
        self.name_ui.comboBox_nameuser.addItems(ul)

    def userMac(self):
        ml = []
        cur_user = self.name_ui.comboBox_nameuser.currentText()
        if not cur_user or cur_user == "Выключить автовход":
            self.name_ui.comboBox_mac.clear()
        else:
            out, err = runProcess("sudo pdpl-user " + cur_user + " | awk '{print $1}' | awk -F: '{print $2}'")
            for line in out.split():
                if line:
                    ml.append(line.decode("utf-8"))
            self.name_ui.comboBox_mac.clear()
            self.name_ui.comboBox_mac.addItems(ml)

    def currentUserAutologin(self):
        # Если текущвая ОС принадлежит астре
        if self.os_ver in self.os_astra:
            state_autologin = stateAutoLoginAstra("/etc/X11/fly-dm/fly-dmrc", "AutoLoginEnable")
            if not state_autologin:
                self.name_ui.label_autologin.setText('Статус: \tВыключен')
            else:
                state_user_login, name_user_login = stateAutoLoginAstra("/etc/X11/fly-dm/fly-dmrc", "AutoLoginUser")
                if state_user_login:
                    name_user = name_user_login
                    self.name_ui.label_autologin.setText('Статус: \tВключён. Пользователь {}'.format(name_user))

        # Если текущвая ОС принадлежит ubuntu, то определяем статус автозагрузки применяя соответствующие функции: stateAutoLogin и userAutoLogin
        elif self.os_ver in self.os_debian:
            state_autologin = stateAutoLogin("/etc/gdm3/custom.conf", "AutomaticLoginEnable")
            if not state_autologin:
                self.name_ui.label_autologin.setText('Статус: \tВыключен')
            else:
                state_user_login, name_user = stateAutoLogin("/etc/gdm3/custom.conf", "AutomaticLogin")
                if state_user_login:
                    # name_user = userAutoLogin("/etc/gdm3/custom.conf", "AutomaticLogin")
                    self.name_ui.label_autologin.setText('Статус: \tВключён. Пользователь {}'.format(name_user))

    def currentStateNetworkManager(self):
        if self.os_ver in self.os_astra:
            out, err = runProcess("sudo systemctl status NetworkManager | grep Active | awk '{print $2}'")
            print(out.decode("utf-8").strip())
            if out.decode("utf-8").strip() == "inactive":
                self.name_ui.label_networkmanager.setText("Статус: \tВыключен")
            elif out.decode("utf-8").strip() == "active":
                self.name_ui.label_networkmanager.setText("Статус: \tВключен")

    def currentStateSuperUser(self):
        out, err = runProcess("sudo cat /etc/shadow | grep root | awk -F: '{print $2}'")
        if out.decode("utf-8").strip() == "!" or out.decode("utf-8").strip() == "*":
            self.name_ui.label_root_state.setText("Статус: \tНе настроен")
        else:
            self.name_ui.label_root_state.setText("Статус: \tНастроен")

    def clickPushbuttonApply(self):
        print("Нажата кнопка применить...")
        cur_user = self.name_ui.comboBox_nameuser.currentText()
        cur_mac = self.name_ui.comboBox_mac.currentText()
        if self.name_ui.checkBox_autologin.isChecked():
            if (self.os_ver in self.os_debian
                    and cur_user != ""
                    and cur_user != "Выключить автовход"):
                self.__applyAutologinDebian(action="Enable", cur_user=cur_user)
            elif self.os_ver in self.os_debian and cur_user == "Выключить автовход":
                self.__applyAutologinDebian(action="Disable")
            elif self.os_ver in self.os_astra and cur_user != "" and cur_user != "Выключить автовход":
                self.__applyAutologinAstra(action="Enable", cur_user=cur_user, cur_mac=cur_mac)
            elif self.os_ver in self.os_astra and cur_user == "Выключить автовход":
                self.__applyAutologinAstra(action="Disable")
            self.currentUserAutologin()
        if self.name_ui.checkBox_networkmanager.isChecked():
            if self.os_ver in self.os_astra and self.name_ui.radioButton_netenable.isChecked():
                self.__applyNetworkManager(action="Enable")
            elif self.os_ver in self.os_astra and self.name_ui.radioButton_netdisable.isChecked():
                self.__applyNetworkManager(action="Disabled")
        if self.name_ui.checkBox_root.isChecked() and len(self.name_ui.lineEdit_pass.text()) != 0:
            if self.name_ui.lineEdit_pass.text() == self.name_ui.lineEdit_pass_confirm.text():
                if self.os_ver in self.os_astra:
                    self.__applySuperUser(os_ver="Astra")
                elif self.os_ver in self.os_debian:
                    self.__applySuperUser()
            else:
                QMessageBox.critical(self.obj_win, "Ошибка!", "Пароли введенные для суперпользоватея не совпадают!", QMessageBox.Ok)

    def __applyAutologinDebian(self, action=None, cur_user=None):
        # Вкючаем автозагрузку
        s1 = None
        s2 = None
        if action == "Enable":
            s1 = "AutomaticLoginEnable = true"
            s2 = "AutomaticLogin = {}".format(cur_user)
        # Отключаем автозагрузку
        elif action == "Disable":
            s1 = "# AutomaticLoginEnable = true"
            s2 = "# AutomaticLogin = user1"

        copyFile("/etc/gdm3/custom.conf", "/etc/gdm3/custom.conf.PNOSKO.bak")
        out, err = changeFile("/etc/gdm3/custom.conf", "AutomaticLoginEnable", s1)
        if err:
            QMessageBox.critical(self.obj_win, "Ошибка!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
        else:
            out, err = changeFile("/etc/gdm3/custom.conf", "AutomaticLogin", s2)
            if err:
                QMessageBox.critical(self.obj_win, "Ошибка!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
            else:
                if action == "Enable":
                    os.system("seahorse")
                QMessageBox.information(self.obj_win, "Успех!", "Настройка автовхода выполнена успешно!", QMessageBox.Ok)

    def __applyAutologinAstra(self, action=None, cur_user=None, cur_mac=None):
        # Вкючаем автозагрузку
        s1 = None
        s2 = None
        s3 = None
        if action == "Enable":
            s1 = "AutoLoginEnable=true"
            s2 = "AutoLoginUser={}".format(cur_user)
            s3 = "AutoLoginMAC=0:"+cur_mac+":0"
        # Отключаем автозагрузку
        elif action == "Disable":
            s1 = "#AutoLoginEnable=false"
            s2 = "#AutoLoginUser=alex1"
            s3 = "#AutoLoginMAC="

        copyFile("/etc/X11/fly-dm/fly-dmrc", "/etc/X11/fly-dm/fly-dmrc.PNOSKO.bak")
        out, err = changeFileAstra("/etc/X11/fly-dm/fly-dmrc", "AutoLoginEnable", s1)
        if err:
            QMessageBox.critical(self.obj_win, "Ошибка!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
        else:
            out, err = changeFileAstra("/etc/X11/fly-dm/fly-dmrc", "AutoLoginUser", s2)
            if err:
                QMessageBox.critical(self.obj_win, "Ошибка!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
            else:
                out, err = changeFileAstra("/etc/X11/fly-dm/fly-dmrc", "AutoLoginMAC", s3)
                if err:
                    QMessageBox.critical(self.obj_win, "Ошибка!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
                else:
                    QMessageBox.information(self.obj_win, "Успех!", "Настройка автовхода выполнена успешно!", QMessageBox.Ok)

    def __applyNetworkManager(self, action=None):
        if action == "Enable":
            return_code = runProcess("sudo systemctl --now unmask NetworkManager", returncode=True)
            if return_code:
                QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка включения службы!", QMessageBox.Ok)
            else:
                return_code = runProcess("sudo systemctl restart NetworkManager", returncode=True)
                if return_code:
                    QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка перезапуска сетевой службы!", QMessageBox.Ok)
                else:
                    if os.path.isfile("/etc/xdg/autostart/nm-applet.desktop.disabled"):
                        return_code = runProcess("sudo mv -f /etc/xdg/autostart/nm-applet.desktop.disabled /etc/xdg/autostart/nm-applet.desktop", returncode=True)
                        if return_code:
                            QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка добавления значка!", QMessageBox.Ok)
                        else:
                            QMessageBox.information(self.obj_win, "Сообщение!", "Включение апплета выполнено успешно!")
                    else:
                        QMessageBox.information(self.obj_win, "Сообщение!", "Включение апплета выполнено успешно!")

                    ask = QMessageBox.information(self.obj_win, "", "Перезапустить графическую сесию?",
                                                  QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Cancel)
                    if ask == QMessageBox.Ok:
                        return_code = runProcess("sudo systemctl restart fly-dm", returncode=True)
                        if return_code:
                            QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка перезапуска графической сесии!", QMessageBox.Ok)
        elif action == "Disabled":
            return_code = runProcess("sudo systemctl --now mask NetworkManager", returncode=True)
            if return_code != 0:
                QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка отключения службы!", QMessageBox.Ok)
            else:
                return_code = runProcess("sudo systemctl restart networking", returncode=True)
                if return_code != 0:
                    QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка перезапуска сетевой службы!", QMessageBox.Ok)
                else:
                    if os.path.isfile("/etc/xdg/autostart/nm-applet.desktop"):
                        return_code = runProcess("sudo mv -f /etc/xdg/autostart/nm-applet.desktop /etc/xdg/autostart/nm-applet.desktop.disabled", returncode=True)
                        if return_code != 0:
                            QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка удаления значка!", QMessageBox.Ok)
                        else:
                            QMessageBox.information(self.obj_win, "Сообщение!", "Отключение апплета выполнено успешно!")
                    else:
                        QMessageBox.information(self.obj_win, "Сообщение!", "Отключение апплета выполнено успешно!")
                    ask = QMessageBox.information(self.obj_win, "", "Перезапустить графическую сесию?",
                                                  QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Cancel)
                    if ask == QMessageBox.Ok:
                        return_code = runProcess("sudo systemctl restart fly-dm", returncode=True)
                        if return_code != 0:
                            QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка перезапуска графической сесии!", QMessageBox.Ok)

    def __applySuperUser(self, os_ver=None):
        err_status = 0
        password = self.name_ui.lineEdit_pass.text().encode()  # Представление в байтовом режиме
        proc = subprocess.Popen(['/usr/bin/sudo', 'passwd', 'root'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        proc.stdin.write(password + b"\n" + password + b"\n")
        proc.stdin.flush()
        proc.communicate()
        err_status = err_status + proc.returncode
        if os_ver == "Astra":
            ret = os.system("sudo pdpl-user -i 63 root > /dev/null")
            err_status = err_status + ret
        if err_status == 0:
            QMessageBox.information(self.obj_win, "Сообщение!", "Настройка пользователя root успех!")
        else:
            QMessageBox.critical(self.obj_win, "Ошибка!", "Ошибка настройки пользователя root!")