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
        self._controller = Controller.Controller()
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
        self._controller.initStatusBar(self._statusBar)

        ex = SplitPane.SplitPane(self._controller)
        self.setCentralWidget(ex)

        self.initToolsBar()
        self.initMenu()
   
        self.showMaximized()

    def displayHelp(self):
        """ """
        QtGui.QMessageBox.information(self, "Aide", "Printemps des sciences 2015")

    def displayAbout(self):
        """ Display some info"""
        QtGui.QMessageBox.information(self, "A propos", "Printemps des sciences 2015")

    def initMenu(self):
        """ This method will initate the menu """
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Fichier')
        helpMenu = menubar.addMenu("&Aide")

        exitAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" + "images/application-exit.png"), 'Quitter', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        aboutAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" + "images/help-browser.png"), "Aide", self)
        aboutAction.setStatusTip("Aide pour cette application")
        aboutAction.triggered.connect(self.displayAbout)
        helpMenu.addAction(aboutAction)

        aboutAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" + "images/dialog-information.png"), "A propos", self)
        aboutAction.setStatusTip("A propos de cette application")
        aboutAction.triggered.connect(self.displayAbout)
        helpMenu.addAction(aboutAction)

    def reloadOpenGl(self):
        """ """
        self._controller.reload()

    def initToolsBar(self):
        """ This method will initate the toolsBar"""
        toolbar = self.addToolBar("Tool Bar")

        reloadAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" +"images/system-reload.png"), "Reload", self)
        reloadAction.setShortcut("Ctrl+R")
        reloadAction.setStatusTip("Reload application")
        reloadAction.triggered.connect(self.reloadOpenGl)
        toolbar.addAction(reloadAction)

        exitAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" +"images/application-exit.png"), "Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit application")
        exitAction.triggered.connect(self.close)
        toolbar.addAction(exitAction)

        toolbar.addSeparator()

        textWidget = QtGui.QLabel(self)
        textWidget.setText("Position lumière :  X ".decode("utf8"))
        toolbar.addWidget(textWidget)


        sliderX = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderX.valueChanged.connect(self._controller.lightPercentX)
        sliderX.setSliderPosition(99)
        toolbar.addWidget(sliderX)


        textWidget = QtGui.QLabel(self)
        textWidget.setText("  Z ")
        toolbar.addWidget(textWidget)

        sliderZ = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderZ.valueChanged.connect(self._controller.lightPercentZ)
        sliderZ.setSliderPosition(99)
        toolbar.addWidget(sliderZ)


        textWidget = QtGui.QLabel(self)
        textWidget.setText("  Hauteur ")
        toolbar.addWidget(textWidget)

        sliderY = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderY.valueChanged.connect(self._controller.lightPercentY)
        sliderY.setSliderPosition(99)
        toolbar.addWidget(sliderY)

        # un espace blanc
        textWidget = QtGui.QLabel(self)
        textWidget.setText(" "* 100)
        toolbar.addWidget(textWidget)



        
        
