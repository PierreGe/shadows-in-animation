#!/usr/bin/python2
# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore

import TreeWidget
import OpenGLWidget
import OpenGLWidgetv2

class SplitPane(QtGui.QWidget):
    
    def __init__(self):
        super(SplitPane, self).__init__()
        
        self.splitter = None
        self.right = None
        self.left = None

        self.initUI()
        
    def initUI(self):      

        hbox = QtGui.QHBoxLayout(self)

        self.left = TreeWidget.TreeWidget()

        self.right = OpenGLWidget.OpenGLWidget()

        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

        self.splitter.addWidget(self.left)
        self.splitter.addWidget(self.right)

        #set a proportion between the tree and the openGL example
        self.splitter.setSizes([50,600])


        hbox.addWidget(self.splitter)
        self.setLayout(hbox)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.show()

        #self.replaceRightChild(OpenGLWidgetv2.OpenGLWidget())

    def replaceRightChild(self,openglWidget):

        self.right.hide()
        self.right.setParent(None)
        del(self.right)
        self.splitter.addWidget(openglWidget)
