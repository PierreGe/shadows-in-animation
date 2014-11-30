#!/usr/bin/python2
# -*- coding: utf8 -*-


import HelpWidget

import OpenGLWidget


class SelectionController(object):
    """docstring for SelectionController"""
    def __init__(self,splitPane):
        self._splitPane = splitPane

    def swichTo(self,item):
        """ """
        # TODO : determiner comment les openGL vont être stocké
        pass
        self._replaceRightWidget(OpenGLWidget.OpenGLWidget())

    def showHelp(self):
        """ """
        self._replaceRightWidget(HelpWidget.HelpWidget())

    def _replaceRightWidget(self,newWidget):
        """ """
        self._splitPane.replaceRightWidget(newWidget)
