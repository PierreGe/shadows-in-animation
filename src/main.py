#!/usr/bin/python2
# -*- coding: utf8 -*-

import sys
from GUI import MainWindow
from PyQt4 import QtGui, QtCore
from Utils import requirement


def main():
    """ """
    requirement.check()
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow.MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()