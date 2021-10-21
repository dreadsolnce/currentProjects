#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
from bginfo import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_main = Ui_MainWindow()
        ui_main.setupUi(self)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
