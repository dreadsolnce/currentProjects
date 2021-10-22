#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from bginfo import Ui_MainWindow


class MainWindow(QMainWindow):
    PATH_CONFIG = sys.path[0] + "/resources/config/"

    def __init__(self):
        super().__init__()
        self.path_config = MainWindow.PATH_CONFIG
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)
        self.show()
        self.act_buttons()

    def act_buttons(self):
        print("Действия над кнопками")
        self.ui_main.pushButton.clicked.connect(self.act_install)
        self.ui_main.pushButton_2.clicked.connect(self.act_uninstall)

    def act_install(self):
        print("Нажата кнопка установить")
        print("Каталог с конфигами:" + self.path_config)

    def act_uninstall(self):
        print("Нажата кнопка удалить")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
