#!/usr/bin/python
# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore


class SplitPane(QtGui.QWidget):
    
    def __init__(self):
        super(SplitPane, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        hbox = QtGui.QHBoxLayout(self)

        left = QtGui.QTextEdit()
        left.setFrameShape(QtGui.QFrame.StyledPanel)
 
        right = QtGui.QTextEdit()
        right.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)


        hbox.addWidget(splitter)
        self.setLayout(hbox)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QSplitter')
        self.show()