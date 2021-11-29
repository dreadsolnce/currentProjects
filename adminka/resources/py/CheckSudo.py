#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget


# Функция выполняет команду и выводит текст ошибки
def run_process_exit_out(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    err = err.decode("utf-8").strip()
    return err


# Класс определения имеет ли право пользователь пользоваться командой sudo
class CheckSudo(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.start()

    def start(self):
        command = "sudo -n ls /"
        checksudo = run_process_exit_out(command)
        if checksudo == "sudo: требуется пароль" or checksudo == "sudo: a password is required":
            print("Для запуска необходимы права суперпользователя")
            self.winCenter()
            QtWidgets.QMessageBox.critical(self, "Ошибка!", "Не достаточно прав для запуска")
            sys.exit(1)
        elif not checksudo:
            print("Программа запущена")

    # Центрирование окна относительно экрана
    def winCenter(self):
        qr = self.frameGeometry()
        qp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(qp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ch = CheckSudo()
    sys.exit(app.exec_())
