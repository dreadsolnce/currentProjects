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
            # ex = False
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


def changeFileNew(file=None, template=None, new_str=None):
    file_tmp = "/tmp/temp.tmp"
    with open(file_tmp, 'w') as ft:
        with open(file, 'r') as f:
            for line in f:
                if " ".join(line.split()) == " ".join(template.split()):
                    ft.writelines(new_str + '\n')
                else:
                    ft.writelines(line)
    out, err = runProcess("sudo cp {} {}".format(file_tmp, file))
    return out, err


def copyFile(file_src=None, file_bak=None, copying_reverse=False):
    out, err = None, None
    if copying_reverse is True:
        # if not os.path.isfile(file_bak):
        #     err = "NotFileBak"
        # else:
        process = subprocess.Popen("sudo cp {} {}".format(file_bak, file_src), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
    else:
        if not os.path.isfile(file_bak):
            process = subprocess.Popen("sudo cp {} {}".format(file_src, file_bak), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
    return out, err


def findTemplateFile(file=None, template=None):
    with open(file, 'r') as f:
        for line in f:
            if " ".join(line.split()) == " ".join(template.split()):
                return True
    return False


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
        self.currentStateSSH()
        self.currentStateTime()
        self.currentStateRemoteSession()
        self.currentStateResolv()

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
        self.name_ui.label_networkmanager.setDisabled(bool_state)

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
        self.name_ui.label_root_state.setDisabled(bool_state)

        self.stateApplyPushButton()

    def clickSetSSH(self):
        bool_state = False
        if self.name_ui.checkBox_ssh.isChecked():
            bool_state = True
        elif not self.name_ui.checkBox_ssh.isChecked():
            bool_state = False

        self.name_ui.radioButton_ssh_disable.setEnabled(bool_state)
        self.name_ui.radioButton_ssh_enable.setEnabled(bool_state)
        self.name_ui.label_ssh_state.setDisabled(bool_state)

        self.stateApplyPushButton()

    def clickSetTimeMode(self):
        bool_state = False
        if self.name_ui.checkBox_time.isChecked():
            bool_state = True
        elif not self.name_ui.checkBox_time.isChecked():
            bool_state = False

        self.name_ui.radioButton_utc.setEnabled(bool_state)
        self.name_ui.radioButton_localtime.setEnabled(bool_state)
        self.name_ui.label_time_state.setDisabled(bool_state)

        self.stateApplyPushButton()

    def clickSetRemoteSession(self):
        bool_state = False
        if self.name_ui.checkBox_remote_session.isChecked():
            bool_state = True
        elif not self.name_ui.checkBox_remote_session.isChecked():
            bool_state = False

        self.name_ui.radioButton_remote_enable.setEnabled(bool_state)
        self.name_ui.radioButton_remote_disable.setEnabled(bool_state)
        self.name_ui.label_remote_session_2.setDisabled(bool_state)

        self.stateApplyPushButton()

    def clickSetResolv(self):
        bool_state = False
        if self.name_ui.checkBox_resolv.isChecked():
            bool_state = True
        elif not self.name_ui.checkBox_resolv.isChecked():
            bool_state = False

        self.name_ui.radioButton_resolv.setEnabled(bool_state)
        self.name_ui.label_resolv_state.setDisabled(bool_state)

        self.stateApplyPushButton()

    def stateApplyPushButton(self):
        if self.name_ui.checkBox_networkmanager.isChecked() or self.name_ui.checkBox_autologin.isChecked() \
                or self.name_ui.checkBox_root.isChecked() or self.name_ui.checkBox_ssh.isChecked() \
                or self.name_ui.checkBox_time.isChecked() or self.name_ui.checkBox_remote_session.isChecked()\
                or self.name_ui.checkBox_resolv.isChecked():
            self.name_ui.pushButton_apply.setEnabled(True)
        elif not self.name_ui.checkBox_networkmanager.isChecked() and not self.name_ui.checkBox_autologin.isChecked() \
                and not self.name_ui.checkBox_root.isChecked() and not self.name_ui.checkBox_ssh.isChecked() \
                and not self.name_ui.checkBox_time.isChecked() and not self.name_ui.checkBox_remote_session.isChecked()\
                and not self.name_ui.checkBox_resolv.isChecked():
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
            state_autologin, name_user_login = stateAutoLoginAstra("/etc/X11/fly-dm/fly-dmrc", "AutoLoginEnable")
            if not state_autologin:
                self.name_ui.label_autologin.setText('Статус: \tВыключен')
                self.name_ui.label_autologin.setStyleSheet("QLabel { background-color: Tomato }")
            else:
                state_user_login, name_user_login = stateAutoLoginAstra("/etc/X11/fly-dm/fly-dmrc", "AutoLoginUser")
                if state_user_login:
                    name_user = name_user_login.strip()
                    self.name_ui.label_autologin.setText('Статус: \tВключён. Пользователь {}'.format(name_user))
                    self.name_ui.label_autologin.setStyleSheet("QLabel { background-color: lightgreen }")

        # Если текущвая ОС принадлежит ubuntu, то определяем статус автозагрузки применяя соответствующие функции: stateAutoLogin и userAutoLogin
        elif self.os_ver in self.os_debian:
            state_autologin, name_user_login = stateAutoLogin("/etc/gdm3/custom.conf", "AutomaticLoginEnable")
            if not state_autologin:
                self.name_ui.label_autologin.setText('Статус: \tВыключен')
                self.name_ui.label_autologin.setStyleSheet("QLabel { background-color: Tomato }")
            else:
                state_user_login, name_user = stateAutoLogin("/etc/gdm3/custom.conf", "AutomaticLogin")
                if state_user_login:
                    # name_user = userAutoLogin("/etc/gdm3/custom.conf", "AutomaticLogin")
                    self.name_ui.label_autologin.setText('Статус: \tВключён. Пользователь {}'.format(name_user))
                    self.name_ui.label_autologin.setStyleSheet("QLabel { background-color: lightgreen }")

    def currentStateNetworkManager(self):
        if self.os_ver in self.os_astra:
            out, err = runProcess("sudo systemctl status NetworkManager | grep Active | awk '{print $2}'")
            print(out.decode("utf-8").strip())
            if out.decode("utf-8").strip() == "inactive":
                self.name_ui.label_networkmanager.setText("Статус: \tВыключен")
                self.name_ui.label_networkmanager.setStyleSheet("QLabel { background-color: lightgreen }")
            elif out.decode("utf-8").strip() == "active":
                self.name_ui.label_networkmanager.setText("Статус: \tВключен")
                self.name_ui.label_networkmanager.setStyleSheet("QLabel { background-color: Tomato }")

    def currentStateSuperUser(self):
        out, err = runProcess("sudo cat /etc/shadow | grep root | awk -F: '{print $2}'")
        if out.decode("utf-8").strip() == "!" or out.decode("utf-8").strip() == "*":
            self.name_ui.label_root_state.setText("Статус: \tНе настроен")
            self.name_ui.label_root_state.setStyleSheet("QLabel { background-color: Tomato }")
        else:
            self.name_ui.label_root_state.setText("Статус: \tНастроен")
            self.name_ui.label_root_state.setStyleSheet("QLabel { background-color: lightgreen }")

    def currentStateSSH(self):
        state = findTemplateFile("/etc/ssh/ssh_config", "ForwardX11 yes")
        if state:
            state = findTemplateFile("/etc/ssh/sshd_config", "PermitRootLogin yes")
            if state:
                state = findTemplateFile("/etc/ssh/sshd_config", "AddressFamily inet")
                if state:
                    state = findTemplateFile("/etc/ssh/sshd_config", "X11UseLocalhost yes")
        if state:
            self.name_ui.label_ssh_state.setText("Статус: \tНастроен")
            self.name_ui.label_ssh_state.setStyleSheet("QLabel { background-color: lightgreen }")
        elif not state:
            self.name_ui.label_ssh_state.setText("Статус: \tНе настроен")
            self.name_ui.label_ssh_state.setStyleSheet("QLabel { background-color: Tomato }")

    def currentStateTime(self):
        out, err = runProcess("timedatectl | grep local | grep TZ | awk -F: '{print $2}'")
        if out[1:41].strip().decode('utf-8') == "yes":
            self.name_ui.label_time_state.setText("Статус: \tLOCALTIME")
            self.name_ui.label_time_state.setStyleSheet("QLabel { background-color: lightgreen }")
        elif out[1:41].strip().decode('utf-8') == "no":
            self.name_ui.label_time_state.setText("Статус: \tUTC")
            self.name_ui.label_time_state.setStyleSheet("QLabel { background-color: Tomato }")

    def currentStateRemoteSession(self):
        if os.path.isfile('/etc/X11/fly-dm/Xaccess'):
            state = findTemplateFile("/etc/X11/fly-dm/Xaccess", "localhost #any host can get a login window")
            if state:
                state = findTemplateFile("/etc/X11/fly-dm/Xaccess", "localhost    CHOOSER BROADCAST	#any indirect host can get a chooser")
            if state:
                self.name_ui.label_remote_session_2.setText("Статус: \tВыключен")
                self.name_ui.label_remote_session_2.setStyleSheet("QLabel { background-color: Tomato }")
            elif not state:
                self.name_ui.label_remote_session_2.setText("Статус: \tВключен")
                self.name_ui.label_remote_session_2.setStyleSheet("QLabel { background-color: lightgreen }")

    def currentStateResolv(self):
        state = False
        comp_state = False
        computer_name = os.uname()[1]
        with open("/etc/hosts", 'r') as f:
            for line in f:
                if len(line.split()) > 1:
                    computer_name_hosts = line.split()[1]
                    if computer_name_hosts == computer_name and not comp_state:
                        comp_state = True
                        ip_hosts_list = line.split()[0].split('.')
                        if len(ip_hosts_list) == 4:
                            for elem in ip_hosts_list:
                                if not elem.isnumeric():
                                    state = True
                                elif 255 < int(elem) or int(elem) < 0:
                                    state = True
                        else:
                            state = True
        if state or not comp_state:
            self.name_ui.label_resolv_state.setText("Статус: \tНе настроен")
            self.name_ui.label_resolv_state.setStyleSheet("QLabel { background-color: Tomato }")
        elif not state or comp_state:
            self.name_ui.label_resolv_state.setText("Статус: \tНастроен")
            self.name_ui.label_resolv_state.setStyleSheet("QLabel { background-color: lightgreen }")
            self.name_ui.checkBox_resolv.setDisabled(True)

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
            self.currentStateNetworkManager()
        if self.name_ui.checkBox_root.isChecked() and len(self.name_ui.lineEdit_pass.text()) != 0:
            if self.name_ui.lineEdit_pass.text() == self.name_ui.lineEdit_pass_confirm.text():
                if self.os_ver in self.os_astra:
                    self.__applySuperUser(os_ver="Astra")
                elif self.os_ver in self.os_debian:
                    self.__applySuperUser()
                self.currentStateSuperUser()
            else:
                QMessageBox.critical(self.obj_win, "Ошибка!", "Пароли введенные для суперпользоватея не совпадают!", QMessageBox.Ok)
        if self.name_ui.checkBox_ssh.isChecked():
            if self.name_ui.radioButton_ssh_enable.isChecked():
                self.__applySSH(action="enable")
            elif self.name_ui.radioButton_ssh_disable.isChecked():
                self.__applySSH(action="restore")
            self.currentStateSSH()
        if self.name_ui.checkBox_time.isChecked():
            if self.name_ui.radioButton_localtime.isChecked():
                self.__applySetTime(action="localtime")
            elif self.name_ui.radioButton_utc.isChecked():
                self.__applySetTime(action="utc")
            self.currentStateTime()
        if self.name_ui.checkBox_remote_session.isChecked():
            if self.name_ui.radioButton_remote_enable.isChecked():
                self.__applySetRemoteSession(action="enable")
            elif self.name_ui.radioButton_remote_disable.isChecked():
                self.__applySetRemoteSession(action="disable")
            self.currentStateRemoteSession()
        if self.name_ui.checkBox_resolv.isChecked():
            if self.name_ui.radioButton_resolv.isChecked():
                self.__applySetResolv()
                self.currentStateResolv()

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
                    # if os.path.isfile("/etc/xdg/autostart/nm-applet.desktop.disabled"):
                    if not os.path.isfile("/etc/xdg/autostart/nm-applet.desktop"):
                        # return_code = runProcess("sudo mv -f /etc/xdg/autostart/nm-applet.desktop.disabled /etc/xdg/autostart/nm-applet.desktop", returncode=True)
                        return_code = runProcess("sudo cp /usr/share/applications/nm-applet.desktop /etc/xdg/autostart/nm-applet.desktop",
                                                 returncode=True)
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
                    # if os.path.isfile("/etc/xdg/autostart/nm-applet.desktop"):
                    if os.path.isfile("/etc/xdg/autostart/nm-applet.desktop"):
                        # return_code = runProcess("sudo mv -f /etc/xdg/autostart/nm-applet.desktop /etc/xdg/autostart/nm-applet.desktop.disabled", returncode=True)
                        return_code = runProcess("sudo rm -rf /etc/xdg/autostart/nm-applet.desktop",
                                                 returncode=True)
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

    def __applySSH(self, action=None):
        if action == "enable":
            copyFile("/etc/ssh/ssh_config", "/etc/ssh/ssh_config.PNOSKO.bak")
            copyFile("/etc/ssh/sshd_config", "/etc/ssh/sshd_config.PNOSKO.bak")

            out, err = changeFile("/etc/ssh/ssh_config", "ForwardX11", "ForwardX11 yes")
            if err:
                QMessageBox.critical(self.obj_win, "Ошибка SSH!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
            else:
                out, err = changeFileAstra("/etc/ssh/sshd_config", "PermitRootLogin", "PermitRootLogin yes")
                if err:
                    QMessageBox.critical(self.obj_win, "Ошибка SSH!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
                else:
                    out, err = changeFileAstra("/etc/ssh/sshd_config", "AddressFamily", "AddressFamily inet")
                    if err:
                        QMessageBox.critical(self.obj_win, "Ошибка SSH!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
                    else:
                        out, err = changeFileAstra("/etc/ssh/sshd_config", "X11UseLocalhost", "X11UseLocalhost yes")
                        if err:
                            QMessageBox.critical(self.obj_win, "Ошибка SSH!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
                        else:
                            return_code = runProcess("sudo systemctl start ssh", returncode=True)
                            if return_code != 0:
                                QMessageBox.critical(self.obj_win, "Ошибка SSH!", "Ошибка запукска службы ssh!", QMessageBox.Ok)
                            else:
                                return_code = runProcess("sudo systemctl enable ssh", returncode=True)
                                if return_code != 0:
                                    QMessageBox.critical(self.obj_win, "Ошибка SSH!", "Ошибка добавления службы ssh в автозагрузку!", QMessageBox.Ok)
                                else:
                                    QMessageBox.information(self.obj_win, "Информация!", "Настройка SSH выолнена успешно!")
        elif action == "restore":
            out, err = copyFile("/etc/ssh/ssh_config.", "/etc/ssh/ssh_config.PNOSKO.bak", copying_reverse=True)
            if err:
                QMessageBox.critical(self.obj_win, "Ошибка!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
            else:
                out, err = copyFile("/etc/ssh/sshd_config", "/etc/ssh/sshd_config.PNOSKO.bak", copying_reverse=True)
                if err:
                    QMessageBox.critical(self.obj_win, "Ошибка!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
                else:
                    QMessageBox.information(self.obj_win, "Успех!", "Настройки SSH успешно востановлены из резервной копии!", QMessageBox.Ok)

    def __applySetTime(self, action=None):
        returncode = None
        if action == "localtime":
            returncode = runProcess("sudo timedatectl set-local-rtc 1 --adjust-system-clock", returncode=True)
        elif action == "utc":
            returncode = runProcess("sudo timedatectl set-local-rtc 0 --adjust-system-clock", returncode=True)
        if returncode == 0:
            QMessageBox.information(self.obj_win, "Информация!", "Настройка формата времени выполнена успешно!")
        else:
            QMessageBox.critical(self.obj_win, "Ошибка настройки времени!", "Ошибка настройки формата времени!", QMessageBox.Ok)

    def __applySetRemoteSession(self, action=None):
        str_template_1 = None
        str_template_2 = None
        str_new_1 = None
        str_new_2 = None
        if action == "enable":
            str_template_1 = "localhost #any host can get a login window"
            str_new_1 = "* #any host can get a login window"
            str_template_2 = "localhost CHOOSER BROADCAST #any indirect host can get a chooser"
            str_new_2 = "* CHOOSER BROADCAST #any indirect host can get a chooser"
            copyFile("/etc/X11/fly-dm/Xaccess", "/etc/X11/fly-dm/Xaccess.PNOSKO.bak")
        elif action == "disable":
            str_template_1 = "* #any host can get a login window"
            str_new_1 = "localhost #any host can get a login window"
            str_template_2 = "* CHOOSER BROADCAST #any indirect host can get a chooser"
            str_new_2 = "localhost CHOOSER BROADCAST #any indirect host can get a chooser"

        out, err = changeFileNew("/etc/X11/fly-dm/Xaccess", str_template_1, str_new_1)
        if err:
            QMessageBox.critical(self.obj_win, "Ошибка!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
        else:
            out, err = changeFileNew("/etc/X11/fly-dm/Xaccess", str_template_2, str_new_2)
            if err:
                QMessageBox.critical(self.obj_win, "Ошибка!", "{}".format(err.decode("utf-8")), QMessageBox.Ok)
            else:
                QMessageBox.information(self.obj_win, "Успех!", "{}".format("Настройка пункта меню выхода 'Удалённая сесиия' выполнена успешно!"), QMessageBox.Ok)

    def __applySetResolv(self):
        file_tmp = "/tmp/temp.tmp"
        file = "/etc/hosts"
        computer_name = os.uname()[1]
        comp_state = False
        with open(file_tmp, 'w') as ft:
            with open(file, 'r') as f:
                for line in f:
                    if len(line.split()) > 1:
                        computer_name_hosts = line.split()[1]
                        if computer_name_hosts == computer_name and not comp_state:
                            comp_state = True
                            ft.writelines("127.0.1.1\t{}\n".format(computer_name))
                        else:
                            ft.writelines(line)
                    else:
                        ft.writelines(line)
                if not comp_state:
                    ft.writelines("127.0.1.1\t{}\n".format(computer_name))
        out, err = runProcess("sudo cp {} {}".format(file_tmp, file))
        QMessageBox.information(self.obj_win, "Успех!", "Успешно настроен файл hosts", QMessageBox.Ok)
