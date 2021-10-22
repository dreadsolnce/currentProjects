#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from bginfo import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)
        self.ui_main.pushButton.setDisabled(True)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
