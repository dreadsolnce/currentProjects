#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox


class ScannerNetworkModule(object):
    def __init__(self, obj_win=None, obj_win_gui=None):
        super().__init__()
        self.obj_win = obj_win
        self.obj_win_gui = obj_win_gui
        self.err = False

    # Функция проверяющая корректность ввода ip адресов
    def correctInput(self):
        print("Correct input scanner network")
        start_ip_sp = self.obj_win.lineEdit_Scanner_startip.text().split(".")
        finished_ip_sp = self.obj_win.lineEdit_Scanner_finishedip.text().split(".")
        full_start_ip, full_finished_ip = ''.join(start_ip_sp), ''.join(finished_ip_sp)
        if full_start_ip > full_finished_ip:
            self.err = True
        else:
            for j in range(1, 3):
                reformat_ip = []
                if j == 1:
                    ip_sp = start_ip_sp
                elif j == 2:
                    ip_sp = finished_ip_sp
                for i in ip_sp:
                    if not self.err and i and int(ip_sp[0]) > 0:
                        if 0 <= int(i) < 256:
                            reformat_ip.append(str(int(i)))
                        else:
                            self.err = True
                    else:
                        self.err = True
                if not self.err and j == 1:
                    reformat_start_ip_sp = reformat_ip
                elif not self.err and j == 2:
                    reformat_finished_ip_sp = reformat_ip
                # elif self.err:
                #     QMessageBox.critical(self.obj_win_gui, "Ошибка!", "Ошибка ввода ip адреса!", QMessageBox.Ok)
                #     self.obj_win_gui.close()
        if self.err:
            QMessageBox.critical(self.obj_win_gui, "Ошибка!", "Ошибка ввода ip адреса!", QMessageBox.Ok)
            self.obj_win_gui.close()

