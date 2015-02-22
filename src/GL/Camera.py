#!/usr/bin/python2
# -*- coding: utf8 -*-

import threading

class Camera(object):
    """The Camera of the main OpenGl view
    It's nearly thread-safe"""
    def __init__(self):
        """ Constructeur de la classe Camera"""
        self._x = 7
        self._xInterval = [2,45]
        self._y = 0
        self._z = 6
        self._zoom = -20.0
        self._zoomAmplitude = 0.15
        self.lock = threading.Lock()

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getZ(self):
        return self._z

    def getZoom(self):
        return self._zoom

    def setX(self,x):
        """ set the X value after having normalized it"""
        self.lock.acquire()
        res = False
        if x < self._xInterval[0]:
            x = self._xInterval[0]
        elif x > self._xInterval[1]:
            x = self._xInterval[1]
        x = self._normalizeAngle(x)
        if x != self._x:
            self._x = x
            res = True
        self.lock.release()
        return res

    def setY(self,y):
        """ set the Y value after having normalized it"""
        self.lock.acquire()
        res = False
        y = self._normalizeAngle(y)
        if y != self._y:
            self._y = y
            res = True
        self.lock.release()
        return res

    def setZ(self,z):
        """ set the Z value after having normalized it"""
        self.lock.acquire()
        res = False
        z = self._normalizeAngle(z)
        if z != self._z:
            self._z = z
            res = True
        self.lock.release()
        return res

    def zoomIn(self):
        self._zoom += self._zoomAmplitude

    def zoomOut(self):
        self._zoom -= self._zoomAmplitude

    def _normalizeAngle(self, angle):
        """ Keep the angle between 0 and 360"""
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        return angle


    def incrementeRotate(self,plus):
        """ Increment Y value by plus, for rotation of the plane"""
        self.lock.acquire()
        y = self.getY() + plus
        y = self._normalizeAngle(y)
        self._y = y
        self.lock.release()
        