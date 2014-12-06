#!/usr/bin/python2
# -*- coding: utf8 -*-


import HelpWidget

import OpenGLWidget


class SelectionController(object):
    """docstring for SelectionController"""
    def __init__(self, splitPane):
        self._splitPane = splitPane
        self.glWidget = OpenGLWidget.OpenGLWidget([("Stick_Figure_by_Swp.OBJ", (0,0,0))])
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
