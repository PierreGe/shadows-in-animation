#!/usr/bin/python2
# -*- coding: utf8 -*-

import os


from PyQt4 import QtGui, QtCore


class HelpWidget(QtGui.QWidget):
    """ Widget contenant un QLabel contenant l'aide du projet"""
    
    def __init__(self):
        """ Constructeur"""
        super(HelpWidget, self).__init__()

        self.textWidget = None

        self.initUI()
        
    def initUI(self):
        """ Intialise la UI du HelpWidget"""
        hbox = QtGui.QHBoxLayout(self)

        self.textWidget = QtGui.QLabel(self)

        self.textWidget.setMinimumSize(200, 200)
        self.textWidget.setAlignment(QtCore.Qt.AlignLeft)
        self.textWidget.setAcceptDrops(True)
        self.textWidget.setAutoFillBackground(True)

        self.textWidget.clear()

        self.textWidget.setText(self._getStringHelp())
        self.textWidget.setStyleSheet(self._getStyleSheet())

        self.textWidget.show()

        hbox.addWidget(self.textWidget)
        self.setLayout(hbox)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.show()

    def _getStyleSheet(self):
        """ Retourne la feuille de style du QLabel"""
        return open(os.getcwd() + "/assets/text-help/text-help.css").read().decode('utf-8')

    def _getStringHelp(self):
        """ Retourne le code html du QLabel"""
        return open(os.getcwd() +"/assets/text-help/text-help.html").read().decode('utf-8')
