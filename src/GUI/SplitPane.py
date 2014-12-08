#!/usr/bin/python2
# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore

import TreeWidget
import HelpWidget


class SplitPane(QtGui.QWidget):
    """ """
    
    def __init__(self, controller ):
        """ """
        super(SplitPane, self).__init__()

        self._controller = controller
        self._controller.initSplitPane(self)

        
        self.splitter = None
        self.right = None
        self.left = None

        self.initUI()
        
    def initUI(self):
        """ this method will intiate the splitpane"""
        hbox = QtGui.QHBoxLayout(self)

        self.left = TreeWidget.TreeWidget(self._controller)

        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

        self.splitter.addWidget(self.left)
        self._controller.showHelp()

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
        if (self.right):
            self.right.hide()
            self.right.setParent(None)
        newWidget.show()
        self.right = newWidget
        self.splitter.addWidget(newWidget)
        self._resize()




