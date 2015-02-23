#!/usr/bin/python2
# -*- coding: utf-8 -*-

import Light

class LightCollection(list):
    """docstring for LightCollection"""
    def __init__(self, *args):
        list.__init__(self, *args)
        self.append(Light.Light())
        self._selection = 0

    def addLight(self, light):
        """ """
        self.append(light)
    
    def getLightList(self):
        """ """
        return self

    def deleteLight(self, lightIndex):
        """ """
        if len(self) > 1:
            del self[lightIndex]

    def getSelectedLight(self):
        """ """
        return self[self._selection]

    def setSelection(self,index):
        """ """
        if index < len(self):
            self._selection = index
        else:
            print("LightCollection.setSelection index out of range")