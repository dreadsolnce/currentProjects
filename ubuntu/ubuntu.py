#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources
import subprocess
import sys
import threading
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
        self.list = ["pycharm-community", "qtdesigner", "timeshift"]
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
        self.command = None
        self.install()

    def install(self):
        print("Установка программы {}".format(self.program))
        if self.program == "pycharm-community":
            self.command = "sudo snap install pycharm-community --classic"
        if self.program == "qtdesigner":
            self.command = "sudo apt-get install python3-pyqt5 qtcreator pyqt5-dev-tools qttools5-dev-tools -y"
        if self.program == "timeshift":
            self.command = "sudo apt-get install timeshift -y"
        t = threading.Thread(target=action_program, name="install_timeshift",
                             args=(self.command,))
        t.start()
        t.join()


class UninstallProgram(object):
    def __init__(self, program=None):
        super().__init__()
        self.command = None
        self.program = program
        self.uninstall()

    def uninstall(self):
        print("Удаление {}".format(self.program))
        if self.program == "pycharm-community":
            print("Не поддерживается удаление!")
        if self.program == "qtdesigner":
            self.command = "sudo apt-get remove qtcreator pyqt5-dev-tools qttools5-dev-tools -y"
        if self.program == "timeshift":
            self.command = "sudo apt-get remove timeshift -y"
        if self.command:
            t = threading.Thread(target=action_program, name="install_timeshift",
                                 args=(self.command,))
            t.start()
            t.join()


def action_program(command):
    st = True
    if command:
        proc = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        while st:
            st = proc.stdout.readline()
            print(st.decode("utf-8"), end="")
        # out, err = proc.communicate()
        # if out.decode("utf-8"): print(out.decode("utf-8"))
        # if err.decode('utf-8'): print(err.decode('utf-8'))


# Проверка зависимостей для запуска программы
def dependency_checking():
    print("Запуск функции проверки установленных зависимостей!")
    state_pack = False
    for d in pkg_resources.working_set:
        if str(d).split()[0] == "PyQt5":
            print("Пакет PyQt5 уже установлен в системе!")
            state_pack = True
    if not state_pack:
        print("Устанавливаем необходимые зависимости!")
        action_program(command="sudo apt-get install python3-pyqt5 -y")


def main():
    print("Запуск функции main")
    dependency_checking()
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    print("Запуск программы " + sys.argv[0])
    main()
