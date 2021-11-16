#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess


# Функция определения версии ОС
def OsVersion():
    command_1, command_2 = "cat /etc/lsb-release | grep DISTRIB_ID | awk -F= '{print $2}'", \
                           "cat /etc/lsb-release | grep DISTRIB_RELEASE | awk -F= '{print $2}'"
    os_ver = action_program(command_1) + " " + action_program(command_2)
    print("Версия ОС: " + os_ver)
    return os_ver


# Функция запуска комманды с выводом результата
def action_program(command):
    st = None
    if command:
        proc = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        st = proc.stdout.readline().decode("utf-8").strip()
    return st


if __name__ == "__main__":
    OsVersion()
