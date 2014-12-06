#!/usr/bin/python2
# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore

import TreeWidget
import SelectionController
import HelpWidget


class SplitPane(QtGui.QWidget):
    """ """
    
    def __init__(self):
        """ """
        super(SplitPane, self).__init__()

        self._selectController = SelectionController.SelectionController(self)
        
        self.splitter = None
        self.right = None
        self.left = None

        self.initUI()
        
    def initUI(self):
        """ """
        hbox = QtGui.QHBoxLayout(self)

        self.left = TreeWidget.TreeWidget(self._selectController)

        self.right = HelpWidget.HelpWidget()

        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

        self.splitter.addWidget(self.left)
        self.splitter.addWidget(self.right)

        self._resize()


        hbox.addWidget(self.splitter)
        self.setLayout(hbox)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.show()

        #self.replaceRightChild(OpenGLWidgetv2.OpenGLWidget())

    def _resize(self):
        """ set a proportion """
        self.splitter.setSizes([50,600])

    def replaceRightWidget(self,newWidget):
        """ """
        self.right.hide()
        self.right.setParent(None)
        newWidget.show()
        self.right = newWidget
        self.splitter.addWidget(newWidget)
        self._resize()




