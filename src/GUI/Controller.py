#!/usr/bin/python2
# -*- coding: utf8 -*-

import json
from os import listdir
from os.path import isfile, join


import HelpWidget
import OpenGLWidget

class Controller(object):
    """Controller will controll :
            - what widget is diplayed on the left part of the splitPane
            - what the statusBar show
        The controller also know all the scene"""
    def __init__(self,statusBar):
        self._statusBar = statusBar
        self._splitPane = None
        self._scene = {} # nom : obj-liste  (from assets/scene/)
        self._parseAllScene() #

    def initSplitPane(self,splitPane):
        """ """
        self._setStatusComputing()
        self._splitPane = splitPane
        self.glWidget = OpenGLWidget.OpenGLWidget(self._scene["Basic Scene"]) # name from json file
        self.helpWidget = HelpWidget.HelpWidget()
        self._setStatusReady()

    def showGL(self, item):
        """ """
        self._setStatusComputing()
        pass
        # TODO use item
        self._replaceRightWidget(self.glWidget)
        self._setStatusReady()

    def showHelp(self):
        """ """
        self._setStatusComputing()
        self._replaceRightWidget(self.helpWidget)
        self._setStatusReady()

    def getAllScene(self):
        """ """
        return self._scene

    def _parseAllScene(self):
        """ This method will assets/scene/ and add all the scene to a dictionnary"""
        mypath = "assets/scene/"
        scenesFiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
        for singleFile in scenesFiles:
            with open("assets/scene/basic.json", "r") as f:
                jasonDict = json.loads(f.read())
                name = jasonDict["name"]
                objects = jasonDict["obj-liste"]
                self._scene[name] = objects

    def _replaceRightWidget(self,newWidget):
        """ """
        self._splitPane.replaceRightWidget(newWidget)

    def _setStatusReady(self):
        """ """
        self._statusBar.showMessage("Ready!")

    def _setStatusComputing(self):
        """ """
        self._statusBar.showMessage("Computing ....")
