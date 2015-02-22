#!/usr/bin/python2
# -*- coding: utf8 -*-

import threading
import math
import numpy

class Camera(object):
    RATIO_DEGREE_RADIAN = 57.2957795
    """The Camera of the main OpenGl view
    It's nearly thread-safe"""
    def __init__(self):
        """ Constructeur de la classe Camera"""
        self._position = [0,0,30]
        self._direction = [0,0] # first is rotation around x => vertical
        self.lock = threading.Lock()
        self._zoomAmplitude = 1
        self._limitUp = 60
        self._limitDown = -10
        self._limitSide = 60
        self._keyStep = 1

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
        if angle != self._direction[0] and 0 < angle < 90:
            self._direction[0] = angle
            return True
        return False

    def setHorizontalAngle(self, angle):
        if angle != self._direction[1]:
            self._direction[1] = self._normalizeAngle(angle)
            return True
        return False

    def rotateHorizontal(self, deltaAngle):
        self._direction[1] += deltaAngle
        self._direction[1] = self._normalizeAngle(self._direction[1])


    def rotateVertical(self, deltaAngle):
        self._direction[0] += deltaAngle


    def _directionVectorFromAngle(self):
        return (math.sin(self._direction[0]/Camera.RATIO_DEGREE_RADIAN),
                math.sin(self._direction[1]/Camera.RATIO_DEGREE_RADIAN),
                math.cos(self._direction[0]/Camera.RATIO_DEGREE_RADIAN))


    def up(self):
        """ """
        if self._position[1] + self._keyStep < self._limitUp:
            self._position[1] += self._keyStep

    def down(self):
        """ """
        print(self._position[1])
        if self._position[1] - self._keyStep > self._limitDown:
            self._position[1] -= self._keyStep

    def left(self):
        """ """
        if self._position[0] - self._keyStep > self._limitDown:
            self._position[0] -= self._keyStep

    def right(self):
        """ """
        if self._position[0] + self._keyStep < self._limitUp:
            self._position[0] += self._keyStep


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


    def setThetaAngle(self):
        """ """
        self._rayon = math.sqrt(self._position[0]**2 + self._position[2]**2)
        if self._position[0] < 0 and self._position[2] < 0:
            theta = math.atan(self._position[2]/self._position[0]) * self.RATIO_DEGREE_RADIAN
            theta += 180
        elif self._position[2] > 0:
            theta = math.acos(self._position[0]/self._rayon) * self.RATIO_DEGREE_RADIAN
        else:
            theta = math.asin(self._position[2]/self._rayon) * self.RATIO_DEGREE_RADIAN

        self._theta = theta

    def incrementeRotate(self,plus):
        """ Increment Y value by plus, for rotation of the plane"""
        self.lock.acquire()
        # self._theta +=  plus
        # self._theta = self._normalizeAngle(self._theta)
        # oldX = self._position[0]
        # oldZ = self._position[2]
        # self._position[0] = self._rayon * math.cos(self._theta/self.RATIO_DEGREE_RADIAN)
        # self._position[2] = self._rayon * math.sin(self._theta/self.RATIO_DEGREE_RADIAN)
        # rotation = self.RATIO_DEGREE_RADIAN *math.acos( (oldX*self._position[0] + oldZ *self._position[2]) / (math.sqrt(oldX**2 + oldZ**2) * math.sqrt(self._position[0]**2 + self._position[2]**2) ))
        self.rotateHorizontal(plus)
        # print(self._direction[1])
        self.lock.release()
        

if __name__ == '__main__':
    camera = Camera()
    assert (camera._position == (0,10,-20))
    assert (camera._direction == (0,0))
    camera.zoomIn()
    print camera._directionVectorFromAngle()
    print camera._position
    # assert (camera._position == (0.0, 11.0, -19.0))

