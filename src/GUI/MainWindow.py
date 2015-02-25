#!/usr/bin/python2
# -*- coding: utf8 -*-

import sys
import os

from PyQt4 import QtGui, QtCore
from OpenGL import GL

import SplitPane
import Controller
import LightPanel
import HelpWidget


class MainWindow(QtGui.QMainWindow):
    """ This class is the GUI's main class """
    def __init__(self):
        """Constructor of the class MainWindow"""
        super(MainWindow, self).__init__()
        # The GUI controller
        self._controller = Controller.Controller(self)
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

    def closeApp(self):
        """ """
        self.close()
        self._controller.killThreads()
        #exit()
        #os.system("kill -9 " + os.getpid()) # hihi

    def displayHelp(self):
        """ """
        QtGui.QMessageBox.information(self, "Aide", "Printemps des sciences 2015")

    def displayAbout(self):
        """ Display some info"""
        QtGui.QMessageBox.information(self, "A propos", "- Pierre Gerard, Bruno Rocha Pereira, Antoine Carpentier" + "\n" + "- Dans ce projet nous examinons le domaine des algorithmes de rendu d'ombre et nous en comparerons quelques-uns dans un environnement de simulation 3D comme le OpenGL. Le but est de tester leurs aspects positifs et négatifs et de voir les conditions dans lesquelles ils donnent le meilleur rendu.")

    def initMenu(self):
        """ This method will initate the menu """
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Fichier')
        helpMenu = menubar.addMenu("&Aide")

        exitAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" + "images/application-exit.png"), 'Quitter', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.closeApp)
        fileMenu.addAction(exitAction)

        aboutAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" + "images/help-browser.png"), "Aide", self)
        aboutAction.setStatusTip("Aide pour cette application")
        aboutAction.triggered.connect(self.displayHelp)
        helpMenu.addAction(aboutAction)

        aboutAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" + "images/dialog-information.png"), "A propos", self)
        aboutAction.setStatusTip("A propos de cette application")
        aboutAction.triggered.connect(self.displayAbout)
        helpMenu.addAction(aboutAction)

    def reloadOpenGl(self):
        """ """
        self._controller.reload()

    def addALight(self):
        """ """
        self.l = LightPanel.AddLightPanel(self._controller)

    def removeALight(self):
        """ """
        self.l = LightPanel.RemoveLightPanel(self._controller)


    def animateLight(self):
        """ """
        self._controller.switchLightAnimation()

    def animateCamera(self):
        """ """
        self._controller.switchCameraAnimation()


    def showHardwareVersion(self):
        """ Display opengl and shading version"""
        helper = self._controller.getOpenGlVersionHelper()
        vendor = helper.getVendor()
        renderer = helper.getRenderer()
        shadingVersion = helper.getShadingVersion()
        openglVersion = helper.getOpenGlVersion()
        if isinstance(shadingVersion, str) and isinstance(openglVersion, str):
            QtGui.QMessageBox.information(self,"Materiel graphique","Vendeur : " + vendor + "\n" + "Renderer : " + renderer + "\n" + "OpenGL : " + openglVersion + "\n" + "GLSL : " + shadingVersion)
        else:
            print("GL not initialized")

    def onTypeSelection(self):
        """ """
        pass


    def initToolsBar(self):
        """ This method will initate the toolsBar"""
        self.toolbar = self.addToolBar("Tool Bar")

        exitAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" +"images/application-exit.png"), "Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Quitter l'application")
        exitAction.triggered.connect(self.closeApp)
        self.toolbar.addAction(exitAction)

        reloadAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" +"images/system-reload.png"), "Reload", self)
        reloadAction.setShortcut("Ctrl+R")
        reloadAction.setStatusTip("Recharge l'application")
        reloadAction.triggered.connect(self.reloadOpenGl)
        self.toolbar.addAction(reloadAction)

        self.toolbar.addSeparator()

        hardwareHelpAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" +"images/hwinfo.png"), "Montre la version du hardware graphique", self)
        hardwareHelpAction.setStatusTip("Montre la version du hardware graphique")
        hardwareHelpAction.triggered.connect(self.showHardwareVersion)
        self.toolbar.addAction(hardwareHelpAction)


        self.toolbar.addSeparator()


        animationActionCamera = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" +"images/tool-animator-camera.png"), "Animation de la camera", self)
        animationActionCamera.setStatusTip("Animation de la camera")
        animationActionCamera.triggered.connect(self.animateCamera)
        self.toolbar.addAction(animationActionCamera)




        self.toolbar.addSeparator()

        addLightAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" +"images/lightBublePlus.png"), "Light+", self)
        addLightAction.setShortcut("Ctrl+L")
        addLightAction.setStatusTip("Ajouter une lampe")
        addLightAction.triggered.connect(self.addALight)
        self.toolbar.addAction(addLightAction)


        removeLightAction = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" +"images/lightBubleMinus.png"), "Light-", self)
        #removeLightAction.setShortcut("Ctrl+L")
        removeLightAction.setStatusTip("Retirer une lampe")
        removeLightAction.triggered.connect(self.removeALight)
        self.toolbar.addAction(removeLightAction)



        self.toolbar.addSeparator()
        self.toolbar.addSeparator()

        lightCollection = self._controller.getLightCollection()
        if len(lightCollection) > 0:
            self._choiceType = "0 Default"
            combo = QtGui.QComboBox(self)
            for lightIndex in range(len(lightCollection)):
                string = "Lampe "+ str(lightIndex+1)
                
                combo.addItem(string)
            combo.activated[str].connect(self.onTypeSelection)
        
        self.toolbar.addWidget(combo)

        self.toolbar.addSeparator()

        animationActionLight = QtGui.QAction(QtGui.QIcon(os.getcwd() + "/assets/" +"images/tool-animator-light.png"), "Animation des lampes", self)
        animationActionLight.setStatusTip("Animation des lampes")
        animationActionLight.triggered.connect(self.animateLight)
        self.toolbar.addAction(animationActionLight)

        self.toolbar.addSeparator()


        textWidget = QtGui.QLabel(self)
        textWidget.setText("  Position lumière :  X ".decode("utf8"))
        self.toolbar.addWidget(textWidget)


        sliderX = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderX.valueChanged.connect(self._controller.lightPercentX)
        sliderX.setSliderPosition(99)
        self.toolbar.addWidget(sliderX)


        textWidget = QtGui.QLabel(self)
        textWidget.setText("  Z ")
        self.toolbar.addWidget(textWidget)

        sliderZ = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderZ.valueChanged.connect(self._controller.lightPercentZ)
        sliderZ.setSliderPosition(99)
        self.toolbar.addWidget(sliderZ)


        textWidget = QtGui.QLabel(self)
        textWidget.setText("  Hauteur ")
        self.toolbar.addWidget(textWidget)

        sliderY = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sliderY.valueChanged.connect(self._controller.lightPercentY)
        sliderY.setSliderPosition(99)
        self.toolbar.addWidget(sliderY)

        # un espace blanc
        textWidget = QtGui.QLabel(self)
        textWidget.setText(" "* 10)
        self.toolbar.addWidget(textWidget)


    def updateToolsBar(self):
        """ """
        self.toolbar.hide()
        self.initToolsBar()
        
        
