#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ScannerNetwork(object):
    def __init__(self, start_ip=None, finished_ip=None):
        super().__init__()
        self.start_ip = start_ip
        self.finished_ip = finished_ip
        if self.start_ip and self.finished_ip:
            self.correctInput()
        print("asdkjasldj"+self.start_ip)

    def correctInput(self):
        start_ip_spl = self.start_ip.split('.')[3]
        finish_ip_spl = self.finished_ip.split('.')[3]
        print(start_ip_spl)


