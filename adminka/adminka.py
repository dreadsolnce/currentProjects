#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import resources

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget

"""
    Программа для настройки и администрирования 
    ОС семейства Linux (Ubuntu, AstraLinux)
"""


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.gui = resources.Ui_MainWindow()
        self.gui.setupUi(self)
        # Задание параметров treeWidget
        self.gui.treeWidget.setVisible(False)
        self.gui.treeWidget.setIndentation(2)
        # Центрирование окна
        self.winCenter()

        self.show()
        self.action()

    def action(self):
        self.gui.actionUbuntu_21_10.triggered.connect(self.clkActUbuntu)
        self.gui.action_Exit.triggered.connect(lambda: sys.exit())

    def clkActUbuntu(self):
        self.gui.treeWidget.setVisible(True)

    # Центрирование окна относительно экрана
    def winCenter(self):
        qr = self.frameGeometry()
        qp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(qp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app1 = MainWindow()
    sys.exit(app.exec_())
