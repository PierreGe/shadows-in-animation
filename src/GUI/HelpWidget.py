#!/usr/bin/python2
# -*- coding: utf8 -*-

import os

from PyQt4 import QtGui, QtCore


class HelpWidget(QtGui.QWidget):
    """ """
    
    def __init__(self):
        """ """
        super(HelpWidget, self).__init__()

        self.initUI()
        
    def initUI(self):
        """ """
        hbox = QtGui.QHBoxLayout(self)

        self.textWidget = QtGui.QLabel(self)
        self.textWidget.setText(self._getStringHelp())
        self.textWidget.setStyleSheet(self._getStyleSheet());

        hbox.addWidget(self.textWidget)
        self.setLayout(hbox)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.show()

    def _getStyleSheet(self):
        """ """
        return open(os.getcwd() + "/GUI/text-help/text-help.css").read()

    def _getStringHelp(self):
        """ """
        return open(os.getcwd() +"/GUI/text-help/text-help.html").read()
