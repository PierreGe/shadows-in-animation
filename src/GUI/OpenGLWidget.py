#!/usr/bin/python2
# -*- coding: utf8 -*-


import math, random
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL,GLU
import ObjParser


class Camera(object):
    """docstring for Camera"""
    def __init__(self):
        """ Constructeur de la classe Camera"""
        self._x = 20
        self._xInterval = [20,60]
        self._y = 352
        self._z = 6

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getZ(self):
        return self._z

    def setX(self,x):
        """ """
        x = self.normalizeAngle(x)
        if x < self._xInterval[0]:
            x = self._xInterval[0]
        elif x > self._xInterval[1]:
            x = self._xInterval[1]
        if x != self._x:
            self._x = x
            return True
        return False

    def setY(self,y):
        """ """
        y = self.normalizeAngle(y)
        if y != self._y:
            self._y = y
            return True
        return False

    def setZ(self,z):
        """ """
        z = self.normalizeAngle(z)
        if z != self._z:
            self._z = z
            return True
        return False

    def normalizeAngle(self, angle):
        """ Keep angle between 0 and 360"""
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        return angle


class Light(object):
    """docstring for Light"""
    def __init__(self):
        self._xInterval = [-20,20]
        self._yInterval = [0,30]
        self._zInterval = [-20,20]
        xInit = (self._xInterval[1])
        yInit = (self._yInterval[1])
        zInit = (self._zInterval[1])
        self.setLights([xInit, yInit, zInit])

    def resetLight(self):
        """ """
        self.__init__()

    def getPosition(self):
        return self._position

    def setLights(self,position):
        "light with a custom position"
        
        self._position = list(position)
        self._position.append(1.0)


    def setLightsRatio(self,positionPercent):
        "light with a custom position"
        x = self._xInterval[0] + (float(positionPercent[0])/100 * ( abs(self._xInterval[0]) + abs(self._xInterval[1])))
        y = self._yInterval[0] + (float(positionPercent[1])/100 * ( abs(self._yInterval[0]) + abs(self._yInterval[1])))
        z = self._zInterval[0] + (float(positionPercent[2])/100 * ( abs(self._zInterval[0]) + abs(self._zInterval[1])))
        #print("{0}, {1}, {2}".format(x,y,z))
        self.setLights([x,y,z])

    def renderLight(self):
        """ """
        if not self._position:
            print("[ERROR] Light position not set !")

        GL.glPushMatrix()
        GL.glDisable(GL.GL_LIGHTING)
        GL.glPointSize(5.0)
        GL.glBegin(GL.GL_POINTS)
        GL.glColor4f(1,0.475, 0.294, 1) # yellow-orrange point
        GL.glVertex4fv(self._position)
        GL.glEnd()
        GL.glPopMatrix() 

        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, ( 1.0,1.0,1.0,1.0 )) 
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, ( 0.6,0.6,0.6,1.0 )) 
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, ( 0.1,0.1,0.1,1.0 ))
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, self._position)

        GL.glLightf(GL.GL_LIGHT0, GL.GL_CONSTANT_ATTENUATION, 1.0)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHTING)
        


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
        for obj in self.objects:
            GL.glDeleteLists(1, GL.GL_COMPILE)
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

    def _shadowMap(self):
        GL.glDepthFunc(GL.GL_LESS)
        GL.glEnable(GL.GL_DEPTH_TEST)

        self.fbo = GL.glGenFramebuffers(1);
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo);
        # GL.glDeleteFramebuffers(1, self.fbo);

        GL.glGenTextures(1, self.textureBuffer);
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.textureBuffer);
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_DEPTH_COMPONENT, 640, 480, 0, GL.GL_DEPTH_COMPONENT, GL.GL_UNSIGNED_BYTE, None)

        GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self.textureBuffer, 0)

        self.renderBuffer = GL.glGenRenderbuffers(1)
        GL.glBindRenderbuffer( GL.GL_RENDERBUFFER, self.renderBuffer )
        GL.glRenderbufferStorage(GL.GL_RENDERBUFFER,GL.GL_RGBA,640,480)
        GL.glFramebufferRenderbuffer( GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_RENDERBUFFER, self.renderBuffer )
        GL.glBindRenderbuffer( GL.GL_RENDERBUFFER, 0 )
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0 )

        GL.glBindTexture( GL.GL_TEXTURE_2D, self.textureBuffer)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP)

        GL.glBindTexture( GL.GL_TEXTURE_2D, 0 )
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo )

        GL.glDrawBuffer(GL.GL_NONE);

        # GL.glViewport(0,0,640,480)
        FBOstatus = GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER)
        if FBOstatus != GL.GL_FRAMEBUFFER_COMPLETE:
            print ("GL.GL_FRAMEBUFFER_COMPLETE failed, CANNOT use FBO\n");

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER,0)
 
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
        for obj in self._object_names:
            self.objects.append((ObjParser.ObjParser(obj[0]), obj[1]))
 
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
        self._shadowMap()

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
            GL.glCallList(obj[0].getGlList())
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
 