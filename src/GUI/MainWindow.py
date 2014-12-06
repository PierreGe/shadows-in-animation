#!/usr/bin/python2
# -*- coding: utf8 -*-

import sys
import os

from PyQt4 import QtGui, QtCore

import SplitPane
import Controller


class MainWindow(QtGui.QMainWindow):
    """ This class is the GUI's main class """
    def __init__(self):
        """Constructor of the class MainWindow"""
        super(MainWindow, self).__init__()
        # The GUI controller
        self._controller = None
        # init the GUI
        self.initUI()
        
    def initUI(self): 
        """ This methode will initiate the GUI :
        - The Menu bar
        - The toorls bar
        - The main SplitPane
        - The statusBar  
        """             
        # Windows title
        self.setWindowTitle("Les ombres au sein des jeux et des animations")

        self._statusBar = self.statusBar()
        self._controller = Controller.Controller(self._statusBar)

        ex = SplitPane.SplitPane(self._controller)
        self.setCentralWidget(ex)

        # si on veut mettre une bar en bas qui dit par exemple "Computing ..."

        self.initToolsBar()
        self.initMenu()
   
        self.showMaximized()

    def initMenu(self):
        """ This method will initate the menu """
        exitAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "images/application-exit.png"), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)


        fileMenu = menubar.addMenu('&Help')
        fileMenu.addAction(exitAction)

    def initToolsBar(self):
        """ This method will initate the toolsBar"""
        exitAction = QtGui.QAction(QtGui.QIcon('images/application-exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)


        
        
