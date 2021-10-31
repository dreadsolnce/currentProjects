#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys
from ubuntu import Ui_Form
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.list = []
        self.ui_main = Ui_Form()
        self.ui_main.setupUi(self)
        self.list_program()
        self.act_button()

    def list_program(self):
        self.list = ["pycharm-community", "qtdesigner"]
        for x in self.list:
            self.ui_main.comboBox.addItem(x)

    def act_button(self):
        print("Действие над кнопками в основном окне программы")
        self.ui_main.pushButton.clicked.connect(self.install)
        self.ui_main.pushButton_2.clicked.connect(self.remove)

    def install(self):
        self.act_program(act="install")

    def remove(self):
        self.act_program(act="remove")

    def act_program(self, act=None):
        if act == "install":
            print("Нажата кнопка установить")
            current_program = self.ui_main.comboBox.currentText()
            InstallProgram(program=current_program)
        elif act == "remove":
            print("Нажата кнопка удалить")
            current_program = self.ui_main.comboBox.currentText()
            UninstallProgram(program=current_program)
        QMessageBox.information(self, "Инфо", "Выполнено!", QMessageBox.Ok)


class InstallProgram(object):
    def __init__(self, program=None):
        super().__init__()
        self.program = program
        self.install()

    def install(self):
        print("Установка программы {}".format(self.program))
        if self.program == "pycharm-community":
            pass
        if self.program == "qtdesigner":
            proc = subprocess.Popen("sudo apt-get install python3-pyqt5 qtcreator "
                                    "pyqt5-dev-tools qttools5-dev-tools -y",
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if out.decode("utf-8"): print(out.decode("utf-8"))
            if err.decode('utf-8'): print(err.decode('utf-8'))


class UninstallProgram(object):
    def __init__(self, program=None):
        super().__init__()
        self.program = program
        self.uninstall()

    def uninstall(self):
        print("Удаление {}".format(self.program))
        if self.program == "pycharm-community":
            pass
        if self.program == "qtdesigner":
            proc = subprocess.Popen("sudo apt-get remove qtcreator "
                                    "pyqt5-dev-tools qttools5-dev-tools -y",
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if out.decode("utf-8"): print(out.decode("utf-8"))
            if err.decode('utf-8'): print(err.decode('utf-8'))


def main():
    print("Запуск функции main")
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    print("Запуск программы " + sys.argv[0])
    main()
