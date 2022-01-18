#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MainSettingsModule(object):
    def __init__(self, os_ver=None, name_ui=None, obj_win=None):
        super().__init__()
        self.os_ver = os_ver
        self.name_ui = name_ui
        self.obj_win = obj_win

    def clickAutologinCheckBox(self):
        bool_state = False
        if self.name_ui.checkBox_autologin.isChecked():
            bool_state = True
        elif not self.name_ui.checkBox_autologin.isChecked():
            bool_state = False
        self.name_ui.label_2.setEnabled(bool_state)
        self.name_ui.label_3.setEnabled(bool_state)
        self.name_ui.comboBox_nameuser.setEnabled(bool_state)
        self.name_ui.lineEdit_accesslevel.setEnabled(bool_state)
