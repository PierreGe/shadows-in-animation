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
        self._statusBar.showMessage('Welcome!')
        self._controller = Controller.Controller(self._statusBar)

        ex = SplitPane.SplitPane(self._controller)
        self.setCentralWidget(ex)

        self.initToolsBar()
        self.initMenu()
   
        self.showMaximized()

    def displayAbout(self):
        """ Display some info"""
        QtGui.QMessageBox.information(self, "A propos", "Printemps des sciences 2015")

    def initMenu(self):
        """ This method will initate the menu """
        exitAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/GUI/" + "images/application-exit.png"), 'Quitter', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Fichier')
        fileMenu.addAction(exitAction)


        helpMenu = menubar.addMenu("&Aide")
        aboutAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/GUI/" + "images/application-exit.png"), "A propos", self)
        aboutAction.setStatusTip("A propos de cette application")
        aboutAction.triggered.connect(self.displayAbout)
        helpMenu.addAction(aboutAction)

    def initToolsBar(self):
        """ This method will initate the toolsBar"""
        exitAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/GUI/" +'images/application-exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)


        
        
