#!/usr/bin/python2
# -*- coding: utf8 -*-

import sys
from PyQt4 import QtGui, QtCore
sys.path.insert(0, 'GUI/')
import MainWindow


def main():
    """ """  
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow.MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()