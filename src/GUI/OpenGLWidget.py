#!/usr/bin/python2
# -*- coding: utf8 -*-


import math, random
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL,GLU
from OpenGL.GL import shaders
from ObjParser import ObjParser

from cgkit.cgtypes import mat4,vec3
from Camera import Camera
from Light import Light       


class OpenGLWidget(QtOpenGL.QGLWidget):
    """ docstring """
    def __init__(self, object_names = [], parent=None):
        """ docstring """
        QtOpenGL.QGLWidget.__init__(self, parent)
        self._camera = Camera()
        self._light = Light()
        self._object_names = object_names

    def getObjectNames(self):
        """ Reload openGLWidget """
        return self._object_names

    def setObjects(self, object_names):
        """ docstring """
        for index, obj in enumerate(self.objects, 1):
            GL.glDeleteLists(index, GL.GL_COMPILE)
        self._object_names = object_names
        self.loadObjects()

    # ---------- Partie : Qt ------------
 
    def minimumSizeHint(self):
        """ docstring """
        return QtCore.QSize(50, 50)
 
    def sizeHint(self):
        """ docstring """
        return QtCore.QSize(400, 400)
 
    def setXRotation(self, angle):
        """ docstring """
        res = self._camera.setX(angle)
        if res:
            self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.updateGL()
 
    def setYRotation(self, angle):
        """ docstring """
        res = self._camera.setY(angle)
        if res:
            self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.updateGL()
 
    def setZRotation(self, angle):
        """ docstring """
        res = self._camera.setZ(angle)
        if res:
            self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.updateGL()

        # Events
    def mousePressEvent(self, event):
        """ This method is called when there is a click """
        self.lastPos = QtCore.QPoint(event.pos())
 
    def mouseMoveEvent(self, event):
        """ This method is called when there is a mouse (drag) event"""
        smoothFactor = 10
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        dx = int(dx/smoothFactor)
        dy = int(dy/smoothFactor)
        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self._camera.getX() + 8 * dy)
            self.setYRotation(self._camera.getY() + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self._camera.getX() + 8 * dy)
            self.setZRotation(self._camera.getZ() + 8 * dx)
        self.lastPos = QtCore.QPoint(event.pos())
 
    def wheelEvent(self, event):
        """ docstring """
        # TODO réparer le zoom, utiliser les frustums
        self.zoom += event.delta()/100.0
        self.updateGL()

    def updateLights(self,position):
        """ """
        self._light.setLightsRatio(position)
        self.updateGL()


    # ---------- Partie : Opengl ------------
 
    # Called at startup
    def initializeGL(self):
        """ docstring """
        self.fbo = 0;
        self.textureBuffer = 0;
        self.renderBuffer = 0
        # initial rotation
        self.zoom = -20

        # save mouse cursor position for smooth rotation
        self.lastPos = QtCore.QPoint()

        # save mouse cursor position for smooth rotation
        self.lastPos = QtCore.QPoint()

        # create floor and load .obj objects
        self.makeFloor()
        self.loadObjects()

    # Objects construction methods
    def makeFloor(self):
        """ docstring """
        self.groundPoints = [-1,0,-1,-1,0,1,1,0,1,1,0,-1]
        self.groundList = GL.glGenLists(1)
        GL.glNewList(self.groundList, GL.GL_COMPILE)
        self.quadrilatere(*(([x*10 for x in self.groundPoints])))
        GL.glEndList()

    def loadObjects(self):
        """ docstring """
        self.objects = []
        for index, obj in enumerate(self._object_names, 1):
            self.objects.append((ObjParser(obj[0]).build(index), obj[1]))
 
    # Called on each update/frame
    def paintGL(self):
        """ docstring """
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        # reload new matrix
        GL.glLoadIdentity()
        # zoom out camera
        GL.glTranslated(0, 0, self.zoom)
        # apply rotation
        GL.glRotated(self._camera.getX(), 1, 0, 0)
        GL.glRotated(self._camera.getY(), 0, 1, 0)
        GL.glRotated(self._camera.getZ(), 0, 0, 1)
        # paint objects
        self._light.renderLight()
        self.paintFloor()
        self.paintObjects()
    def paintFloor(self):
        """ docstring """
        GL.glColor4f(1.0,1.0,1.0,1.0) # WHITE
        GL.glCallList(self.groundList)

    def paintObjects(self):
        """ docstring """
        #GL.glColor3f(1,0,0) # RED
        for obj in self.objects:
            GL.glPushMatrix()
            GL.glTranslated(*obj[1])
            GL.glCallList(obj[0])
            GL.glPopMatrix()

 
    # Called when window is resized
    def resizeGL(self, width, height):
        """ docstring """
        GL.glViewport(0, 0, width, height)
 
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-10, 10, -10, 10, 1, 37) # FRUSTUUUUUUUUM
 
        GL.glMatrixMode(GL.GL_MODELVIEW)

 
    # Work methods
    def quadrilatere(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4): 
        """ docstring """
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex3d(x1, y1, z1)
        GL.glVertex3d(x2, y2, z2)
        GL.glVertex3d(x3, y3, z3)
        GL.glVertex3d(x4, y4, z4)
        GL.glEnd()
 