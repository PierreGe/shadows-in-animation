#!/usr/bin/python2
# -*- coding: utf8 -*-


import math, random
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL,GLU


class OpenGLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
 
        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
 
        self.rep1=6
        self.rep2=6
 
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
        self.object = self.makeObject()
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
#        GL.glEnable(GL.GL_CULL_FACE)
 
    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, -19.0)
        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        GL.glCallList(self.object)
 
    def resizeGL(self, width, height):
        side = min(width, height)
        GL.glViewport((width - side) / 2, (height - side) / 2, side, side)
 
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-6, 6, -6, 6, 1, 37)
#  http://www.talisman.org/opengl-1.1/Reference/glOrtho.html
 
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
        print 'La roue tourne...'
 
 
    def makeObject(self):
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)
 
        f=[]
        NGrille=100
 
        for i in range(NGrille+1):
            z=[]
            for j in range(NGrille+1):
                z.append(5*math.sin(-5+10.0*i/NGrille) * math.cos(-5+10.0*j/NGrille))
            f.append(z)
 
#        print f
#        print f[0][0]
 
        for i in range(1,NGrille+1):
            for j in range(1,NGrille+1):
#                print 'i, j = ' +str((i,j))
#                print (-5+10.0*(i-1)/NGrille, -5+10.0*(j-1)/NGrille)
# Attention, on doit taper "+10.0*" car sinon la division est euclidienne.
                couleur = self.degrade(-6, 6, f[i][j])
 
                self.quadrilatere(-5+10.0*(i-1)/NGrille, -5+10.0*(j-1)/NGrille, f[i-1][j-1],
                -5+10.0*i/NGrille, -5+10.0*(j-1)/NGrille, f[i][j-1],
                -5+10.0*i/NGrille, -5+10.0*j/NGrille, f[i][j],
                -5+10.0*(i-1)/NGrille, -5+10.0*j/NGrille, f[i-1][j],
                couleur[0], couleur[1], couleur[2])
 
        GL.glEndList()
 
        return genList
 
    def degrade(self, zMin, zMax ,zActuel):
# Cas d'un degrade un peu chauvin avec trois couleurs
        Couleur1 = [255, 0, 255]
        Couleur2 = [255, 255, 255]
        Couleur3 = [255, 0, 0]
 
        k = 100.0*(zMax-zActuel)/(zMax - zMin)
 
        if k <= 50:
            c = k / 50.0
 
            r = math.floor(Couleur1[0] + (Couleur2[0] - Couleur1[0])* c)
            g = math.floor(Couleur1[1] + (Couleur2[1] - Couleur1[1])* c)
            b = math.floor(Couleur1[2] + (Couleur2[2] - Couleur1[2])* c)
 
        else:
            c = (k - 50) / 50.0
 
            r = math.floor(Couleur2[0] + (Couleur3[0] - Couleur2[0])* c)
            g = math.floor(Couleur2[1] + (Couleur3[1] - Couleur2[1])* c)
            b = math.floor(Couleur2[2] + (Couleur3[2] - Couleur2[2])* c)
 
        return [r, g, b]
 
    def quadrilatere(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, r, g, b):
        self.qglColor(QtGui.QColor(r,g,b))
 
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex3d(x1, y1, z1)
        GL.glVertex3d(x2, y2, z2)
        GL.glVertex3d(x3, y3, z3)
        GL.glVertex3d(x4, y4, z4)
        GL.glEnd()
 
#        print '\nPoint 1 :'
#        print (x1, y1, z1)
#        print '\nPoint 2 :'
#        print (x2, y2, z2)
#        print '\nPoint 3 :'
#        print (x3, y3, z3)
#        print '\nPoint 4 :'
#        print (x4, y4, z4)
 
 
 
 
    def extrude(self, x1, y1, x2, y2):
        self.qglColor(self.trolltechGreen.dark(250 + int(100 * x1)))
 
        GL.glVertex3d(x1, y1, +0.05)
        GL.glVertex3d(x2, y2, +0.05)
        GL.glVertex3d(x2, y2, -0.05)
        GL.glVertex3d(x1, y1, -0.05)
 
    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle
