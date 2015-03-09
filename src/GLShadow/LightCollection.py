#!/usr/bin/python2
# -*- coding: utf-8 -*-

from GLShadow.Light import Light
from GLShadow.AutoRotateLight import AutoRotateLight


class LightCollection(list):
    """docstring for LightCollection"""
    def __init__(self, *args):
        list.__init__(self, *args)
        l = Light()
        self.append(l)
        self._selection = 0
        self._incrementationRotate = 3
        self._lightRotation = [AutoRotateLight(l,self._incrementationRotate)]

    def addLight(self, light):
        """ """
        self.append(light)
        self._lightRotation.append(AutoRotateLight(light,self._incrementationRotate))
    
    def getLightList(self):
        """ """
        return self

    def deleteLight(self, lightIndex):
        """ """
        if len(self) > 1:
            del self[lightIndex]
            del self._lightRotation[lightIndex]

    def getSelectedLight(self):
        """ """
        return self[self._selection]

    def setSelection(self,index):
        """ """
        if index < len(self):
            self._selection = index
        else:
            print("LightCollection.setSelection index out of range")

    def switchLightAnimation(self):
        """ """
        if self._lightRotation[self._selection]:
            if self._lightRotation[self._selection].getAlive():
                self._lightRotation[self._selection].stop()
            else:
                self._lightRotation[self._selection].start()


    def killThreads(self):
        """ """
        for l in self._lightRotation:
            l.stop()


