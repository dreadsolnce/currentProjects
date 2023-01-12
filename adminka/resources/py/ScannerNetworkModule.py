#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import sys
import time
import os
import socket

from PyQt5.QtWidgets import QMessageBox


class ScannerNetworkModule(object):
    def __init__(self, obj_win=None, obj_win_gui=None):
        super().__init__()
        self.obj_win = obj_win
        self.obj_win_gui = obj_win_gui
        self.err = False
        self.f_list = sys.path[0] + "/files/list.txt"

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
        if self.err:
            QMessageBox.critical(self.obj_win_gui, "Ошибка!", "Ошибка ввода ip адреса!", QMessageBox.Ok)
            self.obj_win_gui.close()
        else:
            s = Scan(reformat_start_ip_sp, reformat_finished_ip_sp, self.f_list)
            s.start()


class RunScan(threading.Thread):
    def __init__(self, ip=None):
        super().__init__()
        self.ip = ip

    def run(self):
        print(self.ip)


class Scan(RunScan):
    def __init__(self, start_ip=None, end_ip=None, f_list="/tmp/list.txt"):
        super().__init__()
        self.start_list = start_ip
        self.end_list = end_ip
        self.f_list = f_list

    def start(self):
        s3, s4 = int(self.start_list[2]), int(self.start_list[3])
        e3, e4 = int(self.end_list[2]), int(self.end_list[3])

        if s3 == e3:
            while s4 <= e4:
                ip = str(self.start_list[0]) + "." + self.start_list[1] + "." + str(s3) + "." + str(s4)
                proc = RunScan(ip)
                proc.start()
                s4 += 1
                time.sleep(0.05)
        elif s3 < e3:
            while s3 <= e3:
                while s4 <= 255:
                    ip = str(self.start_list[0]) + "." + self.start_list[1] + "." + str(s3) + "." + str(s4)
                    proc = RunScan(ip)
                    proc.start()
                    if s3 == e3 and s4 == e4:
                        break
                    s4 += 1
                    time.sleep(0.05)
                s3 += 1
                s4 = 1


        # if os.path.exists(self.f_list):
        #     os.remove(self.f_list)
        # start_ip_spl = self.start_ip.split('.')[3]
        # finish_ip_spl = self.end_ip.split('.')[3]
        # print(start_ip_spl)
        # print(self.start_ip)
        # # for i in range(int(self.start_ip), int(self.end_ip) + 1):
        # #     ip = self.start_ip.split(".")[0] + \
        # #          "." + self.start_ip.split(".")[1] + \
        # #          "." + self.start_ip.split(".")[2] + \
        # #          "." + str(i)
        # #     r = RunScan()
        # #     r.start()
