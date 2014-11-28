#!/usr/bin/python2
# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore

import TreeWidget
import OpenGLWidget

class SplitPane(QtGui.QWidget):
    
    def __init__(self):
        super(SplitPane, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        hbox = QtGui.QHBoxLayout(self)

        left = TreeWidget.TreeWidget()

        right = OpenGLWidget.OpenGLWidget()

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 0)
        splitter.addWidget(left)
        splitter.addWidget(right)


        hbox.addWidget(splitter)
        self.setLayout(hbox)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        #self.setGeometry(300, 300, 300, 200)
        #self.setWindowTitle('QtGui.QSplitter')
        self.show()
