#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL import GL
from OpenGL.GLUT import *
from OpenGL.GLU import *

class OpenGlVersionHelper(object):
    """Check the hardware compatibility"""
    def __init__(self):
        # init GL
        glutInit([])
        window = glutCreateWindow("version")
        glutHideWindow()
        self._vendor = GL.glGetString(GL.GL_VENDOR)
        self._renderer = GL.glGetString(GL.GL_RENDERER)
        self._shadingVersion = GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)
        self._openglVersion = GL.glGetString(GL.GL_VERSION)
        glutDestroyWindow(window)

    def getVendor(self):
        """ """
        return self._vendor

    def getRenderer(self):
        """ """
        return self._renderer

    def getShadingVersion(self):
        """ """
        return self._shadingVersion

    def getOpenGlVersion(self):
        """ """
        return self._openglVersion
        