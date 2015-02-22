#!/usr/bin/python2
# -*- coding: utf8 -*-

import threading
import math
import numpy

class Camera(object):
    RATIO_DEGRE_RAD = 57.2957
    """The Camera of the main OpenGl view
    It's nearly thread-safe"""
    def __init__(self):
        """ Constructeur de la classe Camera"""
        self._position = [0,10,-20]
        self._direction = [0,0] # first is rotation around x => vertical
        self.lock = threading.Lock()
        self._zoomAmplitude = 0.15

    def getX(self):
        return self._position[0]

    def getY(self):
        return self._position[1]

    def getZ(self):
        return self._position[2]

    def getVerticalAngle(self):
        return self._direction[0]

    def getHorizontalAngle(self):
        return self._direction[1]

    def getDirectionX(self):
        return self._direction[0]

    def getDirectionY(self):
        return self._direction[1]

    def setVerticalAngle(self,angle):
        if angle != self._direction[0]:
            self._direction[0] = angle
            return True
        return False

    def getHorizontalAngle(self, angle):
        if angle != self._direction[1]:
            self._direction[1] = angle
            return True
        return False

    def rotateHorizontal(self, deltaAngle):
        self._direction[1] += deltaAngle


    def rotateVertical(self, deltaAngle):
        self._direction[0] += deltaAngle


    def _directionVectorFromAngle(self):
        return (math.sin(self._direction[0]/Camera.RATIO_DEGRE_RAD),
                math.sin(self._direction[1]/Camera.RATIO_DEGRE_RAD),
                math.cos(self._direction[0]/Camera.RATIO_DEGRE_RAD))



    def zoomIn(self):
        self._position = list(numpy.add(self._position, numpy.multiply(self._zoomAmplitude,self._directionVectorFromAngle())))

    def zoomOut(self):
        self._zoomAmplitude = -self._zoomAmplitude
        self.zoomIn()
        self._zoomAmplitude = -self._zoomAmplitude

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
        

if __name__ == '__main__':
    camera = Camera()
    assert (camera._position == (0,10,-20))
    assert (camera._direction == (0,0))
    camera.zoomIn()
    print camera._directionVectorFromAngle()
    print camera._position
    # assert (camera._position == (0.0, 11.0, -19.0))

