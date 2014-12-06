#!/usr/bin/python2
# -*- coding: utf8 -*-


import HelpWidget

import OpenGLWidget

import json


class Controller(object):
    """Controller will controll :
            - what widget is diplayed on the left part of the splitPane
            - what the statusBar show"""
    def __init__(self,statusBar):
        self._statusBar = statusBar
        self._splitPane = None

    def initSplitPane(self,splitPane):
        """ """
        self._setStatusComputing()
        self._splitPane = splitPane
        with open("assets/scene/basic.json", "r") as f:
            objects = json.loads(f.read())
        self.glWidget = OpenGLWidget.OpenGLWidget(objects)
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

    def _replaceRightWidget(self,newWidget):
        """ """
        self._splitPane.replaceRightWidget(newWidget)

    def _setStatusReady(self):
        """ """
        self._statusBar.showMessage("Ready!")

    def _setStatusComputing(self):
        """ """
        self._statusBar.showMessage("Computing ....")
