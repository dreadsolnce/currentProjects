#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import resources

from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow, resources.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        gui = resources.Ui_MainWindow()
        gui.setupUi(self)
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app1 = MainWindow()
    sys.exit(app.exec_())
