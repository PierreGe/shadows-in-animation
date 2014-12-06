#!/usr/bin/python2
# -*- coding: utf8 -*-


import math, random
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL,GLU
from objloader import OBJ


class OpenGLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent) 
        self.init()

    def init(self):
        # initial rotation
        self.xRot = 240
        self.yRot = -480
        self.zRot = 0

        self.lastPos = QtCore.QPoint()
 
        self.trolltechGreen = QtGui.QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QtGui.QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

    def xRotation(self):
        return self.xRot
 
    def yRotation(self):
        return self.yRot
 
    def zRotation(self):
        return self.zRot
 
    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)
 
    def sizeHint(self):
        return QtCore.QSize(400, 400)
 
    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.updateGL()
 
    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.updateGL()
 
    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.updateGL()
 
    def initializeGL(self):
        self.qglClearColor(self.trolltechPurple.dark())
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION,  (-40, 200, 100, 0.0))
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHTING)
        self.makeFloor()
        self.loadObjects()
 
    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, -19.0)
        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        GL.glColor3f(1,1,1)
        GL.glCallList(self.groundList)
        GL.glPushMatrix()
        GL.glTranslated(0,2,0)
        GL.glColor3f(1,0,0)
        for obj in self.objects:
            GL.glCallList(obj.gl_list)
        GL.glPopMatrix()
 
    def resizeGL(self, width, height):
        GL.glViewport(0, 0, width, height)
 
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-10, 10, -10, 10, 1, 37) # FRUSTUUUUUUUUM
 
        GL.glMatrixMode(GL.GL_MODELVIEW)
 
    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())
 
    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
 
        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)
 
        self.lastPos = QtCore.QPoint(event.pos())
 
    def wheelEvent(self, event):
        print 'La routourne va tourner...'

    def makeFloor(self):
        self.groundPoints = [-1,0,-1,-1,0,1,1,0,1,1,0,-1]
        self.groundList = GL.glGenLists(1)
        GL.glNewList(self.groundList, GL.GL_COMPILE)
        self.quadrilatere(*(([x*10 for x in self.groundPoints]) + [0,1,0]))
        GL.glEndList()

    def loadObjects(self):
        self.objects = []
        self.objects.append(OBJ("Stick_Figure_by_Swp.OBJ"))
 
    def quadrilatere(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, r, g, b): 
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex3d(x1, y1, z1)
        GL.glVertex3d(x2, y2, z2)
        GL.glVertex3d(x3, y3, z3)
        GL.glVertex3d(x4, y4, z4)
        GL.glEnd() 
 
    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle
