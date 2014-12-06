#!/usr/bin/python2
# -*- coding: utf8 -*-


import HelpWidget

import OpenGLWidget

import json


class SelectionController(object):
    """docstring for SelectionController"""
    def __init__(self, splitPane):
        self._splitPane = splitPane
        with open("assets/scene/basic.json", "r") as f:
            j = json.loads(f.read())
            print j
        self.glWidget = OpenGLWidget.OpenGLWidget(j)
        self.helpWidget = HelpWidget.HelpWidget()

    def showGL(self, item):
        """ """
        pass
        # TODO use item
        self._replaceRightWidget(self.glWidget)

    def showHelp(self):
        """ """
        self._replaceRightWidget(self.helpWidget)

    def _replaceRightWidget(self,newWidget):
        """ """
        self._splitPane.replaceRightWidget(newWidget)
