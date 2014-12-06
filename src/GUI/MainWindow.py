#!/usr/bin/python2
# -*- coding: utf8 -*-

import sys
from PyQt4 import QtGui, QtCore

import SplitPane

class MainWindow(QtGui.QMainWindow):
    """ This class is the GUI's main class """
    def __init__(self):
        """Constructor of the class MainWindow"""
        super(MainWindow, self).__init__()
        self.initUI()
        
    def initUI(self): 
        """ This methode will initiate the GUI :
        The Menu bar
        The toorls bar
        The main SplitPane
        The statusBar  """             
        # Windows title
        self.setWindowTitle("Les ombres au sein des jeux et des animations")

        ex = SplitPane.SplitPane()
        self.setCentralWidget(ex)

        # si on veut mettre une bar en bas qui dit par exemple "Computing ..."
        #statusBar = self.statusBar()

        self.initToolsBar()
        self.initMenu()
   
        self.showMaximized()

    def initToolsBar(self):
        """ """
        exitAction = QtGui.QAction(QtGui.QIcon('images/application-exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)


        fileMenu = menubar.addMenu('&Help')
        fileMenu.addAction(exitAction)

    def initMenu(self):
        """ """
        exitAction = QtGui.QAction(QtGui.QIcon('images/application-exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        
        
